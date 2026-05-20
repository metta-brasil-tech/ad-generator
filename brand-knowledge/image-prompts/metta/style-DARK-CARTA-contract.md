# Image Prompt — DARK-CARTA (contract mockup)
> Model: gpt-image-2 | Format: STORY 1080×1920 | Placement: center-top

## Base instruction
Generate a photorealistic 3D mockup of a premium formal document (contract or letter) positioned at a slight angle (8–12° clockwise tilt) against a deep dark background (#0C161B). The document occupies approximately 45% of the vertical canvas height and is centered horizontally, placed in the upper half of the frame.

## Document appearance
- White or off-white heavyweight paper (200 gsm texture)
- Visible paper grain and subtle shadow beneath the document
- Elegant gold or cream letterhead at the top — understated, no specific brand name
- A few lines of faint body text (unreadable, blurred for mystery/confidentiality)
- A round wax-style gold seal in the lower-right corner of the document — embossed "M" monogram, premium feel
- Subtle drop-shadow at 20–30px offset to ground the object on the dark background

## Lighting
- Rim lighting from top-left: warm white light catches the paper edge
- Soft ambient fill from front to maintain legibility
- No harsh reflections; matte paper finish

## Background
- Solid #0C161B (very dark blue-black)
- No texture, no gradient — pure flat dark

## Mood
Luxury, exclusivity, formal invitation, scarcity. Think: "You have been selected." Not corporate bureaucracy — aspirational elite membership.

## Negative prompts
- No text that is legible or contains real words
- No envelopes, stamps, or postal elements
- No bright colors or neon accents
- No people or hands visible
- No cluttered desk or office context — isolated object only

## gpt-image-2 parameters
```json
{
  "model": "gpt-image-2",
  "size": "1024x1792",
  "quality": "high",
  "style": "natural"
}
```

## Dynamic prompt injection (pipeline fills these at runtime)
The pipeline may append context like:
- "The contract relates to: {briefing.product}"
- "Urgency level: {briefing.urgency_tone}"

Keep the core visual stable; only lighting warmth or seal detail may shift.
