---
name: the-kumar-method
description: >-
  Creates intro videos for The Kumar Method — 9:16 vertical speaking scenes with
  in-video voice (still camera, fast delivery), interstitial pose+music scenes
  (look-away to intense gaze, slow zoom), and a beat-synced tail montage. Uses
  GPT Image 2 for face-swapped reference images from templates, Seedance 2.0
  for video, parallel subagents for image generation, and an asset URL registry
  to avoid re-uploads. Use when working in video-03-thekumarmethod, generating
  scene docs, swagger pose images, Seedance prompts, or assembling the Kumar
  Method intro timeline. Use 'seedance2.0' skill for all Seedance video prompts
  (not tft create-prompt), plus 'tft-cli', 'tft-cli-models', and
  'tft-cli-video-editor' skills.
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
7. **Aspect ratio:** every image and video is **9:16** (vertical portrait). Pass `--aspect-ratio 9:16` on all `tft image-generate` and `tft video-generate` commands unless the CLI defaults to it.
8. **Cinematic clarity:** every clip is a **clear cinematic shot** — sharp focus, clean composition, intentional lighting, no blur, grain overload, or muddy exposure.
9. **No Python orchestration.** Do not write Python scripts to batch-generate assets. Use **parallel Cursor subagents** (Task tool) to generate images concurrently.
10. **Image prompt tags.** GPT Image 2 prompts use `@Image 1`, `@Image 2` — never local paths or filenames. Video prompt formatting is handled entirely by the seedance2.0 skill.
11. **Seedance prompts via skill, not CLI.** Do **not** run `tft video-generate create-prompt`. For each scene, read the **Seedance scene brief** (below + `scene.md`), then follow [`.cursor/skills/seedance2.0/SKILL.md`](.cursor/skills/seedance2.0/SKILL.md) to write `prompts/seedance_prompt_v01.txt`. Pass that file to `tft video-generate generate --prompt`.

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
| 006 | pose_music | interstitial | invent swagger pose (luxury object setting) | 3 s |
| 007 | speaking | "They will create stories…" | invent swagger pose (speaking style) | ~12 s |
| 008 | pose_music | interstitial | invent swagger pose (luxury object setting) | 3 s |
| 009 | speaking | "It will become irrelevant." | invent swagger pose (speaking style) | ~3 s |
| 010 | tail | beat-sync montage | `tail_01.png`–`tail_06.png` | 13 s |

**Script parsing:** Read [`script.md`](script.md). Text before the first `---` and each block after `---` is one speaking scene. Insert a `pose_music` scene after every speaking scene except none before 001. Append one `tail` scene at the end.

**Duration:**
- Speaking: ~1.7 s per short sentence; count syllables. Minimum **3 s** per clip. Delivery is **fast** — subject speaks briskly; still locked camera.
- Pose: **3 s** (`--duration 3`). **Second 0–1:** subject starts looking away, turns to intense camera gaze, camera slowly zooms to face; luxury setting object visible; `repeatable-music.mp3` synced to beat. **Seconds 1–3:** fade to pure white and silence — music and motion stop; hold white through end of clip. Each pose scene uses a unique pose library ID and unique setting object.
- Tail: **13 s** — matches `showcase-tail.mp3` exactly (`--duration 13`). **One video only** — all six tail poses live in a single montage clip; pose changes sync to music downbeats, not separate videos per pose.

---

## Visual style bible

Extract and reuse these styles in every scene doc and prompt.

### Global video look

- **Aspect ratio:** 9:16 vertical portrait for every image and video
- **Cinematic clarity:** sharp, clean, high-contrast cinematic framing on every clip — no soft focus, no handheld shake, no muddy lighting

### Speaking look (office / thought-leader)

- MCU, seated at desk, direct eye contact, steepled hands
- Black ribbed turtleneck; dramatic low-key key light on face
- Background (default): vintage US wall map, Steve Jobs B&W portrait, desk lamp, keyboard, phone
- **Camera:** locked tripod — **still shot** throughout; no pan, tilt, dolly, or orbit
- **Delivery:** subject speaks **fast** — brisk, confident pace; dialogue must fit duration without dragging
- On-screen text: bold red sans-serif
  - Scene 001 only: words append **in front of** chest (start = first word only; end = full sentence)
  - Scenes 003–009: words appear **in the background behind** the subject — voiceover script revealed **one word at a time**, each word syncing exactly with the spoken line in the video (reference image = final full-line layout)

### Pose look (luxury swagger)

- High-contrast rim-lit cinematic portrait in a **luxury object setting** — each pose scene features a distinct prop or environment (e.g. leather couch, front of expensive car, private jet seat, penthouse balcony)
- Black ribbed turtleneck; contemplative power poses; subject integrated with the setting object, not floating on a plain background
- **Performance arc (every pose clip):** subject **starts looking away from camera** (profile, over-shoulder, or downward gaze) → **turns to face camera** with **confident, intense eye contact** → **camera slowly zooms in** to a tight face MCU by end of clip
- **Pose uniqueness:** each pose scene must use a **different pose area** (head tilt zone, hand placement, body angle, shoulder line) — never repeat the same pose composition in two scenes; pick from the pose shot library below
- **Setting uniqueness:** each pose scene must use a **different setting object** — never repeat the same couch, car, or environment across the video; assign one setting per `pose_library_id`

### Tail look

- Same luxury swagger style as pose scenes
- **Single generated video** — all six tail poses in one montage clip, not one video per pose
- Beat-synced pose changes; flickering rim light or background edge to sync with music
- Six distinct swagger poses across storyboard frames; each change lands on a downbeat of `showcase-tail.mp3`
- **`tail_03` stacked reveal:** `tpl_tail_03.png` is a **three-panel vertical stack** (top: intense eye close-up; middle: hands fanning cash; bottom: polished dress shoe). In the montage, when the `tail_03` beat hits, the three panels **appear one by one** — top panel first, then middle, then bottom — each on successive downbeats within that storyboard cell. The generated `tail_frame_03` image must preserve all three stacked panels; the video animates them revealing sequentially, not all at once.

### Identity swap rules (all generated images)

- **Face, hair, facial hair** from `my-image/my-image.png`
- **Skin tone:** match medium-brown from `my-image`
- **Lock from template:** pose, wardrobe silhouette, framing, lighting style, background (unless user overrides)
- **Change only:** face and skin tone

### Swagger metadata (include in every scene doc)

```yaml
swagger_look: direct eye contact with camera, calm confident authority, no smirk
pose_lock: exact body pose from template — do not alter limbs or framing
pose_library_id: P0N  # pose scenes only — one unique ID per pose scene
pose_setting: [luxury object from library — e.g. leather couch, front of expensive car]
background_policy: preserve template background unless user specifies override; invented poses use pose library setting
skin_tone_match: medium-brown; match subject reference (@Image 2 in prompts)
aspect_ratio: 9:16
camera_style: clear cinematic shot; speaking = still tripod; pose = slow zoom to face
speaking_delivery: fast brisk pace
```

### Pose shot library (pick one per pose scene — all unique)

Assign **one library entry per pose scene** (002, 004, 006, 008). No two scenes in the same video may share the same `pose_area` or the same **setting object**. When inventing swagger poses for scenes without templates, choose an unused library entry.

| ID | Setting object | Pose area | Start gaze | Body / pose | End frame |
|----|----------------|-----------|------------|-------------|-----------|
| P01 | deep leather couch, lounge pose | chin + right hand | looking down-left, away from lens | seated on couch, right hand on chin, elbow on armrest | intense direct gaze, slow zoom to face |
| P02 | front of expensive sports car (hood/grille, night bokeh) | clasped hands at chest | over-right-shoulder, away from lens | standing at car front, hands clasped at sternum | turns to camera, slow zoom to face |
| P03 | private jet cabin seat | left profile + jaw | full left profile, gaze off-frame left | seated in jet seat, jaw set, neck long, rim light on cheekbone | snaps to camera, slow zoom to face |
| P04 | penthouse balcony railing, city skyline | standing lean + crossed arms | chin tucked, eyes down | leaning on railing, arms crossed high on chest | lifts chin to camera, slow zoom to face |
| P05 | designer armchair in minimalist loft | hand on temple | eyes closed or looking up-right away | seated in armchair, right fingertips at temple | opens eyes to intense camera lock, slow zoom |
| P06 | rooftop terrace at dusk | over-shoulder back turn | back three-quarter to camera, head turned away | standing at terrace edge, one shoulder dominant | rotates to face camera, slow zoom to face |
| P07 | luxury home library, leather-bound shelves | steepled fingers low | gaze at book spine, away | seated in reading chair, fingertips steepled below chin | raises gaze to camera, slow zoom to face |
| P08 | wine cellar stone archway | arms behind back | looking up and away to ceiling-left | standing in archway, military stance, shoulders back | drops gaze to intense camera lock, slow zoom |
| P09 | poolside lounge chair, twilight water | single hand on collar | looking off-frame right | reclined on lounge chair, hand adjusting turtleneck collar | hand drops, fierce direct gaze, slow zoom |
| P10 | executive corner office, floor-to-ceiling windows | seated forward + forearms on desk | head turned away right, profile | forearms on mahogany desk, city view behind | pivots head to camera, slow zoom to tight MCU |

**Selection rule:** for a 4-pose video (002, 004, 006, 008), pick 4 distinct IDs (e.g. P01 couch, P02 car, P06 rooftop, P09 poolside). Record `pose_library_id` and `pose_setting` in each `scene.md`.

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
        │   └── seedance_prompt_v01.txt   # written via seedance2.0 skill — not tft create-prompt
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

Create `scenes/scene_NNN/scene.md` for each scene with pose description, `pose_setting`, swagger metadata, image spec, video spec, registry key references, and a `## Seedance brief` block (see **Seedance scene briefs**).

### Step 2 — Reference images (GPT Image 2) — parallel generation

Resolve URLs from registry: `subject_my_image` + relevant `tpl_*`. Do not re-upload sources.

**Generate all images in parallel** — do not serialize scene-by-scene. Launch multiple Cursor subagents (Task tool) at once, one batch per independent image job. Do **not** write Python scripts or shell loops to orchestrate generation.

**Parallel batch plan (launch all subagents in one turn):**

| Subagent | Images to generate |
|----------|-------------------|
| Agent A | Scene 001: `start_v01`, `end_v01` |
| Agent B | Scene 003: `reference_v01` |
| Agent C | Scene 005: `reference_v01` |
| Agent D | Scene 007: `reference_v01` |
| Agent E | Scene 009: `reference_v01` |
| Agent F | Scene 002: `reference_v01` (pose library ID) |
| Agent G | Scene 004: `reference_v01` (pose library ID) |
| Agent H | Scene 006: `reference_v01` (pose library ID) |
| Agent I | Scene 008: `reference_v01` (pose library ID) |
| Agent J | Scene 010: `tail_frame_01_v01`–`tail_frame_06_v01` + storyboard |

Each subagent: run `tft image-generate`, save locally, upload once, register in `production.md` + `registry.json`. Parent agent waits for all subagents, then verifies registry completeness before Step 3.

```bash
tft image-generate generate \
  --model gpt-image-2 \
  --aspect-ratio 9:16 \
  --input-image TPL_URL \
  --input-image SUBJECT_URL \
  --prompt "PROMPT"
```

**Image prompt template:**

```
9:16 vertical portrait. Same pose, framing, lighting, wardrobe, and background as @Image 1.
Replace face with subject from @Image 2. Match medium-brown skin tone from @Image 2.
Clear cinematic shot, sharp focus, clean composition.
Direct eye contact with camera, calm swagger authority.
Do not change body pose, limb positions, or camera framing.
[USER BACKGROUND OVERRIDE if specified]
```

**`@Image` assignment — image generation (GPT Image 2):**

| Flag order | Tag | Role |
|------------|-----|------|
| 1st `--input-image` | `@Image 1` | Template / style / pose reference |
| 2nd `--input-image` | `@Image 2` | Subject identity (face, hair, skin tone) |

Video `@Image` / `@Audio` assignment lives in **Seedance scene briefs** — seedance2.0 skill maps brief tags to prompt text.

After each generated image: save locally, upload once, register as `scene_NNN_<role>_v01`.

**Scene 001:** generate `start_v01` (first word on chest) and `end_v01` (full sentence) from `tpl_speaking_01_start` / `tpl_speaking_01_end`.

**Scenes 003–009:** generate `reference_v01` from assigned template or invented swagger pose. Reference image shows **final background text layout** (full script line behind subject) for speaking scenes 003+.

**Pose scenes 002, 004, 006, 008:** generate `reference_v01` from template or pose library entry — include the **luxury setting object** (couch, car front, etc.) from `pose_setting`; image captures **end state** (intense direct gaze, pose locked, setting visible, ready for slow zoom).

**Scene 010 tail:** generate 6 frames from `tpl_tail_01`–`tpl_tail_06`; compose 2×3 storyboard grid; save `tail_frame_01_v01` separately. **`tail_frame_03`:** preserve the three-panel vertical stack from `tpl_tail_03` (eye close-up / cash hands / dress shoe) — all three panels visible in the reference image; video will reveal them one by one.

**Missing template:** invent a new swagger pose in the same style — speaking scenes use office look; pose scenes use **luxury object setting** from an unused pose library ID (couch, car, jet, etc.); maintain rim-light, black turtleneck, 9:16 framing.

### Step 3 — Video (Seedance 2.0)

**Prompts:** Read the scene's **Seedance scene brief** (section below + `scenes/scene_NNN/scene.md`). Hand off to [seedance2.0 skill](.cursor/skills/seedance2.0/SKILL.md) to produce `prompts/seedance_prompt_v01.txt`. Do not write the final prompt format in this file — seedance2.0 owns structure, camera language, formatting, and checklist.

**Generation:** [`tft-cli-models`](.cursor/skills/tft-cli-models/SKILL.md) for `tft video-generate generate` only.

| Scene type | Model | Registry inputs | Audio |
|------------|-------|-----------------|-------|
| 001 speaking | `seedance-2.0-image-to-video` | `scene_001_start_v01`, `scene_001_end_v01` | `--generate-audio` |
| 003–009 speaking | `seedance-2.0-reference-to-video` | `scene_NNN_reference_v01` | `--generate-audio` |
| 002–008 pose | `seedance-2.0-reference-to-video` | `scene_NNN_reference_v01`, `audio_repeatable_music` | `--no-generate-audio` |
| 010 tail | `seedance-2.0-reference-to-video` | `scene_010_tail_frame_01_v01`, `scene_010_tail_storyboard_v01`, `audio_showcase_tail` | `--no-generate-audio` |

Per scene:

1. Gather creative inputs from `scene.md` and the matching brief row below.
2. Read seedance2.0 skill → write `prompts/seedance_prompt_v01.txt`.
3. Run `tft video-generate generate` with registry URLs and `--prompt "$(cat …/seedance_prompt_v01.txt)"`.

```bash
# Scene 001 — start/end interpolation
tft video-generate generate \
  --model seedance-2.0-image-to-video \
  --aspect-ratio 9:16 \
  --image START_URL --last-frame END_URL \
  --prompt "$(cat scenes/scene_001/prompts/seedance_prompt_v01.txt)" --duration N

# Speaking 003+ / pose / tail — reference to video
tft video-generate generate \
  --model seedance-2.0-reference-to-video \
  --aspect-ratio 9:16 \
  --reference-image REF_URL \
  [--reference-audio AUDIO_URL] \
  [--no-generate-audio] \
  --prompt "$(cat scenes/scene_NNN/prompts/seedance_prompt_v01.txt)" --duration N
```

After each video: save locally, upload once, register as `scene_NNN_video_v01`.

### Step 4 — Timeline assembly

Use `tft-cli-video-editor` skill. Alternate speaking clips (embedded voice) and pose clips (music in first second, then white/silent tail) with **no overlap**. One tail montage clip last, 13 s. All alternating pose scenes should be trimed to 1 second.

---

## Per-scene playbooks

Creative specs for each scene type. Record these in `scene.md`; seedance2.0 skill turns them into the final prompt.

### Speaking 001 (start/end I2V)

| Field | Value |
|-------|-------|
| Images | `start_v01` = first word on chest; `end_v01` = full script line |
| Script | exact line from `script.md` |
| Text | foreground chest, word-by-word synced to speech |
| Camera | locked still tripod |
| Delivery | fast brisk pace |
| Audio | `--generate-audio` |
| Note | only speaking scene with foreground chest text |

### Speaking 003+ (reference to video)

| Field | Value |
|-------|-------|
| Image | `reference_v01` = final background text layout behind subject |
| Script | exact line from `script.md` |
| Text | background red sans-serif, one word at a time synced to voiceover |
| Camera | locked still tripod |
| Delivery | fast brisk pace |
| Audio | `--generate-audio` |

### Pose + music (002, 004, 006, 008)

| Field | Value |
|-------|-------|
| Image | `reference_v01` end-state intense gaze; setting object visible |
| Pose | unique `pose_library_id` + `pose_setting` per scene |
| Beat 0:00–0:01 | look away → turn to intense gaze → slow zoom; music on beat |
| Beat 0:01–0:03 | fade to pure white; audio silence; hold white |
| Dialogue | none |
| Audio | `@Audio 1` = repeatable music; `--no-generate-audio`; `--duration 3` |

### Tail 010

| Field | Value |
|-------|-------|
| Images | 6 tail frames + 2×3 storyboard + separate `tail_frame_01_v01` |
| tail_03 | three stacked panels in reference; reveal top → middle → bottom on successive downbeats |
| Video | one 13 s montage clip — not six separate videos |
| Inputs | first tail frame + storyboard + showcase tail audio |
| Motion | pose change per storyboard cell on downbeats; rim-light flicker on beat |
| Dialogue | none; do not transcribe lyrics |
| Audio | `@Audio 1` = showcase tail; `--no-generate-audio`; `--duration 13` |

---

## Seedance scene briefs

Content-only inputs for the seedance2.0 skill. Include a `## Seedance brief` block in each `scene.md` using these fields. Do **not** write FORMAT/SHOT structure here.

### Tag assignment (pass to seedance brief)

| Scene type | `@Image 1` | `@Image 2` | `@Audio 1` |
|------------|------------|------------|------------|
| 001 speaking I2V | Start frame (`--image`) | — | — |
| 003–009 speaking | Reference frame | — | — |
| 002–008 pose | Reference frame | — | Repeatable music |
| 010 tail | First tail frame | Storyboard grid | Showcase tail music |

### Brief — speaking 001

```yaml
type: speaking_i2v
duration: ~5
shots: 1
aspect_ratio: 9:16
script: "[exact line from script.md]"
tags: { image_1: start frame }
audio: generate_in_video
content:
  - MCU seated desk, steepled hands, office thought-leader look
  - red sans-serif text on chest, word-by-word from first word to full line, synced to speech
  - locked tripod, fast brisk delivery, direct swagger eye contact
avoid: duplicate characters, pose drift, background music, camera movement
```

### Brief — speaking 003+

```yaml
type: speaking_ref
duration: [from syllable count, min 3]
shots: 1
aspect_ratio: 9:16
script: "[exact line from script.md]"
tags: { image_1: reference frame }
audio: generate_in_video
content:
  - MCU locked tripod, fast brisk delivery
  - red sans-serif text in background behind subject, one word at a time synced to voiceover
  - final text layout matches reference image
avoid: foreground chest text, camera movement, slow delivery
```

### Brief — pose + music

```yaml
type: pose_music
duration: 3
shots: 1
aspect_ratio: 9:16
tags: { image_1: reference frame, audio_1: repeatable music }
audio: reference_only  # --no-generate-audio
pose_library_id: P0N
pose_setting: "[luxury object from library]"
content:
  - 0:00-0:01: start gaze away per pose library → turn to intense eye contact → slow zoom to face; music on beat; rim light pulse; setting visible
  - 0:01-0:03: fade to pure white, audio silence, hold white
avoid: dialogue, music after 0:01, repeated pose/setting across video
```

### Brief — tail montage

```yaml
type: tail_montage
duration: 13
shots: 1
aspect_ratio: 9:16
tags: { image_1: tail frame 01, image_2: storyboard, audio_1: showcase tail }
audio: reference_only  # --no-generate-audio
content:
  - single continuous montage, six swagger poses from storyboard, pose change on each downbeat
  - tail_03 cell: three stacked panels reveal top → middle → bottom on successive downbeats
  - rim light / background edge flicker on beat
avoid: dialogue, lyric transcription, separate clips per pose, tail_03 panels all at once
```

---

## Image prompt templates

All image prompts use `@Image N` tags only — never local paths or filenames.

### GPT Image 2 — face swap (speaking)

```
9:16 vertical portrait. Clear cinematic shot, sharp focus.
Same pose, framing, lighting, wardrobe, and background as @Image 1.
Replace face with subject from @Image 2: medium-brown skin, dark hair with voluminous quiff,
mustache and pointed goatee, oval face, direct confident gaze.
Seated at desk, steepled hands at chest, black ribbed turtleneck.
Bold red sans-serif text: "[FULL SCRIPT LINE or FIRST WORD ONLY]"
  - Scene 001 start/end: text on chest in foreground
  - Scenes 003+: full script line in background behind subject (reference = final word layout)
Do not change body pose or camera framing.
```

### GPT Image 2 — pose (face swap)

```
9:16 vertical portrait. Clear cinematic shot, sharp focus.
Same pose, framing, rim lighting, and composition as @Image 1.
Replace face with subject from @Image 2: medium-brown skin, dark hair with quiff,
mustache and goatee. End-state: intense direct eye contact with camera, confident authority.
Black ribbed turtleneck.
Pose library [P0N]: [pose area from library table].
Setting: [luxury object from library — e.g. deep leather couch, front of expensive sports car,
private jet seat, penthouse balcony]. Subject integrated with setting, visible in frame.
High-contrast rim-lit cinematic environment, not plain background.
Do not change body pose, limb positions, or camera framing.
```

### GPT Image 2 — tail frame

```
9:16 vertical portrait. Clear cinematic shot, sharp focus.
Same pose, framing, rim lighting, and composition as @Image 1.
Replace face with subject from @Image 2. Match skin tone from @Image 2.
High-contrast cinematic portrait.
Pose: [describe visible pose and framing from @Image 1].

For third tail frame only (three-panel vertical stack in @Image 1):
  top panel: extreme close-up intense eyes;
  middle panel: hands fanning hundred-dollar bills;
  bottom panel: polished black dress shoe on floor.
All three panels visible in final reference image (stacked layout).
```

---

## Worked examples

### Scene 001

| Field | Value |
|-------|-------|
| Duration | ~5 s |
| Type | speaking |
| Aspect ratio | 9:16 vertical |
| Template | `tpl_speaking_01_start`, `tpl_speaking_01_end` |
| Start image | Red text "This" on chest (foreground) |
| End image | Full line on chest (foreground) |
| Seedance | I2V start→end, still camera, fast delivery, `--aspect-ratio 9:16`, `--generate-audio`, word-by-word chest text synced to speech |
| Registry outputs | `scene_001_start_v01`, `scene_001_end_v01`, `scene_001_video_v01` |
| Swagger | seated desk, steepled fingers, direct gaze, authority |

### Scene 010 (tail)

| Field | Value |
|-------|-------|
| Duration | 13 s (`showcase-tail.mp3`) |
| Type | tail |
| Templates | `tpl_tail_01`–`tpl_tail_06` |
| Images | 6 face-swapped frames, 2×3 storyboard, separate frame 01 |
| `tail_03` | Three-panel vertical stack in reference image; video reveals top → middle → bottom one by one on successive downbeats |
| Seedance | **One** ref-to-video montage (13 s) with frame 01 + storyboard + tail audio — all six poses in a single clip |
| Effects | rim-light flicker on beat, pose change per storyboard cell on downbeats; tail_03 stacked panel sequential reveal |
| Registry outputs | `scene_010_tail_frame_01_v01`, `scene_010_tail_frame_02_v01` … `_06`, `scene_010_tail_storyboard_v01`, `scene_010_video_v01` |

### Pose scene (002, 004, 006, 008)

| Field | Value |
|-------|-------|
| Duration | 3 s (`--duration 3`) |
| Type | pose_music |
| Aspect ratio | 9:16 vertical |
| Pose library | one unique `pose_library_id` (P01–P10) per scene — no repeated pose areas or setting objects |
| Setting | luxury object per library (e.g. P01 = leather couch, P02 = front of expensive car) |
| Performance | start looking away → turn to intense camera gaze → slow zoom to face |
| Beat structure | 0:00–0:01 look-away arc + music + zoom; 0:01–0:03 fade to white + silence |
| Seedance | ref-to-video with reference image + repeatable music, `--no-generate-audio` |
| Registry outputs | `scene_NNN_reference_v01`, `scene_NNN_video_v01` |

---

## Related skills

- [seedance2.0](.cursor/skills/seedance2.0/SKILL.md) — final Seedance prompt generation from scene briefs
- [tft-cli-models](.cursor/skills/tft-cli-models/SKILL.md) — image-generate, video-generate generate, file upload
- [tft-cli-video-editor](.cursor/skills/tft-cli-video-editor/SKILL.md) — timeline assembly

---

## Checklist

- [ ] Read `script.md`; do not edit unless user requests
- [ ] `script.md` is non-empty before processing
- [ ] Source assets uploaded and registered in `production.md` + `registry.json` during script parse
- [ ] `scene-doc.md` and `scenes/scene_NNN/` created from script parse
- [ ] Per-scene `scene.md` with swagger metadata, `pose_library_id` + `pose_setting` (pose scenes), and registry cross-refs
- [ ] All GPT Image 2 references generated **in parallel via subagents** (no Python scripts); URLs registered (no duplicate uploads)
- [ ] Each `scene.md` includes a `## Seedance brief` block per **Seedance scene briefs** section
- [ ] `seedance_prompt_v01.txt` written via **seedance2.0 skill** only (not `tft create-prompt`)
- [ ] All GPT Image 2 prompts use `@Image N` only — no local paths or filenames
- [ ] Every image and video is **9:16** and a **clear cinematic shot**
- [ ] Pose clips: unique pose library ID + luxury setting object per scene (couch, car, etc.); look-away → intense gaze → slow zoom; music in 0:00–0:01, fade to white + silence 0:01–0:03
- [ ] Tail = one 13 s montage with all six poses beat-synced; not separate videos per pose; `tail_03` three stacked panels reveal one by one (top → middle → bottom)
- [ ] Seedance videos generated with correct model, `--aspect-ratio 9:16`, and audio flags per scene type
- [ ] Speaking = in-video voice; pose/tail = reference music only; no overlap on timeline
- [ ] All generated assets have local path + remote URL in registry
- [ ] Timeline assembled in scene order
