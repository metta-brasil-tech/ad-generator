"""LLM adapter — model-agnostic via LiteLLM.

Suporta Claude, OpenAI, Gemini, Mistral, Groq, Ollama (local).
Trocar provider = trocar env var. Zero refactor de código.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

try:
    import litellm
    from litellm import completion, embedding
    _LITELLM_OK = True
except ImportError:
    _LITELLM_OK = False


@dataclass
class LLMResponse:
    content: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    raw: Any


class LLMAdapter:
    """Unified LLM interface across providers via LiteLLM."""

    def __init__(self, provider: str | None = None, model: str | None = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "claude")
        self.model = model or self._resolve_model(self.provider)
        self.temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0"))

        if not _LITELLM_OK:
            raise ImportError("litellm not installed. Run: pip install litellm")

    @staticmethod
    def _resolve_model(provider: str) -> str:
        env_var = f"LLM_MODEL_{provider.upper()}"
        model = os.getenv(env_var)
        if not model:
            defaults = {
                # Sonnet 4.6 ($3/$15 por 1M) — a própria skill 04 recomenda "Claude
                # Sonnet ou GPT-4o" pra engenharia de prompt de imagem. Escrever prompt
                # a partir de template não exige o raciocínio (nem o custo) do Opus
                # ($5/$25). Override por env: LLM_MODEL_CLAUDE.
                "claude": "claude-sonnet-4-6",
                "openai": "gpt-5",
                "gemini": "gemini/gemini-2.5-flash",  # string litellm válida (testada)
                "ollama": "llama3.1:70b",
            }
            model = defaults.get(provider, provider)
        return model

    def _fallback_model(self, e: Exception) -> str | None:
        """Modelo pra REFAZER quando o provider primário estoura cota/billing/auth/
        rate — escolhe um provider com chave disponível QUE NÃO SEJA o que falhou.
        Ordem: Gemini > Claude > OpenAI (Gemini primeiro porque é o que tem crédito
        aqui; antes só caía pro Claude, que hoje está sem crédito). None = não refaz.
        Desliga com LLM_FALLBACK=0 (ou o legado LLM_FALLBACK_CLAUDE=0)."""
        if os.getenv("LLM_FALLBACK", os.getenv("LLM_FALLBACK_CLAUDE", "1")) != "1":
            return None
        name = e.__class__.__name__.lower()
        msg = str(e).lower()
        transient = (
            "ratelimit" in name or "authentication" in name or "permission" in name
            or any(k in msg for k in ("quota", "rate limit", "billing", "insufficient",
                                      "exceeded your current", "credit balance", "credit",
                                      "invalid api key", "api key"))
        )
        if not transient:
            return None
        cur = str(self.model)
        has_gem = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
        has_claude = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_KEY"))
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        if has_gem and not cur.startswith("gemini/"):
            return os.getenv("LLM_MODEL_GEMINI", "gemini/gemini-2.5-flash")
        if has_claude and not cur.startswith(("claude-", "anthropic/")):
            return os.getenv("LLM_MODEL_CLAUDE", "claude-opus-4-8")
        if has_openai and not cur.startswith(("gpt-", "openai/")):
            return os.getenv("LLM_MODEL_OPENAI", "gpt-5")
        return None

    def complete(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Complete with optional JSON Schema constraint (function calling)."""
        import time
        t0 = time.time()

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        # Claude models deprecated temperature — only send for non-Claude providers
        if not self.model.startswith(("claude-", "anthropic/")):
            kwargs["temperature"] = self.temperature

        # JSON Schema-constrained output — only for OpenAI (Claude doesn't support oneOf/anyOf)
        if json_schema is not None and not self.model.startswith(("claude-", "anthropic/")):
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "Output", "schema": json_schema, "strict": False},
            }

        # Timeout + retries: sem isso, uma request travada (socket parado) prende o
        # pipeline inteiro por horas (já aconteceu). litellm aborta em LLM_TIMEOUT_S
        # e retenta LLM_NUM_RETRIES vezes com backoff.
        kwargs["timeout"] = float(os.getenv("LLM_TIMEOUT_S", "90"))
        kwargs["num_retries"] = int(os.getenv("LLM_NUM_RETRIES", "2"))

        try:
            response = completion(**kwargs)
        except Exception as e:
            # AUTO-CURA: se o provider primário estourar cota/billing/auth, refaz num
            # provider com chave disponível (Gemini > Claude > OpenAI). O site não pode
            # morrer (500) porque a conta de UM provider secou. Caso real atual: a
            # Anthropic está sem crédito ("credit balance too low") → cai pro Gemini.
            # Desliga com LLM_FALLBACK=0.
            fb_model = self._fallback_model(e)
            if not fb_model:
                raise
            import sys as _sys
            print(f"[llm] provider primário falhou ({e.__class__.__name__}); "
                  f"caindo pro fallback ({fb_model})", file=_sys.stderr)
            kwargs["model"] = fb_model
            if fb_model.startswith(("claude-", "anthropic/")):
                kwargs.pop("temperature", None)    # Claude descontinuou temperature
                kwargs.pop("response_format", None)  # e não suporta json_schema aqui
            response = completion(**kwargs)
            self.model = fb_model  # reflete o que REALMENTE rodou
        elapsed_ms = int((time.time() - t0) * 1000)

        content = response.choices[0].message.content or ""
        usage = response.usage if hasattr(response, "usage") else None

        return LLMResponse(
            content=content,
            tokens_in=getattr(usage, "prompt_tokens", 0) if usage else 0,
            tokens_out=getattr(usage, "completion_tokens", 0) if usage else 0,
            latency_ms=elapsed_ms,
            raw=response,
        )

    def complete_json(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
    ) -> tuple[dict, LLMResponse]:
        """Complete and parse JSON output. Retries once on parse failure."""
        for attempt in range(2):
            resp = self.complete(system, user, json_schema=json_schema)
            try:
                # Strip markdown code fences if present
                content = resp.content.strip()
                if content.startswith("```"):
                    content = content.split("\n", 1)[1] if "\n" in content else content
                    content = content.rsplit("```", 1)[0] if "```" in content else content
                data = json.loads(content)
                return data, resp
            except json.JSONDecodeError as e:
                if attempt == 1:
                    raise ValueError(f"LLM did not return valid JSON after retry: {e}\nContent: {resp.content[:500]}")
                user = f"{user}\n\nIMPORTANT: previous response was not valid JSON. Return ONLY a valid JSON object, no markdown fences, no prose."
        raise RuntimeError("unreachable")


class MockLLMAdapter:
    """No-op adapter for dry-run / dataflow validation. Returns canned responses."""

    def __init__(self, fixtures: dict[str, dict] | None = None):
        self.fixtures = fixtures or {}

    def complete(self, system: str, user: str, json_schema=None, max_tokens=4096) -> LLMResponse:
        # Identify which skill is calling based on system content fingerprint
        skill = self._identify_skill(system)
        canned = self.fixtures.get(skill, {})
        return LLMResponse(
            content=json.dumps(canned, ensure_ascii=False),
            tokens_in=0, tokens_out=0, latency_ms=5,
            raw=None,
        )

    def complete_json(self, system: str, user: str, json_schema=None) -> tuple[dict, LLMResponse]:
        resp = self.complete(system, user, json_schema=json_schema)
        return json.loads(resp.content), resp

    @staticmethod
    def _identify_skill(system: str) -> str:
        markers = {
            "briefing-parser": "Skill 01",
            "style-selector": "Skill 02",
            "layout-composer": "Skill 03",
            "image-prompt-engineer": "Skill 04",
            "assembler": "Skill 05",
            "qa-validator": "Skill 06",
        }
        for name, marker in markers.items():
            if marker in system:
                return name
        return "unknown"


class EmbeddingAdapter:
    """Embedding generator via LiteLLM (works with OpenAI, Cohere, Voyage, etc.)."""

    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")

    def embed(self, text: str) -> list[float]:
        if not _LITELLM_OK:
            raise ImportError("litellm not installed")
        response = embedding(model=self.model, input=[text])
        return response.data[0]["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = embedding(model=self.model, input=texts)
        return [d["embedding"] for d in response.data]
