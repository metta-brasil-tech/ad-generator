"""Image generation adapter — Nano Banana 2 (Gemini) / gpt-image-1 / DALL-E 3.

Implementação real. Use `IMAGE_GEN_PROVIDER` env var pra escolher provider.
Salva PNG local em artifacts/images/ + retorna URL/path.
"""
from __future__ import annotations

import base64
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx


@dataclass
class ImageGenResult:
    url: str          # file:// path or http URL
    local_path: str   # absolute path to saved PNG
    provider: str
    model: str
    elapsed_ms: int
    cost_usd: float | None = None


def _save_bytes(data: bytes, name: str) -> Path:
    out_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts")) / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.png"
    out_path.write_bytes(data)
    return out_path


def _aspect_to_size(aspect: str, provider: str, model: str = "") -> str:
    """Map aspect ratio to provider-specific size string."""
    if provider == "openai":
        if model == "gpt-image-1":
            # gpt-image-1: 1024x1024, 1024x1536 (portrait), 1536x1024 (landscape)
            mapping = {"9:16": "1024x1536", "3:4": "1024x1536", "16:9": "1536x1024", "1:1": "1024x1024"}
        else:
            # dall-e-3: 1024x1024, 1024x1792 (portrait), 1792x1024 (landscape)
            mapping = {"9:16": "1024x1792", "3:4": "1024x1792", "16:9": "1792x1024", "1:1": "1024x1024"}
    elif provider == "gemini":
        mapping = {"9:16": "9:16", "16:9": "16:9", "1:1": "1:1", "4:3": "4:3", "3:4": "3:4"}
    else:
        mapping = {}
    return mapping.get(aspect, "1024x1024")


class OpenAIImageGen:
    """OpenAI Images API. Supports gpt-image-2, gpt-image-1, dall-e-3."""

    def __init__(self, model: str = "gpt-image-2"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_IMAGE_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY (or OPENAI_IMAGE_API_KEY) not set")

    def generate(self, prompt: str, aspect_ratio: str = "9:16") -> ImageGenResult:
        t0 = time.time()
        size = _aspect_to_size(aspect_ratio, "openai", model=self.model)

        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        if self.model in ("gpt-image-2", "gpt-image-1"):
            payload = {
                "model": self.model,
                "prompt": prompt[:4000],
                "size": size,
                "quality": "high",
                "n": 1,
            }
            est_cost = 0.19 if size == "1024x1792" else 0.17
        else:
            # dall-e-3 legacy
            payload = {
                "model": self.model,
                "prompt": prompt[:4000],
                "size": size,
                "quality": "hd",
                "n": 1,
                "response_format": "b64_json",
            }
            est_cost = 0.08 if size == "1024x1792" else 0.04

        r = httpx.post(url, headers=headers, json=payload, timeout=180)
        if r.status_code != 200:
            raise RuntimeError(f"OpenAI image-gen {r.status_code}: {r.text[:400]}")
        data = r.json()["data"][0]
        b64 = data.get("b64_json") or ""
        if not b64:
            # gpt-image-1 may return URL instead — handle both
            if "url" in data:
                img_bytes = httpx.get(data["url"], timeout=60).content
            else:
                raise RuntimeError(f"OpenAI returned no image data: {str(data)[:300]}")
        else:
            img_bytes = base64.b64decode(b64)

        name = f"openai_{int(t0)}"
        local = _save_bytes(img_bytes, name)
        return ImageGenResult(
            url=f"file://{local}",
            local_path=str(local),
            provider="openai",
            model=self.model,
            elapsed_ms=int((time.time() - t0) * 1000),
            cost_usd=est_cost,
        )


class GeminiImageGen:
    """Gemini Image (Nano Banana 2 / Imagen 3) via Google Generative AI API."""

    def __init__(self, model: str = "imagen-3.0-generate-002"):
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY (or GOOGLE_API_KEY) not set")

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "9:16",
        reference_images: list[str] | None = None,
    ) -> ImageGenResult:
        t0 = time.time()

        # Imagen 3 endpoint
        # Note: Nano Banana 2 specifically = gemini-2.5-flash-image-preview
        # Imagen 3 = imagen-3.0-generate-002 — pick based on self.model
        if "imagen" in self.model.lower():
            return self._generate_imagen(prompt, aspect_ratio, t0)
        return self._generate_nano_banana(prompt, aspect_ratio, reference_images, t0)

    def _generate_imagen(self, prompt: str, aspect_ratio: str, t0: float) -> ImageGenResult:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:predict"
            f"?key={self.api_key}"
        )
        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": _aspect_to_size(aspect_ratio, "gemini"),
            },
        }
        r = httpx.post(url, json=payload, timeout=120)
        r.raise_for_status()
        preds = r.json().get("predictions", [])
        if not preds:
            raise RuntimeError(f"Imagen returned no predictions: {r.text[:300]}")
        b64 = preds[0].get("bytesBase64Encoded") or preds[0].get("image", {}).get("bytesBase64Encoded")
        if not b64:
            raise RuntimeError(f"Imagen prediction missing image bytes: {preds[0]}")
        png = base64.b64decode(b64)
        name = f"imagen_{int(t0)}"
        local = _save_bytes(png, name)
        return ImageGenResult(
            url=f"file://{local}",
            local_path=str(local),
            provider="gemini",
            model=self.model,
            elapsed_ms=int((time.time() - t0) * 1000),
            cost_usd=0.04,
        )

    def _generate_nano_banana(
        self,
        prompt: str,
        aspect_ratio: str,
        reference_images: list[str] | None,
        t0: float,
    ) -> ImageGenResult:
        """Nano Banana 2 = gemini-2.5-flash-image-preview (multimodal native)."""
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        parts: list[dict] = [{"text": prompt}]
        # Reference images (if provided as local paths or http URLs)
        for ref in (reference_images or []):
            try:
                img_bytes = self._read_image(ref)
                parts.append({
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": base64.b64encode(img_bytes).decode("ascii"),
                    }
                })
            except Exception as e:
                print(f"  ⚠ reference image failed: {ref} → {e}")

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
            },
        }
        r = httpx.post(url, json=payload, timeout=180)
        r.raise_for_status()
        body = r.json()

        # Extract image bytes from candidates
        for cand in body.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    png = base64.b64decode(inline["data"])
                    name = f"nano_banana_{int(t0)}"
                    local = _save_bytes(png, name)
                    return ImageGenResult(
                        url=f"file://{local}",
                        local_path=str(local),
                        provider="gemini",
                        model=self.model,
                        elapsed_ms=int((time.time() - t0) * 1000),
                        cost_usd=0.04,
                    )

        raise RuntimeError(f"Nano Banana returned no image: {str(body)[:300]}")

    @staticmethod
    def _read_image(ref: str) -> bytes:
        """Read image from local path or http URL."""
        if ref.startswith(("http://", "https://")):
            return httpx.get(ref, timeout=30).content
        if ref.startswith("figma://"):
            raise NotImplementedError("figma:// refs need Figma API resolution — pass http URL instead")
        return Path(ref).read_bytes()


class MockImageGen:
    """No-op for testing dataflow."""

    def generate(self, prompt: str, aspect_ratio: str = "9:16", **kwargs) -> ImageGenResult:
        placeholder = "https://placehold.co/1080x1920/0C161B/FFBE18/png?text=MOCK+%5BAI+IMAGE%5D"
        return ImageGenResult(
            url=placeholder, local_path="", provider="mock", model="mock",
            elapsed_ms=10, cost_usd=0.0,
        )


class ImageGenAdapter:
    """Unified entry point — selects backend by env var."""

    def __init__(self, provider: str | None = None):
        self.provider = (provider or os.getenv("IMAGE_GEN_PROVIDER", "openai")).lower()

        if self.provider == "mock":
            self.backend = MockImageGen()
        elif self.provider in ("openai", "gpt-image-2", "gpt-image-1", "dall-e-3"):
            model = "dall-e-3" if self.provider == "dall-e-3" else (
                "gpt-image-1" if self.provider == "gpt-image-1" else "gpt-image-2"
            )
            self.backend = OpenAIImageGen(model=model)
        elif self.provider in ("nano-banana-2", "gemini-nano-banana"):
            self.backend = GeminiImageGen(model="gemini-2.5-flash-image-preview")
        elif self.provider in ("gemini", "imagen", "imagen-3"):
            self.backend = GeminiImageGen(model="imagen-3.0-generate-002")
        else:
            raise ValueError(f"Unknown image-gen provider: {self.provider}")

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        aspect_ratio: str = "9:16",
        reference_images: list[str] | None = None,
    ) -> ImageGenResult:
        # Embed negative prompt by appending it (OpenAI doesn't have native, Gemini ignores)
        full_prompt = prompt
        if negative_prompt:
            full_prompt += f"\n\nAVOID: {negative_prompt}"
        try:
            if isinstance(self.backend, GeminiImageGen):
                return self.backend.generate(full_prompt, aspect_ratio, reference_images)
            return self.backend.generate(full_prompt, aspect_ratio)
        except Exception as e:
            print(f"  [fail] image-gen failed: {e}")
            return MockImageGen().generate(prompt, aspect_ratio)
