# Image Prompt — DARK-OBJETO (3D metaphorical object)
> Model: gpt-image-2 | Format: STORY 1080×1920 | Placement: center-top

## Base instruction
Generate a dramatic, photorealistic 3D render of a single symbolic object that metaphorically represents transformation, growth, or strategic power. The object occupies the upper 45–50% of the canvas, centered, with moody rim lighting against a deep dark background.

## Object selection (pipeline injects based on briefing tese)
The pipeline will specify the object via `{briefing.objeto_metafora}`. If not provided, default to:
- A geometric crystal or prism (transformation / clarity)
- A chess piece — king or rook (strategy / dominance)
- A compass or chronometer (precision / navigation)
- A single polished stone or obsidian sphere (solidity / permanence)

## Visual style
- Hyper-detailed surface: visible material texture (glass, metal, stone, ceramic)
- Moody rim light from top-left: warm amber or cool blue depending on object material
- Subtle lens flare or light scatter on glass/crystal objects
- Object casts a soft shadow downward — grounding it in space
- No background context: pure isolated object against flat dark (#0C161B)

## Lighting
- Primary: directional from top-left at 45° angle — creates strong highlight and deep shadow
- Rim light: thin warm line tracing the right edge of the object
- Ambient: near-zero — dramatic contrast, not flat

## Background
- Solid #0C161B with no gradient or texture
- Optionally: very subtle radial vignette (barely perceptible) to focus attention on object

## Mood
Power, clarity, intentional transformation. Premium B2B authority. Not decorative — each object choice carries meaning.

## Negative prompts
- No multiple objects or busy scenes
- No text, logos, or labels on the object
- No photographic stock-image aesthetic — must feel like a 3D art render
- No bright backgrounds, white rooms, or studio setups visible
- No people or hands

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
The pipeline appends:
- "Object: {briefing.objeto_metafora}" (e.g., "chess king", "crystal prism", "compass")
- "Metaphor meaning: {briefing.tese}" (e.g., "strategic clarity", "decisive growth")
- "Material finish: {briefing.material}" (optional: "matte obsidian", "polished gold", "frosted glass")
