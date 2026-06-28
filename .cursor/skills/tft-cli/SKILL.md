---
name: tft-cli
description: >-
  Guide for helping creators use the TheFluxTrain CLI (tft) from the terminal.
  Covers install, login, file upload, media metadata, job polling, and routing
  to the right command group. Use when the user wants to generate media, edit
  Flow Studio pipelines, edit video timelines, or build character/product bibles via tft, or asks about
  thefluxtrain-cli commands.
---

# TheFluxTrain CLI (tft) — Agent Guide

Help creators run TheFluxTrain from the terminal. This skill covers authentication, shared utilities, and how to pick the right tool. Load a domain skill when you know the goal:

| Skill | Use for |
|-------|---------|
| **tft-cli-models** | One-off image, video, motion, or audio generation |
| **tft-cli-flow-studio** | Building and wiring Flow Studio node graphs |
| **tft-cli-video-editor** | Timeline editing — clips, tracks, subtitles, story |
| **tft-cli-characters** | Character/product bibles — previews and reference sheets |

When flags or commands are uncertain, run `tft commands` and `tft <group> <command> --help` as the live source of truth.

---

## What tft is

The **TheFluxTrain CLI** (`tft`) lets creators call TheFluxTrain from the terminal. After a one-time browser sign-in, they can generate images and videos, build Flow Studio pipelines, and edit timeline projects without writing HTTP requests by hand.

---

## Getting started

### Install

```bash
pip install thefluxtrain-cli
```

Or with uv:

```bash
uv tool install thefluxtrain-cli
```

Confirm:

```bash
tft --help
```

### Sign in and session

```bash
tft login      # device-code sign-in in the browser
tft whoami     # show signed-in account
tft commands   # list all command groups
tft sync       # refresh command list (run after platform updates)
tft logout     # clear local credentials
```

**Sign-in flow:** Run `tft login` → open https://thefluxtrain.com/cli/authorize → enter the code from the terminal → return to the terminal. Credentials are stored locally; no manual API key paste required.

---

## Universal agent rules

1. **Never pass local file paths** to generation flags, Flow Studio media inputs, or video-editor `cloudUrl`.
2. **Always upload first:** `tft files upload --file <path>` → copy the URL from the output.
3. **Upload once, reuse everywhere** — same URL for generation, Flow Studio input nodes, and video editor.
4. **Async jobs:** When a generation returns a job id, poll until complete:
   ```bash
   tft jobs check-status --editor-id JOB_ID
   ```
5. **Help on demand:** `tft <group> <command> --help` for flags and examples.
6. **Models + video editor:** Generation commands (`image-generate`, `video-generate`, `motion-control`, `audio-generate`) can be combined with the video editor. Typical pattern: generate media with **tft-cli-models** → upload or use the output URL → add clips to a timeline with **tft-cli-video-editor** (`createAsset` for video, image, or audio, tracks, subtitles, etc.).
7. **Flows are Flow Studio only:** When the creator asks to make a **flow**, build a **pipeline**, or wire a **repeatable workflow**, use **flow-studio** and **utils from this skill only** (`files upload`, `media info`, etc.). Do **not** substitute one-off `image-generate` / `video-generate` / `audio-generate` commands for nodes that belong in the graph — create and connect the matching Flow Studio nodes instead (see **tft-cli-flow-studio**).

---

## Utils (shared by all tools)

These commands are used across image, video, Flow Studio, and video editor workflows. See domain skills for generation-specific commands.

### File upload

Upload a local image, video, or audio file (max 100 MB) and get a public URL.

```bash
tft files upload --file ./photo.png
tft files upload -f ./clip.mp4
tft files upload --file ./voice.mp3
```

**When to use:** Before any command that needs `--input-image`, `--image`, `--video`, `--audio-url`, Flow Studio `input-image` / `input-video` / `input-audio` nodes, or video-editor `cloudUrl`.

### Media metadata

Probe width, height, duration, and other metadata for local files or uploaded URLs.

```bash
tft media info --file ./clip.mp4
tft media info --url UPLOAD_URL
tft media info --file ./clip.mp4 --output json
```

**When to use:** Before `video-editor` `createAsset` — video/image need `width`, `height`, and `duration`; audio clips need `duration` only.

### Video prompt creation

Turn a rough scene brief into a model-ready prompt before generation. No credits charged.

```bash
tft video-generate create-prompt --model veo-3.1-fast -i "Ocean waves at golden hour, aerial drone"
tft video-generate create-prompt -m seedance-2.0-reference-to-video -i "Jewellery macro, slow dolly, luxury pacing"
```

**When to use:** Creator has a rough idea but needs a polished, model-specific prompt. Seedance 2.0 models use the Seedance cinematic guide; other models use a generic video guide.

**Typical two-step workflow:**
1. `tft video-generate create-prompt --model MODEL -i "brief"` → copy `prompt` from output
2. `tft video-generate generate --model MODEL --prompt "..."` (+ uploads as needed)

See **tft-cli-models** for full `create-prompt` flags.

### Extract audio from video

Derive an audio file from a video URL.

```bash
tft files upload --file ./clip.mp4
tft video-render extract-audio --url UPLOAD_URL --format m4a
```

Formats: `m4a` (default), `mp3`, `wav`.

### Extract frames from video

Capture PNG screenshots at the start, end, and/or specific times in a video.

```bash
tft files upload --file ./clip.mp4

# Default: first + last frame
tft video-render extract-frames --url UPLOAD_URL

# Specific times only (seconds)
tft video-render extract-frames --url UPLOAD_URL --no-start --no-end --timestamp 1.5 --timestamp 4.0

# Start frame + one midpoint
tft video-render extract-frames --url UPLOAD_URL --no-end --timestamp 3.0
```

Response fields: `start`, `end`, `timestamps` (array of URLs, one per `--timestamp` in order). Use as `image` / `last_frame` inputs for image-to-video models.

### Job status

Check progress on long-running image, video, motion, or audio jobs.

```bash
tft jobs check-status --editor-id YOUR_JOB_ID
```

Repeat until the job completes and an output URL is available. Use the job id returned from the generation command.

### Output format and verbose

Available on manifest commands:

```bash
tft flow-studio list --output yaml
tft video-editor get --project-id PID --output json -v
```

- `--output json` or `--output yaml` — structured response for parsing
- `-v` / `--verbose` — log request details to stderr when debugging

---

## Command group router

Map the creator's goal to the right group and skill:

| Creator wants… | Command group | Skill |
|----------------|---------------|-------|
| A single image (text, reference, inpaint, LoRA, cartoon, product shot) | `image-generate` | tft-cli-models |
| A single video (text-to-video, image-to-video, reference, edit) | `video-generate` | tft-cli-models |
| Polish a rough scene brief into a model-ready video prompt | `video-generate create-prompt` | tft-cli-models |
| Animate a still using motion from a reference video | `motion-control` | tft-cli-models |
| Speech, voice change, dubbing, SFX, transcription | `audio-generate` | tft-cli-models |
| A reusable multi-step pipeline (node graph) | `flow-studio` | tft-cli-flow-studio |
| Edit a timeline — clips, tracks, subtitles, story | `video-editor` | tft-cli-video-editor |
| Character or product bible (preview + sheet) | `characters` | tft-cli-characters |
| Upload a file | `files` | _(this skill)_ |
| Probe media dimensions/duration | `media` | _(this skill)_ |
| Extract audio from video | `video-render` | _(this skill)_ |
| Extract frame screenshots from video | `video-render` | _(this skill)_ |
| Poll async generation | `jobs` | _(this skill)_ |

### Decision flow

```
Creator request
  → Local file involved? → tft files upload first
  → Wants a "flow" / pipeline / wired workflow? → tft-cli-flow-studio + utils ONLY (no one-off model commands)
  → Single generation output (no flow)? → tft-cli-models
  → Rough idea needs a polished video prompt first? → tft video-generate create-prompt, then tft-cli-models generate
  → Timeline / edit project? → tft-cli-video-editor (can use tft-cli-models first to generate clips, then place on timeline)
  → Character or product bible? → tft-cli-characters (create → generate-preview → sheet-prompt → generate-sheet)
```

### Models with video editor

These skills work together for end-to-end edits:

1. **Generate** — `tft image-generate`, `tft video-generate`, `tft motion-control`, or `tft audio-generate` (see **tft-cli-models**)
2. **Upload** — if the output is a local file, `tft files upload`; otherwise reuse the generation output URL
3. **Edit timeline** — `tft video-editor` to create the project, add video/image/audio clips, tracks, subtitles (see **tft-cli-video-editor**)

Example: `tft audio-generate text-to-speech` → upload MP3 → `createAsset` with `type:"audio"` on track 2, alongside video B-roll on track 1.

### Flow requests — Flow Studio strict mode

When the user says **flow**, **pipeline**, **workflow**, or **graph**:

- Use `tft flow-studio` commands only for structure and wiring
- Use utils from this skill (`files upload`, `media info`, `jobs check-status`) as needed
- **Do not** call `tft image-generate generate`, `tft video-generate generate`, or other standalone model commands as a stand-in for Flow Studio nodes
- Pick node `definitionId` values from `tft flow-studio nodes` and wire them with `apply` actions

---

## Sub-skill summaries

### tft-cli-models

One-off generation: images (`generate`, `lora`, `cartoon-convert`, `product-photography`), videos (`video-generate generate` with 27+ models, `video-generate create-prompt` for model-ready prompts), motion (`motion-control animate`), and audio (`text-to-speech`, `speech-to-speech`, `isolation`, `dubbing-start`, `sound-effects`, `speech-to-text`, `transcribe-words`).

### tft-cli-flow-studio

List, create, read, and patch Flow Studio graphs. Six commands: `list`, `create`, `get`, `apply`, `nodes`, `collections`. Apply uses JSON actions: `create`, `update`, `delete`, `connect`. **CLI edits graph structure only** — running generation happens in the browser at Flow Studio.

### tft-cli-video-editor

Eight subcommands for timeline projects: `list`, `create`, `get`, `apply-asset`, `apply-subtitle`, `apply-timeline`, `apply-story`, `delete`. Nine mutation operations for video, image, audio, text, and shape clips, plus tracks, settings, subtitles, and story text. Pairs naturally with **tft-cli-models** when generated media should land on a timeline.

### tft-cli-characters

Seven subcommands for character/product bibles: `list`, `create`, `get`, `add-preview`, `generate-preview`, `sheet-prompt`, `generate-sheet`. Preview step uses nano-banana; sheet step uses gpt-image-2. Pairs with **tft-cli-flow-studio** via `input-character` nodes.

---

## Troubleshooting

| What you see | What to try |
|--------------|-------------|
| Login timed out | Run `tft login` again; complete browser authorization before the code expires |
| Command list unavailable | Run `tft login` or `tft sync` |
| 403 Unauthorized | Run `tft logout`, then `tft login` again |
| Command not found | Run `tft sync` to refresh the command list |
| `flow-studio` or `video-editor` missing | Run `tft sync` after a platform update; confirm with `tft commands` |
| Flow Studio apply returns 422 | Check JSON: valid `op`, camelCase fields, correct port ids from `tft flow-studio nodes` |
| Flow Studio apply returns 404 | Confirm `--flow-id` exists (`tft flow-studio list`) |
| Video editor apply returns 422 | Check action JSON; video/image need `cloudUrl` + dimensions from `tft media info`; audio needs `cloudUrl` + `duration` |
