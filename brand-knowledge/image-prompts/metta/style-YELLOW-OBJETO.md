# Image Prompt — Estilo YELLOW-OBJETO

> Herda de `_base.md`. Skill 04 escolhe a seção correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Objeto 3D estilizado (render matte/clay, NÃO fotografia, NÃO cartoon 2D) flutuando
isolado sobre fundo amarelo chapado. É a metáfora visual do conceito da copy —
ex: um processo/hábito difícil virando fácil = objeto que parece pesado mas está
sendo escalado/sustentado com uma ferramenta simples (escada, corda). Estética de
capa de app ou ilustração editorial contemporânea (Notion/Stripe/Linear blog
style), não corporativa séria.

## SEÇÃO PROD — gpt-image-1 / gpt-image-2

### Template

```
3D rendered illustration in a matte clay/soft-plastic material style (like modern
app onboarding art or a Pixar concept render), of {object_description}, isolated
and floating on a solid flat SOLID YELLOW background (hex #F5C518 or similar warm
amber-yellow, NO gradient, NO texture, NO shadow gradient on the backdrop itself),
soft studio three-point lighting on the object with gentle contact shadow beneath
it, matte non-glossy surface finish, {accent_prop_if_any}, minimalist clean
composition with generous negative space around the object, object positioned in
the lower two-thirds of the frame,
high production 3D render quality, smooth clay-like textures, muted secondary
color on the object itself (not bright rainbow, 1-2 accent colors max),
without photorealism, without real photography look, without cartoon 2D flat
illustration, without hand-drawn line art, without text or logos in image
```

### Variáveis

| Var | Opções |
|---|---|
| `{object_description}` | "a dark rocky cliff formation with a melting/dripping wax-like texture along its edges, with a simple aluminum ladder leaning against it reaching up to a plain wooden stool balanced on its flat top" / "a giant boulder with a single sapling growing from a crack at its top" / "a spiral staircase floating in mid-air leading to nothing" — depende da metáfora da copy |
| `{accent_prop_if_any}` | "a thin metal ladder as the only secondary prop" / "no secondary props, single hero object only" |

### Exemplo preenchido — "vai ficando mais fácil, é só fazer todo dia"

```
3D rendered illustration in a matte clay/soft-plastic material style (like modern app onboarding art or a Pixar concept render), of a dark rocky cliff formation with a melting/dripping wax-like black texture along its edges, with a simple aluminum ladder leaning against it reaching up to a plain wooden stool balanced on its flat top, isolated and floating on a solid flat SOLID YELLOW background (hex #F5C518, NO gradient, NO texture), soft studio three-point lighting on the object with a gentle contact shadow beneath it, matte non-glossy surface finish, a thin metal ladder as the only secondary prop, minimalist clean composition with generous negative space around the object, object positioned in the lower two-thirds of the frame, high production 3D render quality, smooth clay-like textures, muted dark palette on the object itself against the bright yellow backdrop, without photorealism, without real photography look, without cartoon 2D flat illustration, without hand-drawn line art, without text or logos
```

## Versão

`style-YELLOW-OBJETO_v1.0` · 2026-07-02 · novo estilo, cobre lacuna de render 3D estilizado (nenhum outro estilo Metta permite 3D render — todos pedem fotorrealismo)
