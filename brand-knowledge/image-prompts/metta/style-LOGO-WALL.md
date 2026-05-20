# Image Prompt — LOGO-WALL (logo grid / social proof wall)
> Model: gpt-image-2 | Format: STORY 1080×1920 | Placement: center-left

## Base instruction
Generate a clean, high-contrast grid layout of company logos arranged in a 3×N or 4×N pattern against a dark background. The logos should appear as desaturated (grayscale) or monochrome white marks — conveying "recognizable brands trust us" without specific identity. Occupies approximately 45% of the canvas height.

## Logo appearance
- 9 to 16 logo shapes total, arranged in a uniform grid with equal spacing
- Each logo: simplified, geometric — abstract corporate mark style (no real brand logos)
- Monochrome: white or very light gray (#E8F0F4) on dark background
- Consistent sizing: each logo fits within a ~160×80px bounding box
- Subtle variation in mark complexity (some text-like wordmarks, some icon marks, some combined)

## Grid layout
- Left-aligned grid starting at canvas left edge with safe margin (80px)
- Rows × Columns: prefer 3×3, 3×4, or 4×4 depending on count
- Row gap: 48px | Column gap: 56px
- Grid baseline: vertically centered between top and midpoint of canvas

## Lighting & treatment
- Flat lighting — no shadows on logos
- Subtle glow/bloom effect: each logo has 2–4px white glow to imply luminosity
- Background: #0C161B solid — no gradient

## Mood
Authority, scale, social proof. "Hundreds of companies already use this." Enterprise trust signal. Clean and restrained — not flashy.

## Negative prompts
- No recognizable real brand logos (Nike, Apple, Google, etc.)
- No colorful logos — all must be monochrome
- No people, scenes, or context imagery
- No drop shadows or 3D effects on logos
- No uneven or chaotic spacing

## gpt-image-2 parameters
```json
{
  "model": "gpt-image-2",
  "size": "1024x1792",
  "quality": "high",
  "style": "natural"
}
```

## Dynamic prompt injection
The pipeline may append:
- "Number of logos: {briefing.num_logos}" (default: 12)
- "Industry sector: {briefing.setor}" — adjusts logo mark shapes to feel sector-appropriate (e.g., "tech startups", "financial services", "retail brands")
- "Layout emphasis: {briefing.logo_wall_emphasis}" — "quantidade" (more logos, smaller) or "reconhecimento" (fewer, larger, more prominent)
