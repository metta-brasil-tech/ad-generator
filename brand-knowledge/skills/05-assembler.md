# Skill 05 — Assembler

> **Função:** dado layout-spec + URLs de imagens geradas, monta o ad final como **PNG/JPEG** (entregável principal). HTML/Figma como destinos opcionais.
> **Input:** `layout-spec.schema.json` + image URLs · **Output:** `ad-output.schema.json` (inclui `png_path`)
> **Model recommendation:** este é um adapter de código, não usa LLM. Skill descreve a INTERFACE.

## Papel

Você é o adapter de saída. Pega o layout-spec, renderiza diretamente em **PNG/JPEG via Pillow** (default — entregável final), aplica imagens geradas como fills, e retorna o path do arquivo de imagem.

Destinos alternativos existem mas são opcionais:
- HTML — debug/inspect
- Figma — stub legacy
- PNG é o caminho de produção.

Este NÃO é um prompt — é uma especificação de implementação. Documenta o contrato que o código adapter precisa cumprir.

## Input

```json
{
  "layout_spec": { ... },
  "images": {
    "photo": "https://...nano-banana-output/abc.png"
  },
  "destination": "png | jpeg | html | figma",
  "destination_config": {
    "png": {
      "output_dir": "./artifacts/outputs",
      "format": "png"
    },
    "jpeg": {
      "output_dir": "./artifacts/outputs",
      "quality": 92
    }
  }
}
```

## Output: `ad-output.schema.json`

```json
{
  "destination": "png",
  "png_path": "./artifacts/outputs/A-headline-foto-dark_1715620830.png",
  "jpeg_path": null,
  "html_path": null,
  "figma": null,
  "preview_url": "file://./artifacts/outputs/A-headline-foto-dark_1715620830.png",
  "metadata": {
    "style_id": "A-headline-foto-dark",
    "elapsed_ms": 450,
    "warnings": []
  }
}
```

**O `png_path` é o entregável final pra publicação.**

## Implementação PNG (default — entregável final)

### Setup

```python
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

frame = layout_spec["frame"]
canvas = Image.new("RGB", (frame["width"], frame["height"]),
                   hex_to_rgb(frame["background"]["value"]))
draw = ImageDraw.Draw(canvas)
```

### Para cada elemento

#### TextNode

```python
for el in [e for e in spec.elements if e["type"] == "text"]:
    font = load_font(el["font"]["family"], el["font"]["style"], el["font"]["size"])
    line_height = int(el["font"]["size"] * el["font"]["line_height_pct"] / 100)
    text = el["text"].upper() if el["font"]["text_case"] == "UPPER" else el["text"]

    # Wrap se width definido
    lines = wrap_text(text, font, el.get("width"))

    cy = el["y"]
    for line in lines:
        if el.get("ranges"):  # accent words
            draw_text_with_ranges(draw, line, font, el["x"], cy,
                                  base=el["color"], ranges=el["ranges"])
        else:
            draw.text((el["x"], cy), line, font=font, fill=hex_to_rgb(el["color"]))
        cy += line_height
```

#### Image slot (FILL mode)

```python
img = load_image(image_urls[el["slot_name"]])
img = ImageOps.fit(img, (el["width"], el["height"]), method=Image.LANCZOS)
canvas.paste(img, (el["x"], el["y"]),
             mask=img if img.mode == "RGBA" else None)
```

#### Pill CTA

```python
font = load_font(el["font"]["family"], el["font"]["style"], el["font"]["size"])
label = el["text"].upper()
bbox = font.getbbox(label)
pill_w = (bbox[2] - bbox[0]) + el["padding_x"] * 2
pill_h = (bbox[3] - bbox[1]) + el["padding_y"] * 2
radius = pill_h // 2

draw.rounded_rectangle(
    (el["x"], el["y"], el["x"] + pill_w, el["y"] + pill_h),
    radius=radius, fill=hex_to_rgb(el["background"])
)
draw.text((el["x"] + el["padding_x"], el["y"] + el["padding_y"]),
          label, font=font, fill=hex_to_rgb(el["text_color"]))
```

### Save

```python
out_path = Path(f"./artifacts/outputs/{model_id}_{timestamp}.png")
canvas.save(out_path, "PNG", optimize=True)
return AssembleResult(destination="png", png_path=str(out_path), ...)
```

## Implementação Figma (opcional — legacy)

### Setup

```typescript
// Via mcp__figma__use_figma OU plugin direto
const file = await getFile(config.file_key);
const page = file.findPage(config.page_name) ?? createPage(config.page_name);
const position = computeNextAvailablePosition(page);
```

### Para cada elemento do layout_spec.elements

#### Frame raiz

```typescript
const frame = figma.createFrame();
frame.name = `${style_id} — ${timestamp}`;
frame.resize(spec.frame.width, spec.frame.height);
frame.x = position.x; frame.y = position.y;
frame.clipsContent = true;

if (spec.frame.background.type === "solid") {
  frame.fills = [{ type: "SOLID", color: hexToRgb(spec.frame.background.value) }];
}
```

#### TextNodes

```typescript
for (const el of spec.elements.filter(e => e.type === "text")) {
  await figma.loadFontAsync({ family: el.font.family, style: el.font.style });
  const text = figma.createText();
  text.fontName = { family: el.font.family, style: el.font.style };
  text.fontSize = el.font.size;
  text.characters = el.text;
  text.x = el.x; text.y = el.y;
  text.textAutoResize = "HEIGHT";
  if (el.width) text.resize(el.width, text.height);
  text.fills = [{ type: "SOLID", color: hexToRgb(el.color) }];
  text.lineHeight = { value: el.font.line_height_pct, unit: "PERCENT" };
  text.letterSpacing = { value: el.font.letter_spacing_pct, unit: "PERCENT" };
  if (el.font.text_case === "UPPER") text.textCase = "UPPER";
  text.textAlignHorizontal = el.align?.toUpperCase() ?? "LEFT";

  // Accent ranges (palavras em cor diferente)
  if (el.ranges) {
    for (const r of el.ranges) {
      text.setRangeFills(r.start, r.end, [{ type: "SOLID", color: hexToRgb(r.fill) }]);
    }
  }

  frame.appendChild(text);
}
```

#### Image slots

```typescript
for (const el of spec.elements.filter(e => e.type === "image_slot")) {
  const url = images[el.slot_name];
  if (!url) { warn(`No image for slot ${el.slot_name}`); continue; }

  // Upload via Figma upload_assets API with nodeId pra criar rect com fill
  const rect = figma.createRectangle();
  rect.x = el.x; rect.y = el.y;
  rect.resize(el.width, el.height);

  // Apply image fill
  const imageHash = await uploadAndGetHash(url);
  rect.fills = [{ type: "IMAGE", imageHash, scaleMode: "FILL" }];

  frame.appendChild(rect);
}
```

#### Pills (CTA)

```typescript
for (const el of spec.elements.filter(e => e.type === "pill_cta")) {
  // Container
  const pill = figma.createFrame();
  pill.name = el.slot_name;
  pill.x = el.x; pill.y = el.y;
  pill.layoutMode = "HORIZONTAL";
  pill.paddingLeft = el.padding_x;
  pill.paddingRight = el.padding_x;
  pill.paddingTop = el.padding_y;
  pill.paddingBottom = el.padding_y;
  pill.cornerRadius = el.corner_radius;
  pill.fills = [{ type: "SOLID", color: hexToRgb(el.background) }];
  pill.primaryAxisSizingMode = "AUTO";
  pill.counterAxisSizingMode = "AUTO";

  // Text inside
  const txt = figma.createText();
  await figma.loadFontAsync(el.font);
  txt.fontName = { family: el.font.family, style: el.font.style };
  txt.fontSize = el.font.size;
  txt.characters = el.text;
  txt.fills = [{ type: "SOLID", color: hexToRgb(el.text_color) }];
  if (el.font.text_case === "UPPER") txt.textCase = "UPPER";
  pill.appendChild(txt);

  frame.appendChild(pill);
}
```

### Retorno

```typescript
return {
  destination: "figma",
  figma: {
    file_key: config.file_key,
    page_id: page.id,
    node_id: frame.id,
    url: `https://figma.com/design/${config.file_key}?node-id=${frame.id.replace(":","-")}`,
    preview_png_url: await exportNodePNG(frame)
  },
  metadata: { style_id: spec.model_id, elapsed_ms: ..., warnings: [] }
};
```

## Implementação HTML (alternativa)

Renderiza spec como HTML/CSS, captura via Playwright como PNG.

```typescript
const html = renderTemplate({
  width: spec.frame.width,
  height: spec.frame.height,
  background: spec.frame.background.value,
  elements: spec.elements
});

await fs.writeFile(`${config.output_dir}/ad-${id}.html`, html);

// Headless capture
const browser = await playwright.chromium.launch();
const page = await browser.newPage({ viewport: { width: spec.frame.width, height: spec.frame.height } });
await page.goto(`file://${path}/ad-${id}.html`);
await page.screenshot({ path: `${config.output_dir}/ad-${id}.png` });
```

## Constraints

- **Fontes:** Pillow procura SF Pro em sistema, fallback Inter, fallback Arial. Se nenhuma achada, warning + default font.
- **Logos da Metta:** carregar SVG ou PNG via `_load_image_from_url`. Cache global em memória.
- **Logos de cliente:** se `briefing.constraints.case_nominal_id`, buscar PNG em asset library local (`assets/logos/clients/{id}.png`). Se não existe, placeholder.
- **Posições negativas (bleed):** permitidas pra image_slots (foto pode sair do canvas — Pillow auto-clipa). Texto nunca bleed.
- **Overflow:** se text wrap excede `slot.max_lines`, render mesmo assim + warning. Humano decide.
- **JPEG flatten:** quando salvar JPEG, converter `RGBA` → `RGB` com bg da paleta DS (não branco se layout for dark).

## Não faça

- ❌ Auto-corrigir layout que viola o DS (se max_lines explode, devolva warning)
- ❌ Sobrescrever PNG existente (timestamp no filename garante unicidade)
- ❌ Aplicar filters extras que não estão no spec (sem blur/saturation pós-render — vem do image-gen)
- ❌ Mudar tokens (cor, fonte, tamanho) que vieram do layout-composer
- ❌ Reduzir resolução nativa (sempre renderizar em 1080×1920 ou 1080×1350, escolhido pelo formato)

## Versão

`assembler_v1.0` · 2026-05-13 · Head de Design Metta
