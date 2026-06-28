---
name: tft-cli-video-editor
description: >-
  TheFluxTrain CLI commands for the video editor — timeline projects, clips
  (video, image, audio), tracks, subtitles, and story text. Covers all subcommands
  and nine mutation operations with parameters and examples. Use when the creator
  wants to edit a video timeline programmatically via tft.
---

# tft — Video Editor

Edit timeline projects stored in your account. Projects sync with the browser video editor at `/video-editor`. For file upload and media metadata, see **tft-cli** skill.

---

## Subcommands

| Subcommand | Purpose |
|------------|---------|
| `list` | List saved projects |
| `create` | New or duplicate project |
| `get` | Read full timeline state |
| `apply-asset` | Clip and media mutations |
| `apply-subtitle` | Subtitle enable/disable and per-word edits |
| `apply-timeline` | Track and render-settings mutations |
| `apply-story` | Project narrative text |
| `delete` | Remove project |

All four `apply-*` commands accept the same underlying mutation format; each documents a focused subset.

---

## Typical workflow

```bash
# 1. Probe local media
tft media info --file ./clip.mp4

# 2. Upload
tft files upload --file ./clip.mp4

# 3. Create project
tft video-editor create --name "My edit"

# 4. Add clips
tft video-editor apply-asset --project-id YOUR_PROJECT_ID --actions '[
  {"op":"createAsset","type":"video","trackId":"track-1","cloudUrl":"UPLOAD_URL",
   "name":"clip.mp4","width":1920,"height":1080,"duration":10.5}
]'

# 5. Inspect state (get clip ids, media ids)
tft video-editor get --project-id YOUR_PROJECT_ID
```

**Audio clip** (voiceover on track 2 — duration only, no width/height):

```bash
tft media info --file ./voice.mp3
tft files upload --file ./voice.mp3
tft video-editor apply-asset --project-id YOUR_PROJECT_ID --actions '[
  {"op":"createAsset","type":"audio","trackId":"track-2","cloudUrl":"UPLOAD_URL",
   "name":"voice.mp3","duration":6.0}
]'
```

---

## `list`

```bash
tft video-editor list
```

Returns `projects[]` with `id`, `name`, `created_at`, `updated_at`.

---

## `create`

```bash
tft video-editor create --name "My edit"
tft video-editor create --name "Copy of demo" --source-project-id YOUR_PROJECT_ID
```

| Flag | Required | Description |
|------|----------|-------------|
| `--name` / `-n` | yes | Display name |
| `--source-project-id` | no | Duplicate an existing project |

Returns `project_id`, `name`, `project` (initial timeline state).

**Default blank project:**
- Tracks: `track-1` ("Track 1"), `track-2` ("Track 2")
- Settings: 1080×1920, 30 fps, `backgroundColor: "#000000"`
- Empty `mediaLibrary` and `clips`

---

## `get`

```bash
tft video-editor get --project-id YOUR_PROJECT_ID
```

| Flag | Required | Description |
|------|----------|-------------|
| `--project-id` | yes | Project id from list or create |

Returns `project_id`, `name`, timestamps, and `project` state:

| Field | Description |
|-------|-------------|
| `mediaLibrary` | Reusable uploaded media entries |
| `clips` | Timeline placements |
| `tracks` | Track rows |
| `totalDuration` | Timeline length in seconds |
| `settings` | Canvas width, height, fps, backgroundColor, subtitleStyle |
| `story` | Free-form narrative (Story tab) |

### ID reference

| Id type | Where to find | Used for |
|---------|---------------|----------|
| **Clip id** | `clips[].id` | `assetId` in update/delete/split/subtitle ops |
| **Media id** | `mediaLibrary[].id` | `sourceAssetId` when reusing uploads |
| **Track id** | `tracks[].id` | `trackId` in createAsset, createTrack |

**Rules:**
- `assetId` in mutations = **timeline clip id**, not media library id
- If you pass a media library id as `assetId` and exactly one clip references it, it auto-resolves
- If multiple clips share the same media, you **must** use the clip id

---

## `delete`

```bash
tft video-editor delete --project-id YOUR_PROJECT_ID
```

---

## `apply-story`

Set or clear the project narrative (Story tab).

```bash
tft video-editor apply-story --project-id YOUR_PROJECT_ID --text "Scene 1: Opening shot..."
tft video-editor apply-story --project-id YOUR_PROJECT_ID --text ""
```

| Flag | Required | Description |
|------|----------|-------------|
| `--project-id` | yes | Target project |
| `--text` / `-t` | yes | Full story body (`""` clears) |

Equivalent JSON: `[{"op":"updateStory","text":"..."}]`

---

## Apply commands (`apply-asset`, `apply-subtitle`, `apply-timeline`)

All accept:

| Flag | Required | Description |
|------|----------|-------------|
| `--project-id` | yes | Target project |
| `--actions` | yes | JSON array of mutation actions (camelCase) |

```bash
tft video-editor apply-asset --project-id PID --actions '[{"op":"createAsset",...}]'
```

---

## Operations reference

### `createAsset` — add clip to timeline

**CLI:** `apply-asset`

**Purpose:** Place video, image, audio, text, or shape on a track.

#### Video/image — new upload

Requires `cloudUrl`, `width`, `height`, `duration` from upload + `tft media info`.

```json
{
  "op": "createAsset",
  "type": "video",
  "trackId": "track-1",
  "startTime": 0,
  "cloudUrl": "UPLOAD_URL",
  "name": "clip.mp4",
  "width": 1920,
  "height": 1080,
  "duration": 10.5,
  "id": "optional-clip-id"
}
```

#### Video/image — reuse existing media

```json
{
  "op": "createAsset",
  "type": "video",
  "trackId": "track-2",
  "startTime": 5,
  "sourceAssetId": "media-abc123"
}
```

#### Audio — new upload

Requires `cloudUrl`, `duration` from upload + `tft media info` (no width/height).

```json
{
  "op": "createAsset",
  "type": "audio",
  "trackId": "track-2",
  "startTime": 0,
  "cloudUrl": "UPLOAD_URL",
  "name": "voice.mp3",
  "duration": 6.0,
  "id": "optional-clip-id"
}
```

#### Audio — reuse existing media

```json
{
  "op": "createAsset",
  "type": "audio",
  "trackId": "track-2",
  "startTime": 5,
  "sourceAssetId": "media-abc123"
}
```

#### Text overlay

```json
{
  "op": "createAsset",
  "type": "text",
  "trackId": "track-1",
  "startTime": 2.5,
  "duration": 3,
  "text": "Hello"
}
```

#### Shape overlay

```json
{
  "op": "createAsset",
  "type": "shape",
  "trackId": "track-1",
  "shapeType": "rect",
  "duration": 4
}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | yes | `video`, `image`, `audio`, `text`, or `shape` |
| `trackId` | no | Defaults to first track |
| `startTime` | no | Timeline start (seconds); defaults to end of track |
| `cloudUrl` | yes* | Upload URL (*unless `sourceAssetId` set) |
| `width`, `height`, `duration` | yes* | From `tft media info` (*video/image new upload) |
| `duration` | yes* | From `tft media info` (*audio new upload) |
| `sourceAssetId` | yes* | Media library id (*reuse path) |
| `text` | no | Text content (default: "Double click to edit") |
| `shapeType` | no | `rect` (default) or `circle` |
| `duration` | no | Visible duration (default 5s for text/shape) |
| `id`, `name` | no | Optional clip id and display name |

```bash
tft video-editor apply-asset --project-id PID --actions '[
  {"op":"createAsset","type":"text","trackId":"track-1","text":"Hello"}
]'
```

---

### `updateAsset` — patch clip fields

**CLI:** `apply-asset` (general), `apply-subtitle` (subtitle fields)

**Purpose:** Move, trim, restyle, or add subtitles to a clip.

```json
{
  "op": "updateAsset",
  "assetId": "CLIP_ID",
  "patch": {
    "trackId": "track-2",
    "startTime": 3,
    "duration": 6,
    "speed": 1,
    "trimStart": 0,
    "trimEnd": 0,
    "position": { "x": 540, "y": 960 },
    "scale": 1,
    "width": 800,
    "height": 450,
    "text": "Updated text",
    "style": {
      "fontSize": 64,
      "color": "#ffffff",
      "fontWeight": "700",
      "backgroundColor": "#000000",
      "backgroundOpacity": 0.6,
      "paddingX": 20,
      "paddingY": 12,
      "borderRadius": 12
    },
    "shape": { "type": "rect", "fill": "#22c55e" },
    "framing": {
      "enabled": true,
      "borderWidth": 8,
      "borderColor": "#ffffff",
      "borderRadius": 16
    },
    "crop": { "top": 0, "left": 0, "bottom": 0, "right": 0 },
    "animations": [
      { "id": "anim-1", "type": "fade", "position": "start", "duration": 0.5, "config": {} }
    ],
    "subtitlesEnabled": true,
    "subtitles": {
      "provider": "whisperx",
      "detectedLanguage": "en",
      "text": "hello world",
      "words": [
        { "word": "hello", "start": 0.5, "end": 1.0, "score": 0.99, "style": { "fontSize": 48, "color": "#ffffff" } },
        { "word": "world", "start": 1.0, "end": 1.4, "score": 0.98 }
      ],
      "createdAt": 0
    }
  }
}
```

**Animation types:** `fade`, `slide`, `zoom`, `typewriter`

**Trim vs split:** Use `trimStart`/`trimEnd` to shorten visible media; use `splitAsset` to cut into multiple timeline segments.

```bash
tft video-editor apply-asset --project-id PID --actions '[
  {"op":"updateAsset","assetId":"clip-1","patch":{"startTime":3,"trackId":"track-2"}}
]'
```

---

### `deleteAsset` — remove clip

**CLI:** `apply-asset`

Does not remove the `mediaLibrary` entry.

```json
{ "op": "deleteAsset", "assetId": "CLIP_ID" }
```

---

### `splitAsset` — cut video into segments

**CLI:** `apply-asset`

**Purpose:** Split a video clip at one or more points.

| Parameter | Description |
|-----------|-------------|
| `assetId` | Video clip id |
| `splitTimes` | Array of cut points in **seconds from clip start** (not global timeline) |

**Constraints:**
- Video clips only
- At most **one** `splitAsset` per clip per batch — combine all cuts in one `splitTimes` array
- Each split time must be > 0.1s and < (clip duration − 0.1s)

```json
{ "op": "splitAsset", "assetId": "clip-1", "splitTimes": [5.0] }
{ "op": "splitAsset", "assetId": "clip-1", "splitTimes": [2.0, 5.5, 8.0] }
```

Example: clip at timeline 20s, 10s long → split at midpoint uses `splitTimes: [5.0]`, not `[25.0]`.

---

### `createTrack` — add track row

**CLI:** `apply-timeline`

```json
{ "op": "createTrack", "name": "Track 3" }
{ "op": "createTrack", "id": "track-3", "name": "Overlay" }
```

---

### `deleteTrack` — remove track and all its clips

**CLI:** `apply-timeline`

```json
{ "op": "deleteTrack", "trackId": "track-2" }
```

---

### `updateSettings` — patch composition settings

**CLI:** `apply-timeline`

```json
{
  "op": "updateSettings",
  "patch": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "backgroundColor": "#000000",
    "subtitleStyle": {
      "paddingXL": 40,
      "paddingXR": 40,
      "paddingYT": 18,
      "paddingYB": 18,
      "borderRadius": 12,
      "backgroundColor": "#000000",
      "backgroundOpacity": 0.6,
      "color": "#ffffff",
      "fontSize": 48,
      "centerX": null,
      "centerY": null
    }
  }
}
```

```bash
tft video-editor apply-timeline --project-id PID --actions '[
  {"op":"updateSettings","patch":{"width":1080,"height":1920,"fps":30,"backgroundColor":"#000000"}}
]'
```

---

### `updateStory` — set project narrative

**CLI:** `apply-story` (via `--text`) or any apply command

```json
{ "op": "updateStory", "text": "Scene 1: A hero enters the city at dawn." }
```

---

### `updateSubtitleWord` — patch one subtitle word

**CLI:** `apply-subtitle`

```json
{
  "op": "updateSubtitleWord",
  "assetId": "CLIP_ID",
  "wordIndex": 0,
  "wordPatch": {
    "word": "hello",
    "start": 0.5,
    "end": 1.0,
    "score": 0.99,
    "style": { "color": "#ffff00", "fontSize": 56, "backgroundColor": "#000000", "backgroundOpacity": 0.8 }
  }
}
```

```bash
tft video-editor apply-subtitle --project-id PID --actions '[
  {"op":"updateAsset","assetId":"CLIP_ID","patch":{"subtitlesEnabled":false}}
]'
tft video-editor apply-subtitle --project-id PID --actions '[
  {"op":"updateSubtitleWord","assetId":"CLIP_ID","wordIndex":0,"wordPatch":{"style":{"color":"#ffff00","fontSize":56}}}
]'
```

For global subtitle styling, use `updateSettings` with `patch.subtitleStyle` via `apply-timeline`.

---

## Operation → command routing

| `op` | Recommended command |
|------|---------------------|
| `createAsset`, `updateAsset`, `deleteAsset`, `splitAsset` | `apply-asset` |
| `updateAsset` (subtitle fields), `updateSubtitleWord` | `apply-subtitle` |
| `createTrack`, `deleteTrack`, `updateSettings` | `apply-timeline` |
| `updateStory` | `apply-story` |

---

## Agent batching rules

1. **createAsset exclusivity:** A batch that creates a clip must not also update/delete/split/trim that same new clip. Defer follow-up ops to the next pass after `get`.
2. **splitAsset exclusivity:** At most one `splitAsset` per clip per batch; no other ops on that clip in the same batch.
3. **splitTimes are clip-relative**, not global timeline time.
4. **Do not invent `cloudUrl`** — use `sourceAssetId` for media already in `mediaLibrary`.
5. **Avoid clip overlap** on the same track.

---

## Subtitles workflow

Add voice clip with subtitles in one batch (video clip with embedded subtitles — use `type:audio` for pure voiceover without captions):

```bash
tft video-editor apply-asset --project-id PID --actions '[
  {"op":"createAsset","id":"voice-clip-1","type":"audio","trackId":"track-2",
   "cloudUrl":"UPLOAD_URL","name":"voice.mp3","duration":6.0}
]'
```

For captions burned into the timeline as text overlays, use `type:video` plus subtitle fields:

```bash
tft video-editor apply-asset --project-id PID --actions '[
  {"op":"createAsset","id":"voice-clip-1","type":"video","trackId":"track-1",
   "cloudUrl":"UPLOAD_URL","name":"voice.mp4","width":1920,"height":1080,"duration":6.0},
  {"op":"updateAsset","assetId":"voice-clip-1","patch":{
    "subtitlesEnabled":true,
    "subtitles":{
      "provider":"whisperx","detectedLanguage":"en","text":"hello world",
      "words":[{"word":"hello","start":0.5,"end":1.0},{"word":"world","start":1.0,"end":1.4}]
    }
  }}
]'
```

Skip subtitles for music-only clips (`subtitlesEnabled: false` or leave unset).

Generate word timestamps with `tft audio-generate transcribe-words` (see **tft-cli-models**).

---

## Browser live sync

Open the project in the video editor and enable **Live sync** in the toolbar. The timeline reloads every few seconds in read-only mode while CLI edits are applied. Turn live sync off to edit manually.

---

## Common errors

| Issue | Fix |
|-------|-----|
| 422 on apply | Check JSON: valid `op`, camelCase fields, `cloudUrl` from upload |
| Clip not found | Use clip id from `get`, not media library id (unless unambiguous) |
| Missing dimensions | Run `tft media info` before `createAsset` (audio needs duration only) |
| Split fails | Use clip-relative times; one `splitAsset` per clip per batch |
| Subtitle word edit fails | Clip must have `subtitles.words[]`; check `wordIndex` |
