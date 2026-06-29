---
name: the-kumar-method
description: >-
  Creates intro videos for The Kumar Method — speaking scenes with in-video
  voice, interstitial pose+music scenes, and a beat-synced tail montage. Uses
  GPT Image 2 for face-swapped reference images from templates, Seedance 2.0
  for video, and an asset URL registry to avoid re-uploads. Use when working
  in video-03-thekumarmethod, generating scene docs, swagger pose images,
  Seedance prompts, or assembling the Kumar Method intro timeline. Use 'tft-cli' and 'tft-cli-models' and 'tft-cli-video-editor' skills.
---

# The Kumar Method — Intro Video Skill

Creates an intro video for the person in `my-image/` with in-video voiceover and background music. Voice and music **never overlap** on the timeline.

---

## Hard constraints

1. **Never edit `script.md`** unless the user explicitly requests it.
2. **Never edit files in `templates/`** — read-only pose/style references.
3. **No separate TTS.** Voice is generated inside Seedance video clips (`--generate-audio`). Do not call `tft audio-generate text-to-speech`.
4. **Upload once, reuse URLs.** Look up [`production.md`](production.md) before every upload. Pass registry URLs to TFT — never local paths.
5. **Audio separation:** speaking clips = voice only; pose clips = `repeatable-music.mp3` only; tail = `showcase-tail.mp3` only.
6. **Minimum clip length:** every Seedance video must be **≥ 3 s** (`--duration 3` minimum).

---

## Video structure

```
Speaking 001 → Pose+Music 002 → Speaking 003 → Pose+Music 004 → Speaking 005
→ Pose+Music 006 → Speaking 007 → Pose+Music 008 → Speaking 009 → Tail 010
```

| Scene | Type | Script / purpose | Template |
|------|------|------------------|----------|
| 001 | speaking | "This is a message to every legacy production house." | `speaking_01_start.png` + `speaking_01_end.png` | ~5 s |
| 002 | pose_music | interstitial | `pose_01_start.png` | 3 s |
| 003 | speaking | "My name is Mohammad Saquib. I'm an AI engineer." | `speaking_02_reference.png` | ~6 s |
| 004 | pose_music | interstitial | `pose_02_reference.png` | 3 s |
| 005 | speaking | "And I'm building a product…" | invent swagger pose (speaking style) | ~10 s |
| 006 | pose_music | interstitial | invent swagger pose (silhouette style) | 3 s |
| 007 | speaking | "They will create stories…" | invent swagger pose (speaking style) | ~12 s |
| 008 | pose_music | interstitial | invent swagger pose (silhouette style) | 3 s |
| 009 | speaking | "It will become irrelevant." | invent swagger pose (speaking style) | ~3 s |
| 010 | tail | beat-sync montage | `tail_01.png`–`tail_06.png` | 13 s |

**Script parsing:** Read [`script.md`](script.md). Text before the first `---` and each block after `---` is one speaking scene. Insert a `pose_music` scene after every speaking scene except none before 001. Append one `tail` scene at the end.

**Duration:**
- Speaking: ~2.5 s per short sentence; count syllables (see seedance2.0 dialogue math). Minimum **3 s** per clip.
- Pose: **3 s** (`--duration 3`). **Second 0–1:** subject holds swagger pose with `repeatable-music.mp3` synced to the beat. **Seconds 1–3:** fade to pure white and silence — music and motion stop; hold white through end of clip.
- Tail: **13 s** — matches `showcase-tail.mp3` exactly (`--duration 13`). **One video only** — all six tail poses live in a single montage clip; pose changes sync to music downbeats, not separate videos per pose.

---

## Visual style bible

Extract and reuse these styles in every scene doc and prompt.

### Speaking look (office / thought-leader)

- MCU, seated at desk, direct eye contact, steepled hands
- Black ribbed turtleneck; dramatic low-key key light on face
- Background (default): vintage US wall map, Steve Jobs B&W portrait, desk lamp, keyboard, phone
- On-screen text: bold red sans-serif
  - Scene 001: words append **in front of** chest (start = first word only; end = full sentence)
  - Scenes 003+: words appear **in background** behind subject, word-by-word animation in video

### Pose look (silhouette swagger)

- High-contrast rim-lit portrait on plain off-white background
- Black ribbed turtleneck; contemplative power poses (hand to chin, clasped hands, over-shoulder glance)
- Subject always looks at camera with calm authority

### Tail look

- Same silhouette swagger style as pose scenes
- **Single generated video** — all six tail poses in one montage clip, not one video per pose
- Beat-synced pose changes; flickering rim light or background edge to sync with music
- Six distinct swagger poses across storyboard frames; each change lands on a downbeat of `showcase-tail.mp3`

### Identity swap rules (all generated images)

- **Face, hair, facial hair** from `my-image/my-image.png`
- **Skin tone:** match medium-brown from `my-image`
- **Lock from template:** pose, wardrobe silhouette, framing, lighting style, background (unless user overrides)
- **Change only:** face and skin tone

### Swagger metadata (include in every scene doc)

```yaml
swagger_look: direct eye contact with camera, calm confident authority, no smirk
pose_lock: exact body pose from template — do not alter limbs or framing
background_policy: preserve template background unless user specifies override
skin_tone_match: medium-brown from my-image
```

---

## Folder structure

```
video-03-thekumarmethod/
├── SKILL.md
├── script.md                 # READ ONLY unless user requests edit
├── scene-doc.md              # master scene plan (generated)
├── production.md             # asset URL registry only
├── assets/
│   └── registry.json         # JSON mirror of production.md URLs
├── my-image/my-image.png
├── audio/
│   ├── repeatable-music.mp3
│   └── showcase-tail.mp3
├── templates/                # READ ONLY
└── scenes/
    └── scene_NNN/
        ├── scene.md
        ├── images/
        │   ├── reference_v01.png
        │   ├── start_v01.png       # scene 001 only
        │   ├── end_v01.png         # scene 001 only
        │   └── image_prompt_v01.txt
        ├── prompts/
        │   ├── seedance_prompt_v01.txt
        │   └── seedance_brief.txt
        ├── storyboards/            # tail scene only
        │   ├── tail_storyboard_v01.png
        │   └── tail_frame_01_v01.png
        └── output/
            └── scene_NNN_v01.mp4
```

### Asset key naming

| Prefix | Example | Use |
|--------|---------|-----|
| `subject_*` | `subject_my_image` | Source subject photo |
| `audio_*` | `audio_repeatable_music` | Source audio |
| `tpl_*` | `tpl_speaking_01_start` | Template images |
| `scene_NNN_*_vNN` | `scene_001_start_v01` | Generated images |
| `scene_NNN_video_vNN` | `scene_001_video_v01` | Generated videos |

Roles for generated images: `reference`, `start`, `end`, `tail_frame_NN`, `tail_storyboard`.

---

## Asset URL registry

Every uploaded file is recorded in [`production.md`](production.md) and [`assets/registry.json`](assets/registry.json). Both start empty — source and generated asset rows are added when `script.md` is processed. No scene list in `production.md`.

### Upload-once workflow

1. **Resolve:** Look up asset key in `production.md`. If `Remote URL` is set and `Status` is `approved`, use it — do not re-upload.
2. **Upload if missing:** `tft files upload --file <local path>` → write URL to registry immediately.
3. **Re-upload only when:** file regenerated (new `_v02` suffix) or user explicitly requests refresh.
4. **Generation commands:** Pass registry URLs to `--input-image`, `--reference-image`, `--image`, `--last-frame`, `--reference-audio`.
5. **Scene cross-ref:** Each `scene.md` lists registry keys consumed, e.g. `inputs: scene_001_start_v01, scene_001_end_v01`.

### Source assets required per script (registered during Step 1)

When processing a script, discover and upload only the sources needed for that run:

| Asset key | Local path | When needed |
|-----------|------------|-------------|
| `subject_my_image` | `my-image/my-image.png` | always |
| `audio_repeatable_music` | `audio/repeatable-music.mp3` | pose scenes (music in first 1 s of 3 s clip) |
| `audio_showcase_tail` | `audio/showcase-tail.mp3` | tail scene (13 s) |
| `tpl_*` | `templates/<file>.png` | per scene template assignment |

Upload each missing key, then append a row to Source Asset Registry in `production.md` and sync `registry.json` before image or video generation.

### Registry tables (in production.md — populated at runtime)

```markdown
## Source Asset Registry

| Asset key | Local path | Remote URL | Uploaded | Status |

## Generated Image Registry

| Asset key | Scene | Local path | Remote URL | Source inputs | Status |

## Generated Video Registry

| Asset key | Scene | Local path | Remote URL | Inputs used | Status |
```

---

## Workflow

### Step 1 — Parse script → scene-doc.md + source assets

**Only when `script.md` is non-empty.** If the script has no speaking lines, stop and ask the user to add content.

1. Parse `script.md` — speaking blocks, interstitial pose scenes, tail scene.
2. Assign templates per scene; list required `tpl_*` keys for this script.
3. **Register source assets:** upload `subject_my_image`, both audio files, and each required template. Append rows to Source Asset Registry in `production.md`; sync `registry.json`. Reuse existing URLs — do not re-upload.
4. Create [`scene-doc.md`](scene-doc.md) with scene index and `scenes/scene_NNN/scene.md` per scene.

Scene planning and source asset registration both happen here — **not** pre-listed in `production.md`.

```markdown
# Scene Document — The Kumar Method Intro

## Project metadata
- Subject: my-image
- Background: [user override | default from template]
- Visual style: speaking | pose | tail
- Swagger: direct camera eye contact, confident authority, no smirk
- Voice: native in-video (Seedance --generate-audio); no separate TTS

## Scene index
| # | Type | Duration | Script line | Audio | Seedance model | Template | Registry inputs |
```

Create `scenes/scene_NNN/scene.md` for each scene with pose description, swagger metadata, image spec, video spec, and registry key references.

### Step 2 — Reference images (GPT Image 2)

Resolve URLs from registry: `subject_my_image` + relevant `tpl_*`. Do not re-upload sources.

```bash
tft image-generate generate \
  --model gpt-image-2 \
  --input-image TPL_URL \
  --input-image SUBJECT_URL \
  --prompt "PROMPT"
```

**Image prompt template:**

```
Same pose, framing, lighting, wardrobe, and background as @Image 1.
Replace face with subject from @Image 2. Match medium-brown skin tone.
Direct eye contact with camera, calm swagger authority.
Do not change body pose, limb positions, or camera framing.
[USER BACKGROUND OVERRIDE if specified]
```

After each generated image: save locally, upload once, register as `scene_NNN_<role>_v01`.

**Scene 001:** generate `start_v01` (first word on chest) and `end_v01` (full sentence) from `tpl_speaking_01_start` / `tpl_speaking_01_end`.

**Scenes 003–009:** generate `reference_v01` from assigned template or invented swagger pose.

**Scene 010 tail:** generate 6 frames from `tpl_tail_01`–`tpl_tail_06`; compose 2×3 storyboard grid; save `tail_frame_01_v01` separately.

**Missing template:** invent a new swagger pose in the same style — speaking scenes use office look; pose scenes use silhouette look; maintain rim-light, black turtleneck, direct camera gaze.

### Step 3 — Video (Seedance 2.0)

Follow [`.cursor/skills/seedance2.0/SKILL.md`](../../.cursor/skills/seedance2.0/SKILL.md) for prompt format. Use [`tft-cli-models`](../../.cursor/skills/tft-cli-models/SKILL.md) for commands.

| Scene type | Model | Registry inputs | Audio |
|------------|-------|-----------------|-------|
| 001 speaking | `seedance-2.0-image-to-video` | `scene_001_start_v01`, `scene_001_end_v01` | `--generate-audio` |
| 003–009 speaking | `seedance-2.0-reference-to-video` | `scene_NNN_reference_v01` | `--generate-audio` |
| 002–008 pose | `seedance-2.0-reference-to-video` | `scene_NNN_reference_v01`, `audio_repeatable_music` | `--no-generate-audio` |
| 010 tail | `seedance-2.0-reference-to-video` | `scene_010_tail_frame_01_v01`, `scene_010_tail_storyboard_v01`, `audio_showcase_tail` | `--no-generate-audio` |

```bash
# Scene 001 — start/end interpolation
tft video-generate create-prompt -m seedance-2.0-image-to-video -i "BRIEF"
tft video-generate generate \
  --model seedance-2.0-image-to-video \
  --image START_URL --last-frame END_URL \
  --prompt "PROMPT" --duration N

# Speaking 003+ / pose / tail — reference to video
tft video-generate create-prompt -m seedance-2.0-reference-to-video -i "BRIEF"
tft video-generate generate \
  --model seedance-2.0-reference-to-video \
  --reference-image REF_URL \
  [--reference-audio AUDIO_URL] \
  [--no-generate-audio] \
  --prompt "PROMPT" --duration N
```

After each video: save locally, upload once, register as `scene_NNN_video_v01`.

### Step 4 — Timeline assembly

Use `tft-cli-video-editor` skill. Alternate speaking clips (embedded voice) and pose clips (music in first second, then white/silent tail) with **no overlap**. One tail montage clip last, 13 s. All alternating pose scenes should be trimed to 1 second.

---

## Per-scene playbooks

### Speaking 001 (start/end I2V)

- **Images:** `start_v01` = first word only on chest; `end_v01` = full script line
- **Video:** interpolate start → end; word-by-word text animation in foreground
- **Voice:** dialogue inline — `@Image 1 speaks directly to camera: "This is a message to every legacy production house."`
- **Pose:** seated desk, steepled fingers, MCU, office background

### Speaking 003+ (reference to video)

- **Image:** `reference_v01` showing final word layout in background
- **Video:** word-by-word background text animation as subject speaks; reference image = final state
- **Voice:** exact script line as dialogue in shot prose

### Pose + music (002, 004, 006, 008)

- **Image:** `reference_v01` from pose template or invented silhouette swagger pose
- **Video:** **3 s** clip (`--duration 3`). **0:00–0:01:** subject holds swagger pose with subtle movement; `@Audio 1` (repeatable music) plays and drives the beat. **0:01–0:03:** fade to pure white; audio fades to silence; no motion — hold white through end.
- **No dialogue** in prompt; music only in the first second

### Tail 010

- **Images:** 6 frames + 2×3 storyboard grid + separate `tail_frame_01_v01`
- **Video:** **one 13 s montage** — generate a single clip, not six separate pose videos
- **Video inputs:** first frame + storyboard + showcase tail audio
- **Video prompt:** describe each of 6 storyboard frames; pose changes on downbeats synced to `@Audio 1`; flicker/strobe on rim light or background edge on beat; do not transcribe lyrics

---

## Structured prompt templates

### GPT Image 2 — face swap (speaking)

```
Same pose, framing, lighting, wardrobe, and background as the template reference.
Replace face with subject from my-image: medium-brown skin, dark hair with voluminous quiff,
mustache and pointed goatee, oval face, direct confident gaze.
Seated at desk, steepled hands at chest, black ribbed turtleneck.
Bold red sans-serif text: "[FULL SCRIPT LINE or FIRST WORD ONLY]" [foreground for 001 start / background for 003+].
Do not change body pose or camera framing.
```

### GPT Image 2 — face swap (pose silhouette)

```
Same pose, framing, rim lighting, and silhouette as the template reference.
Replace face with subject from my-image: medium-brown skin, dark hair with quiff,
mustache and goatee, direct eye contact with camera, calm swagger authority.
Black ribbed turtleneck, plain off-white background.
Do not change body pose, limb positions, or camera framing.
```

### GPT Image 2 — tail frame

```
Same over-shoulder swagger pose and rim-lit silhouette as tail template reference.
Replace face with subject from my-image. Match skin tone.
High-contrast cinematic portrait, plain bright background.
Pose [N]: [describe from tail_0N template — e.g. over-shoulder glance, hand to chin].
```

### Seedance 2.0 — speaking 001 (I2V, plain text)

```
FORMAT: [N]s / 1 SHOTS / Opening statement with word-by-word text reveal

PRIMARY CHARACTER: @Image 1.

SETTING: (@Image 1) office thought-leader environment

VISUAL STYLE: Dramatic low-key MCU, photorealistic, bold red sans-serif text overlay

CONTINUITY: Same wardrobe and face throughout. Only one @Image 1 in frame.

WHAT TO AVOID: duplicate characters, pose drift, background music

---

SHOT 1 — 0:00 to 0:0[N].
MCU, 50mm, locked tripod.
Opens on @Image 1 seated at desk, steepled hands. Red text on chest animates word by word from "[FIRST WORD]" to full line. @Image 1 speaks directly to camera: "This is a message to every legacy production house." Direct swagger eye contact throughout. End on full sentence visible.
```

Use `--image` = start URL, `--last-frame` = end URL, `--generate-audio`.

### Seedance 2.0 — speaking 003+ (ref to video)

```
FORMAT: [N]s / 1 SHOTS / Script delivery with background word reveal

PRIMARY CHARACTER: @Image 1.

SETTING: (@Image 1)

VISUAL STYLE: Dramatic low-key MCU, photorealistic, red sans-serif text in background

CONTINUITY: Match @Image 1 reference exactly. Text builds word by word in background behind subject.

---

SHOT 1 — 0:00 to 0:0[N].
MCU, 50mm, slow push-in.
@Image 1 speaks directly to camera: "[EXACT SCRIPT LINE]." Red background text animates word by word, syncing with speech, resolving to final layout matching @Image 1. Swagger direct gaze throughout.
```

Use `--reference-image` = reference URL, `--generate-audio`.

### Seedance 2.0 — pose + music

```
FORMAT: 3s / 1 SHOTS / Swagger pose then fade to white

PRIMARY CHARACTER: @Image 1.

SETTING: (@Image 1) minimalist rim-lit silhouette

SOUNDTRACK: @Audio 1 (first second only, then silence)

VISUAL STYLE: High-contrast rim light, photorealistic portrait

CONTINUITY: Same pose family as @Image 1. Only one subject in frame.

WHAT TO AVOID: dialogue, duplicate characters, music after 0:01

---

SHOT 1 — 0:00 to 0:03.
MS, 85mm, slow orbit.
0:00 to 0:01: @Image 1 holds swagger pose, direct eye contact with camera. Subtle confident micro-movements synced to rhythm of @Audio 1. Rim light pulses gently with the beat. No dialogue.
0:01 to 0:03: subject and rim light fade smoothly to pure white. @Audio 1 fades to silence. Hold solid white, no motion, no sound through 0:03.
```

Use `--reference-image` + `--reference-audio` (repeatable music), `--no-generate-audio`, `--duration 3`.

### Seedance 2.0 — tail montage

Single video only — all six poses in one 13 s clip. Do not generate separate videos per tail pose.

```
FORMAT: 13s / 1 SHOTS / Beat-synced swagger montage

PRIMARY CHARACTER: @Image 1.

SETTING: (@Image 1) (@Image 2)

SOUNDTRACK: @Audio 1

VISUAL STYLE: High-contrast rim-lit silhouette montage, flickering light accents on beat

CONTINUITY: Same subject identity across all six pose beats in @Image 2 storyboard. One continuous montage — pose change on each downbeat.

WHAT TO AVOID: dialogue, lyric transcription, separate clips per pose

---

SHOT 1 — 0:00 to 0:13.
WS to MS montage, 50mm, dynamic cuts motivated by beat.
@Image 1 cycles through six distinct swagger poses from @Image 2 storyboard — over-shoulder glance, hand to chin, clasped hands, profile rim-lit, forward lean, held hero frame. Each pose change lands on a downbeat of @Audio 1. Rim light and background edge flicker on beat. Direct camera eye contact in each pose. No dialogue.
```

Use `--reference-image` tail_frame_01 + storyboard + showcase tail audio, `--no-generate-audio`, `--duration 13`. Output: **one** `scene_010_video_v01` — not six pose clips.

---

## Worked examples

### Scene 001

| Field | Value |
|-------|-------|
| Duration | ~5 s |
| Type | speaking |
| Template | `tpl_speaking_01_start`, `tpl_speaking_01_end` |
| Start image | Red text "This" on chest |
| End image | Full line on chest |
| Seedance | I2V start→end, `--generate-audio`, word-by-word foreground text |
| Registry outputs | `scene_001_start_v01`, `scene_001_end_v01`, `scene_001_video_v01` |
| Swagger | seated desk, steepled fingers, direct gaze, authority |

### Scene 010 (tail)

| Field | Value |
|-------|-------|
| Duration | 13 s (`showcase-tail.mp3`) |
| Type | tail |
| Templates | `tpl_tail_01`–`tpl_tail_06` |
| Images | 6 face-swapped frames, 2×3 storyboard, separate frame 01 |
| Seedance | **One** ref-to-video montage (13 s) with frame 01 + storyboard + tail audio — all six poses in a single clip |
| Effects | rim-light flicker on beat, pose change per storyboard cell on downbeats |
| Registry outputs | `scene_010_tail_frame_01_v01`, `scene_010_tail_frame_02_v01` … `_06`, `scene_010_tail_storyboard_v01`, `scene_010_video_v01` |

### Pose scene (002, 004, 006, 008)

| Field | Value |
|-------|-------|
| Duration | 3 s (`--duration 3`) |
| Type | pose_music |
| Beat structure | 0:00–0:01 pose + `repeatable-music.mp3`; 0:01–0:03 fade to white + silence |
| Seedance | ref-to-video with reference image + repeatable music, `--no-generate-audio` |
| Registry outputs | `scene_NNN_reference_v01`, `scene_NNN_video_v01` |

---

## Related skills

- [seedance2.0](../../.cursor/skills/seedance2.0/SKILL.md) — cinematic prompt structure and dialogue math
- [tft-cli-models](../../.cursor/skills/tft-cli-models/SKILL.md) — image-generate, video-generate, file upload
- [tft-cli-video-editor](../../.cursor/skills/tft-cli-video-editor/SKILL.md) — timeline assembly

---

## Checklist

- [ ] Read `script.md`; do not edit unless user requests
- [ ] `script.md` is non-empty before processing
- [ ] Source assets uploaded and registered in `production.md` + `registry.json` during script parse
- [ ] `scene-doc.md` and `scenes/scene_NNN/` created from script parse
- [ ] Per-scene `scene.md` with swagger metadata and registry cross-refs
- [ ] GPT Image 2 references generated; URLs registered (no duplicate uploads)
- [ ] Seedance videos ≥ 3 s; pose clips = pose + music in 0:00–0:01, fade to white + silence 0:01–0:03
- [ ] Tail = one 13 s montage with all six poses beat-synced; not separate videos per pose
- [ ] Seedance videos generated with correct model and audio flags per scene type
- [ ] Speaking = in-video voice; pose/tail = reference music only; no overlap on timeline
- [ ] All generated assets have local path + remote URL in registry
- [ ] Timeline assembled in scene order
