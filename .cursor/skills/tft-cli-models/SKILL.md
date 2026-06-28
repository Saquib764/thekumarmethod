---
name: tft-cli-models
description: >-
  TheFluxTrain CLI commands for one-off image, video, motion, and audio
  generation. Covers image-generate, video-generate, motion-control, and
  audio-generate with all models, flags, and examples. Use when the creator
  wants to generate a single image, video, animation, voice, or audio file
  via tft without building a Flow Studio graph.
---

# tft — Models (Image, Video, Motion, Audio)

One-off generation commands. For file upload, media metadata, and job polling, see **tft-cli** skill.

**Upload rule:** Upload local files with `tft files upload --file <path>` first. Pass the returned URL to flags — never local paths.

**Async jobs:** Video and motion commands often return a job id. Poll with:
```bash
tft jobs check-status --editor-id JOB_ID
```

---

## Cross-cutting parameters

These flags appear on many generation commands:

| Flag | Purpose |
|------|---------|
| `--folder-id` | Organize output in a folder |
| `--project-id` | Link output to a project |
| `--message-id` | Your own tracking id |
| `--training-id` | Link to a training run (image LoRA workflows) |
| `--output json` / `--output yaml` | Structured response |

---

## Image generation (`tft image-generate`)

Create or edit images — text-to-image, reference images, inpainting, LoRA, cartoon styles, product composites.

### `generate` — Generate image with Flux and other models

**When to use:** Text-to-image, image-to-image, or inpainting with a mask.

**Requires:** At least one of `--prompt` or `--input-image`.

```bash
tft image-generate generate --prompt "A cat in space" --model flux-2-pro
tft image-generate generate --prompt "Same style portrait" --input-image UPLOAD_URL --aspect-ratio 16:9
tft image-generate generate --prompt "Replace the sky" --input-image UPLOAD_URL --mask MASK_URL --model flux-fill-pro
```

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` / `-p` | — | Text prompt (required if no input image) |
| `--input-image` | — | Reference image URL (repeatable) |
| `--mask` | — | Mask image URL for inpainting |
| `--model` / `-m` | `flux-2-pro` | Model: `flux-2-pro`, `nano-banana`, `nano-banana-2`, `flux-fill-pro`, `z-image-base`, `wan-2-7-pro`, `gpt-image-2` |
| `--resolution` | `2 MP` | e.g. `1 MP`, `2 MP` |
| `--aspect-ratio` | `1:1` | e.g. `16:9`, `9:16` |
| `--steps` | `50` | Inference steps |
| `--guidance` | `60.0` | Guidance scale |
| `--output-format` | `png` | `png` or `jpg` |
| `--output-quality` | `81` | 0–100 |
| `--quality` | — | Quality tier (e.g. for `gpt-image-2`) |
| `--safety-tolerance` | `2` | 0–5 |
| `--enable-web-search` / `--no-enable-web-search` | `false` | Web search for Nano Banana 2 |
| `--negative-prompt` | — | Content to avoid (WAN 2.7 Pro) |
| `--folder-id`, `--project-id`, `--training-id`, `--message-id` | — | Organization / tracking |

**Model picker:**

| Model | Best for |
|-------|----------|
| `flux-2-pro` | General high-quality text/reference images |
| `nano-banana-2` | Fast, cost-efficient iterations |
| `nano-banana` | Highest Nano-family fidelity |
| `flux-fill-pro` | Inpainting with mask |
| `z-image-base` | Pure text-to-image (no reference) |
| `wan-2-7-pro` | Reference images + negative prompt |
| `gpt-image-2` | OpenAI-style generation/inpainting |

---

### `lora` — Generate with trained LoRA models

**When to use:** Images in a custom-trained style or subject.

**Requires:** `--prompt`, `--lora` (repeatable), `--trainer-model`.

```bash
tft image-generate lora -p "ohwx person in a cafe" --lora your-org/your-lora --trainer-model flux2 --aspect-ratio 3:4
tft image-generate lora -p "styled portrait" --lora org/lora --trainer-model flux1 --image UPLOAD_URL --strength 0.9
```

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` / `-p` | required | Text prompt |
| `--lora` | required | LoRA identifier (HF repo id, repeatable) |
| `--trainer-model` | required | `flux1`, `flux2`, or `qwen_image` |
| `--lora-scale` | `1.0` | Scale per LoRA 0.0–2.0 (repeatable) |
| `--aspect-ratio` | `1:1` | Output aspect ratio |
| `--prompt-strength` | `0.8` | Prompt strength |
| `--num-outputs` | `1` | Number of images |
| `--num-inference-steps` | `28` | Inference steps |
| `--guidance-scale` | `3.5` | Guidance scale |
| `--output-format` | `png` | Output format |
| `--output-quality` | `80` | Output quality |
| `--image` | — | Reference image URL (img2img) |
| `--mask` | — | Mask image URL |
| `--seed` | — | Random seed |
| `--use-oyecartoon` / `--no-use-oyecartoon` | `false` | Oye-cartoon path |
| `--paste-reference` / `--no-paste-reference` | `false` | Paste reference image |
| `--strength` | `0.9` | Image-to-image strength |

---

### `cartoon-convert` — Photo to cartoon or character styles

**When to use:** Turn a photo into cartoon or themed character looks.

**Requires:** `--image`, `--action`.

```bash
tft files upload --file ./photo.jpg
tft image-generate cartoon-convert --image UPLOAD_URL --action cartoonify --gender female
tft image-generate cartoon-convert --image UPLOAD_URL --action superhero --gender male
```

| Flag | Default | Description |
|------|---------|-------------|
| `--image` | required | Source photo URL |
| `--action` | required | `cartoonify`, `plain`, `adventurer`, `knight`, `futuristic`, `schoolkid`, `superhero`, `spider-boy`, `spider-girl`, `super-boy`, `super-girl` |
| `--gender` | `male` | `male` or `female` (for compatible actions) |
| `--aspect-ratio` | `match_input_image` | Output aspect ratio |
| `--output-format` | `png` | `png` or `jpg` |
| `--safety-tolerance` | `2` | 0–5 |
| `--prompt-upsampling` / `--no-prompt-upsampling` | `false` | Prompt upsampling |

---

### `product-photography` — Composite product onto background

**When to use:** Place a product cutout onto a background scene with lighting from a text prompt.

**Requires:** `--product-photo`, `--background-photo`, `--prompt`.

```bash
tft files upload --file ./product.png
tft files upload --file ./bg.jpg
tft image-generate product-photography --product-photo PRODUCT_URL --background-photo BG_URL -p "soft studio lighting"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--product-photo` | required | Product image URL |
| `--background-photo` | required | Background image URL |
| `--prompt` / `-p` | required | Scene and lighting description |
| `--lora-strength` | `0.7` | LoRA strength 0.0–1.0 |
| `--guidance-scale` | `4.5` | Guidance scale |
| `--output-format` | `png` | `png` or `jpg` |

---

## Video generation (`tft video-generate`)

### `create-prompt` — Create a model-ready video prompt

**When to use:** Turn a rough scene brief into a generation-ready prompt before calling `generate`.

```bash
tft video-generate create-prompt --model veo-3.1-fast -i "Ocean waves at golden hour, aerial drone"
tft video-generate create-prompt -m seedance-2.0-reference-to-video -i "Jewellery macro, slow dolly, luxury pacing"
```

| Flag | Required | Description |
|------|----------|-------------|
| `--model` / `-m` | Yes | Video model ID — selects which prompt skill guide to use |
| `--instruction` / `-i` | Yes | Rough scene description or creative brief |

**Skill routing:** `seedance-2.0-*` models use the Seedance 2.0 cinematic guide; all other models use a generic video guide. Response includes `prompt` (use with `generate`) and `skill` (which guide was used). No credits charged.

**In Flow Studio:** Use the **Video Prompt** node (`video-prompt-enhance`) to run this inside a pipeline—wire `output` to a video generator's `prompt` input. Set the node's **Target Model** to match the downstream generator.

**Two-step workflow:**
```bash
tft video-generate create-prompt -m veo-3.1-fast -i "Cat walking through neon alley at night"
# copy prompt from output, then:
tft video-generate generate -m veo-3.1-fast --prompt "..." --duration 5
```

### `generate` — Generate video with Veo, Kling, Seedance, and other models

**When to use:** Create video from text, a starting image, reference clips, or multi-shot setups.

```bash
tft video-generate generate --prompt "Ocean waves at sunset" --model veo-3.1-fast --duration 5
tft video-generate generate -p "Slow cinematic pan" --image UPLOAD_URL --aspect-ratio 16:9
tft video-generate generate -p "Character walks" --reference-image REF_URL --model kling-o3-reference-to-video-pro
```

### Model selection guide

| Model | Capability | Typical inputs |
|-------|------------|----------------|
| `veo-3.1-fast` | Text or image to video | `--prompt`, optional `--image` |
| `veo-3.1` | Higher quality Veo | `--prompt`, optional `--image` |
| `creatify-aurora` | Talking avatar from image + audio | `--image`, `--reference-audio` |
| `kling-o3-text-to-video-standard` | Text to video | `--prompt` |
| `kling-o3-text-to-video-pro` | Text to video (pro) | `--prompt` |
| `kling-o3-image-to-video-standard` | Image to video | `--image`, `--prompt` |
| `kling-o3-image-to-video-pro` | Image to video (pro) | `--image`, `--prompt` |
| `kling-o3-reference-to-video-standard` | Reference image to video | `--reference-image`, `--prompt` |
| `kling-o3-reference-to-video-pro` | Reference image to video (pro) | `--reference-image`, `--prompt` |
| `kling-o3-edit-video-standard` | Edit existing video | `--video`, `--prompt` |
| `kling-o3-edit-video-pro` | Edit existing video (pro) | `--video`, `--prompt` |
| `kling-o3-video-reference-standard` | Style/motion from reference video | `--video`, `--prompt` |
| `kling-o3-video-reference-pro` | Style/motion from reference video (pro) | `--video`, `--prompt` |
| `seedance-v1.5-pro-text-to-video` | Seedance text to video | `--prompt` |
| `seedance-v1.5-pro-image-to-video` | Seedance image to video | `--image`, `--prompt` |
| `seedance-2.0-fast-text-to-video` | Fast Seedance 2.0 T2V | `--prompt` |
| `seedance-2.0-text-to-video` | Seedance 2.0 T2V (quality) | `--prompt` |
| `seedance-2.0-fast-image-to-video` | Fast Seedance 2.0 I2V | `--image`, `--prompt` |
| `seedance-2.0-image-to-video` | Seedance 2.0 I2V (quality) | `--image`, `--prompt` |
| `seedance-2.0-fast-reference-to-video` | Fast ref image/video/audio to video | `--reference-image`, `--reference-video`, `--reference-audio` |
| `seedance-2.0-reference-to-video` | Ref to video (quality) | `--reference-image`, `--reference-video`, `--reference-audio` |
| `happy-horse-text-to-video` | Happy Horse T2V | `--prompt` |
| `happy-horse-image-to-video` | Happy Horse I2V | `--image`, `--prompt` |
| `happy-horse-reference-to-video` | Happy Horse ref to video | `--reference-image`, `--prompt` |
| `happy-horse-video-edit` | Happy Horse video edit | `--video`, `--prompt` |
| `ltx-2.3-text-to-video` | LTX 2.3 text to video | `--prompt` |
| `ltx-2.3-image-to-video` | LTX 2.3 image to video | `--image`, `--prompt` |
| `ltx-2.3-audio-to-video` | LTX 2.3 audio-driven video | `--reference-audio` |
| `ltx-2.3-video-to-video` | LTX 2.3 video transform | `--video`, `--prompt` |
| `ltx-2.3-reference-video-to-video` | LTX 2.3 ref video to video | `--reference-video`, `--prompt` |
| `ltx-2.3-extend-video` | Extend existing video | `--video`, `--prompt` |

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--model` / `-m` | `veo-3.1-fast` | Video model (see table above) |
| `--prompt` / `-p` | — | Text prompt |
| `--image` | — | Start frame URL |
| `--last-frame` | — | End frame URL (interpolation) |
| `--reference-image` | — | Reference image URL (repeatable) |
| `--reference-video` | — | Reference video URL (repeatable) |
| `--reference-audio` | — | Reference audio URL (repeatable) |
| `--video` | — | Source video URL (edit/extend) |
| `--duration` | `5` | Duration in seconds (1–60) |
| `--resolution` | — | e.g. `720p`, `1080p` |
| `--aspect-ratio` | `16:9` | e.g. `16:9`, `9:16` |
| `--generate-audio` / `--no-generate-audio` | `true` | Generate or keep audio |
| `--camera-fixed` / `--no-camera-fixed` | — | Seedance: fix camera position |
| `--elements` | — | Kling character/object elements (JSON array) |
| `--multi-prompts` | — | Kling multi-shot prompts (JSON: `[{prompt, duration}]`) |
| `--shot-type` | `customize` | Kling multi-shot type |
| `--lora` | — | LoRA weight URL (repeatable) |
| `--lora-scale` | `1.0` | Scale per LoRA (repeatable) |
| `--seed` | — | Random seed |
| `--negative-prompt` | — | Negative prompt |
| `--folder-id`, `--message-id` | — | Organization / tracking |

**Kling multi-shot example:**
```bash
tft video-generate generate --model kling-o3-reference-to-video-multishot \
  --prompt "A day in the city" \
  --multi-prompts '[{"prompt":"Morning coffee","duration":3},{"prompt":"Evening walk","duration":4}]' \
  --reference-image UPLOAD_URL
```

---

## Motion control (`tft motion-control animate`)

**When to use:** Make a still image move by transferring motion from a reference video ("animate this photo like that clip").

**Requires:** `--image`, `--video` (both uploaded URLs).

```bash
tft files upload --file ./portrait.jpg
tft files upload --file ./motion.mp4
tft motion-control animate --image PORTRAIT_URL --video MOTION_URL --model-variant pro
tft motion-control animate --image PORTRAIT_URL --video MOTION_URL --model-variant wan-2.2-animate-replace -p "Replace character"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--image` | required | Still image URL |
| `--video` | required | Reference motion video URL |
| `--model-variant` | `pro` | `std`, `pro`, or `wan-2.2-animate-replace` |
| `--duration` | `5.0` | Estimated output duration (pricing) |
| `--prompt` / `-p` | — | Optional guidance text |
| `--keep-original-sound` / `--no-keep-original-sound` | `true` | Keep reference video audio |
| `--character-orientation` | `video` | `image` or `video` |
| `--refert-num` | `1` | Wan reference frames: `1` or `5` |
| `--frames-per-second` | `24` | Output FPS (Wan) |
| `--go-fast` / `--no-go-fast` | `true` | Fast processing (Wan) |
| `--resolution` | — | e.g. `720` (Wan) |
| `--folder-id`, `--message-id` | — | Organization / tracking |

Poll job status after submission.

---

## Audio & voice (`tft audio-generate`)

Create and edit audio — speech, voice conversion, isolation, dubbing, sound effects, transcription.

### `text-to-speech` — Synthesize speech from text

**Requires:** `--text`, `--voice-id`.

```bash
tft audio-generate text-to-speech --text "Welcome to TheFluxTrain." --voice-id YOUR_VOICE_ID
tft audio-generate text-to-speech -t "Hello world" --voice-id VOICE_ID --model-id eleven_multilingual_v2
```

| Flag | Default | Description |
|------|---------|-------------|
| `--text` / `-t` | required | Text to synthesize |
| `--voice-id` | required | ElevenLabs voice ID |
| `--model-id` | `eleven_multilingual_v2` | TTS model |
| `--output-format` | `mp3_44100_128` | Output format |

---

### `speech-to-speech` — Convert speech to a different voice

**Requires:** `--audio-url`, `--voice-id`.

```bash
tft files upload --file ./source.mp3
tft audio-generate speech-to-speech --audio-url UPLOAD_URL --voice-id YOUR_VOICE_ID
```

| Flag | Default | Description |
|------|---------|-------------|
| `--audio-url` | required | Source audio URL |
| `--voice-id` | required | Target voice ID |
| `--model-id` | `eleven_multilingual_sts_v2` | Speech-to-speech model |
| `--output-format` | `mp3_44100_128` | Output format |
| `--filename` | — | Optional filename hint |

---

### `isolation` — Isolate vocals or speech

**Requires:** `--audio-url`.

```bash
tft files upload --file ./track.mp3
tft audio-generate isolation --audio-url UPLOAD_URL
```

| Flag | Description |
|------|-------------|
| `--audio-url` | required — source audio URL |
| `--filename` | Optional filename hint |

---

### `dubbing-start` — Dub audio into another language

**Requires:** `--audio-url`, `--target-lang`.

```bash
tft files upload --file ./voice.mp3
tft audio-generate dubbing-start --audio-url UPLOAD_URL --target-lang es
```

| Flag | Description |
|------|-------------|
| `--audio-url` | required — source audio URL |
| `--target-lang` | required — e.g. `es`, `fr` (2–10 char language code) |
| `--filename` | Optional filename hint |

---

### `sound-effects` — Generate sound effects from text

**Requires:** `--text`.

```bash
tft audio-generate sound-effects --text "Soft rain on window" --duration-seconds 3
tft audio-generate sound-effects -t "Door creak" --loop
```

| Flag | Default | Description |
|------|---------|-------------|
| `--text` / `-t` | required | Sound effect description |
| `--duration-seconds` | — | 0.5–30 seconds |
| `--prompt-influence` | `0.3` | 0.0–1.0 |
| `--loop` / `--no-loop` | `false` | Seamlessly looping SFX |

---

### `speech-to-text` — Transcribe to plain text

**Requires:** `--audio-url`. Returns immediately — no job polling.

```bash
tft files upload --file ./interview.mp3
tft audio-generate speech-to-text --audio-url UPLOAD_URL --language en
```

| Flag | Default | Description |
|------|---------|-------------|
| `--audio-url` | required | Source audio URL |
| `--language` | `en` | Language hint |
| `--model-id` | `grok-speech-to-text` | STT model |
| `--format-text` / `--no-format-text` | `true` | Punctuation and capitalization |

---

### `transcribe-words` — Word-level timestamps

**Requires:** `--audio-url`. Returns word-level timing (WhisperX).

```bash
tft files upload --file ./clip.wav
tft audio-generate transcribe-words --audio-url UPLOAD_URL --language en
tft audio-generate transcribe-words --audio-url UPLOAD_URL --task translate
```

| Flag | Default | Description |
|------|---------|-------------|
| `--audio-url` | required | Source audio URL |
| `--language` | — | ISO code; omit for auto-detect |
| `--model-id` | `whisperx` | Transcription model |
| `--task` | `transcribe` | `transcribe` or `translate` (to English) |
| `--align-output` / `--no-align-output` | `true` | Word-level timestamps |
| `--initial-prompt` | — | Vocabulary/style hint |
| `--batch-size` | `64` | Parallelization batch size |

Use word timestamps for video-editor subtitles or caption workflows.
