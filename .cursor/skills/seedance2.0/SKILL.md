---
name: seedance-2.0
description: >-
  Final Seedance 2.0 prompt generation only. Converts a scene brief into a
  TFT-ready plain-text prompt (FORMAT, shots, camera, tags). Use when writing
  seedance_prompt_v01.txt — not tft create-prompt. Creative content comes from
  the project scene brief; this skill owns prompt structure and videography.
---

# Seedance 2.0 — Final Prompt Generation

**Scope:** This skill produces the final `seedance_prompt_v01.txt` only. It does not plan scenes, assign registry assets, or run TFT commands.

**Input:** A scene brief from the project workflow (`scene.md` → `## Seedance brief` block, or equivalent YAML).

**Output:** Plain-text Seedance 2.0 prompt ready for `tft video-generate generate --prompt`.

Do **not** run `tft video-generate create-prompt`.

**Saquib@TheFluxTrain. All rights reserved.**

---

## Workflow

1. Read the scene brief — `duration`, `shots`, `tags`, `script`, `content`, `avoid`, `audio`.
2. Map brief `tags` to `@Image 1`, `@Image 2`, `@Audio 1` in CLI flag order.
3. Fill the cinematic prompt structure below using brief `content` for what happens; apply camera, timing, and formatting rules from this skill.
4. Run the pre-flight checklist.
5. Save to `prompts/seedance_prompt_v01.txt`.

**Do not ask questions** when the brief is complete. **Do not invent** script lines or creative beats not in the brief.

**Reference-first rule:** Tag `@Image N` for supplied references — describe motion, camera, and continuity only; do not re-describe face, wardrobe, or environment locked in the reference.

---

## Scene brief fields (input)

Expect these from the project skill / `scene.md`:

| Field | Use in prompt |
|-------|---------------|
| `duration` | `FORMAT: [N]s` |
| `shots` | `FORMAT: … / [N] SHOTS` |
| `aspect_ratio` | `VISUAL STYLE` |
| `script` | Dialogue inline in shot prose (speaking scenes) |
| `tags` | `PRIMARY CHARACTER`, `SETTING`, `SOUNDTRACK` — map to `@Image N` / `@Audio N` |
| `audio: generate_in_video` | No SOUNDTRACK section; write dialogue for `--generate-audio` |
| `audio: reference_only` | `SOUNDTRACK: @Audio 1`; do not transcribe music |
| `content` | Shot action, beat structure, text animation, performance |
| `avoid` | `WHAT TO AVOID` section |
| `pose_library_id` / `pose_setting` | `CONTINUITY` and shot prose (pose scenes) |

---

## TIMING MATTERS

| Duration | Capacity |
|----------|----------|
| 3 s | One tight beat — minimal action |
| 5 s | One clear action or short dialogue |
| 10 s | Two or three actions, at most |
| 15 s | Up to four distinct actions, maximum |

**Dialogue math:** ~2–3 s per spoken line. Cut before adding.

If the brief's `content` exceeds duration capacity, trim in the prompt — do not extend duration unless the brief says so.

---

## CINEMATIC PROMPT STRUCTURE

Plain text. No markdown bold. Sections in this order; skip empty optionals.

```
FORMAT: [duration]s / [shot count] SHOTS / [one-line concept]

PRIMARY CHARACTER: @Image 1.

SECONDARY CHARACTER[optional]: @Image 2.

SETTING: [Tag references (@Image N) — do not re-describe tagged refs]

SOUNDTRACK[optional]: @Audio 1 [or score description]

PALETTE[optional]: [Dominant color + accent]

VISUAL STYLE: [Aesthetic + technical specs + aspect ratio from brief]

CONTINUITY[optional]: [Anti-drift rules from brief]

WHAT TO AVOID: [From brief avoid list]

---

SHOT 1 — 0:00 to 0:0X. (First shot: no TRANSITION IN.)
TRANSITION OUT[if another shot follows]: [technique + concrete cue]
[Framing], [lens]mm, [camera movement].
[Actions, dialogue, beat structure — flowing prose from brief content.]

(Middle shots: both TRANSITION IN and TRANSITION OUT. Final shot: TRANSITION IN only, no TRANSITION OUT.)
```

**Single-shot briefs (`shots: 1`):** omit all transition lines. Put fade-in/out in framing and action prose.

---

## FORMATTING RULES — STRICT

- `@Image 1` / `@Audio 1` only — not `@image_1`, `[Image 1]`, filenames, or registry keys
- Whole-second timestamps: `0:00 to 0:05`
- `---` before shot block; blank line between shots
- Shot header separated from action prose by period + line break
- One `@Image N` per unique character

---

## TAG ASSIGNMENT

Map brief `tags` to prompt tags in the same order as CLI `--image`, `--reference-image`, `--reference-audio` flags:

| Brief key | Prompt tag |
|-----------|------------|
| `image_1` | `@Image 1` |
| `image_2` | `@Image 2` |
| `audio_1` | `@Audio 1` |

**I2V:** `@Image 1` = start frame; describe interpolation toward end state in shot prose.

**Reference-to-video:** tag each reference; state continuity and motion only.

---

## AUDIO IN PROMPT

| Brief `audio` | Prompt behavior |
|---------------|-----------------|
| `generate_in_video` | Exact `script` as inline dialogue; no SOUNDTRACK |
| `reference_only` | `SOUNDTRACK: @Audio 1`; visual beat sync only; no lyric transcription |

**POV device scenes:** add device-mic audio note when brief specifies POV.

---

## CAMERA LANGUAGE

### Framing

| Term | Meaning |
|------|---------|
| ECU | Extreme close-up |
| CU | Close-up — face and neck |
| MCU | Medium close-up — dialogue |
| MS | Medium shot — waist up |
| WS | Wide shot — full body in environment |
| OTS | Over-the-shoulder |
| POV | Camera is the eyes |

### Lenses

| Lens | Feel |
|------|------|
| 24–28mm | Wide, immersive |
| 35mm | Documentary, natural |
| 50mm | Neutral — default dialogue |
| 85mm | Intimate, shallow DOF |
| 100mm macro | Object/texture detail |

### Movement

| Term | Use |
|------|-----|
| Locked tripod / still shot | No pan, tilt, dolly, orbit |
| Slow push-in / zoom in | Emotional escalation |
| Slow pull-back | Reveal |
| Tracking | Follows subject |
| Handheld | Urgency, realism |
| Whip pan | Fast action transition |

Pick framing, lens, and movement to serve the brief's `content` — do not contradict brief camera constraints (e.g. "locked tripod" in content → locked shot only).

---

## TRANSITIONS (multi-shot only)

- Shot 1: `TRANSITION OUT` only
- Middle shots: both `TRANSITION IN` and `TRANSITION OUT`
- Final shot: `TRANSITION IN` only
- Pair adjacent OUT/IN; name technique + one concrete cue

Core terms: match cut, match on action, smash cut, cross dissolve, fade in/out, whip pan, L-cut/J-cut, invisible cut, graphic match, zoom transition.

---

## DIALOGUE

- Use exact `script` from brief — no paraphrase
- Inline in shot prose with double quotes
- 1–2 short lines per shot max
- Specify delivery pace when brief indicates (e.g. fast brisk pace)

---

## LOGIC RULES — PREVENT AI FAILURES

Add to CONTINUITY or WHAT TO AVOID when relevant:

| Failure | Rule |
|---------|------|
| Duplicate characters | Only one @Image 1 in frame at any time |
| Reference drift | Match @Image 1 exactly — no limb or framing changes |
| Props from nowhere | Prop introduced with visible motion |
| Environment too dark | Dim but visible — not pitch black |
| Autofocus hunting | Focus locked; no autofocus shifting |
| POV shows device | Camera IS the device; device never in frame |

Merge brief `avoid` list into `WHAT TO AVOID`.

---

## PRE-FLIGHT CHECKLIST

- [ ] Brief fields reflected in prompt — duration, shots, content, avoid
- [ ] `@Image` / `@Audio` order matches brief tags / CLI flag order
- [ ] Reference images tagged, not re-described
- [ ] Shot count and transitions match brief (`shots: 1` → no transition lines)
- [ ] Action and dialogue fit duration
- [ ] Plain text only — no markdown bold
- [ ] No filenames, registry keys, or local paths

---

## FINAL PRINCIPLES

**Translate the brief, don't rewrite it.** Brief `content` and `script` are authoritative.

**Respect the clock.** Cut before you add.

**Tags, not paths.** `@Image 1` in prompts; URLs in CLI only.

**This skill owns format.** Project skill owns creative briefs and workflow.

---

## Related

- [tft-cli-models](../tft-cli-models/SKILL.md) — `tft video-generate generate` commands
