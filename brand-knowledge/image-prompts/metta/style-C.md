# Image Prompt — Estilo C (Tipografia pura sobre escuro)

> Herda de `_base.md`.

## Função da imagem nesse estilo

**Não tem imagem.** Estilo C é puramente tipográfico.

## Quando o image-prompt-engineer é chamado pra estilo C

Retornar imediatamente:

```json
{
  "image_required": false,
  "rationale": "Estilo C-tipografia-pura-dark não usa imagem. Skip image-gen step.",
  "skip": true
}
```

Pipeline deve pular direto pro `05-assembler` sem chamar image-gen API.

## Versão

`style-C_v1.0` · 2026-05-13 · Head de Design Metta
