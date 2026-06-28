# The Kumar Method — Create images like @thekumarmethod

Recreate the **thekumarmethod** look from any source clip: keep the original **pose, framing, and scene**, swap the **face, text, and styling** with AI — no reshoot, no long prompt engineering.

Inspired by [@thekumarmethod](https://www.instagram.com/thekumarmethod/). This repo documents the **image workflow only** — how to go from a video clip to an approval-ready restyled still.

---

## How to use this repo

1. **Replace the image in `my-image/`** — swap `my-image/my-image.png` with your own portrait photo. This is the face used across every scene.
2. **Replace the script in `script.md`** — write your speaking lines, one scene per block, with each scene separated by `---` on its own line.
3. **Run the workflow in your AI editor:**
   - **Cursor:** open Plan mode with `script.md`, review the plan, then Verify and Build.
   - **Claude Code:** plan first using [`SKILL.md`](SKILL.md), then execute the steps it outlines.

The agent reads your script, generates scene docs, restyled images, Seedance clips, and assembles the final intro video on the timeline.

---

## What this repo covers

| Step | Output |
|------|--------|
| Upload a source video | Motion and composition reference |
| Extract the clearest frame | Sharp still from your clip |
| Restyle with GPT Image 2 | New image — new face, text, or styling |

**This workflow does not generate video.** It stops at the restyled image. You use a clip only to borrow a single frame (pose, lighting, framing).

---

## The idea in one sentence

**Upload video → grab the clearest frame → describe what to change → GPT Image 2 restyles the still while preserving pose and scene.**

Why not edit the whole video in one prompt? Video models often rewrite motion when you ask for appearance changes. This workflow isolates the edit to **one still** so pose, outfit, framing, and lighting stay locked.

---

## Quick start

Run the workflow in **TheFluxTrain Flow Studio** — no local install required.

| Resource | Link |
|----------|------|
| **Open the template** | [The Kumar Method in Explore](https://thefluxtrain.com/explore?flowTemplateId=12) |
| **Tutorial and results** | [Create images like thekumarmethod from your own video](https://thefluxtrain.com/tutorials/flow-studio-thekumarmethod-video-restyle-tutorial) |

---

## What you need

- **Source video** — any clip where the subject’s face is visible, not motion-blurred, and not blocked by hands or props.
- **Reference photo** (recommended) — clear headshot or portrait for the new identity.
- **Short edit note** — plain language for what should change (see [Prompts](#prompts)).
- **TheFluxTrain account** — image generations use credits. Expect a few runs while you pick the best frame and restyle result.

**Time:** First run is usually **5 minutes**, including uploads and one or two restyle attempts.

---

## Workflow overview

### How the Flow Studio graph is wired

| Node | What it does |
|------|----------------|
| **1. Source Video** | Your original clip — used only to pull a still. |
| **2. Extract First Frame** | Pulls **Start**, **Custom**, and **End** frame previews. |
| **Additional edits** | Where you type simple instructions (text swap, identity cue). |
| **Describe Image** | Auto-notes background, outfit, and expression so prompts stay consistent. |
| **Prompt Template — GPT Image 2** | Combines your instruction + scene description into one edit prompt. |
| **3. GPT Image 2 — Restyle Frame** | Produces the new still; compare variants in the node sink. |

The **Instructions** note on the canvas repeats these steps while you work.

---

## Step-by-step

### 1. Open the template

Go to [The Kumar Method](https://thefluxtrain.com/explore?flowTemplateId=12). Demo media loads so you can explore before swapping in your own files.

### 2. Add your source video

Select **1. Source Video** and replace the placeholder — upload from disk or paste a hosted URL.

Pick footage where the subject’s **face is visible**, not motion-blurred, and not blocked by props or hands.

### 3. Extract the best frame

Select **2. Extract First Frame** and click **Generate**.

The node shows **Start**, **Custom**, and **End** previews. Choose the one where the person reads clearest — usually **Custom** after you set **Custom time** to a moment mid-gesture.

If the Custom frame is wrong, adjust **Custom time** slightly and generate again. Do not move on until one frame looks sharp.

### 4. Add a reference photo (optional)

Replace the **Character reference** image with your target identity — a well-lit portrait works best.

This image feeds **Image 2** on the GPT Image 2 node so the swap has a concrete face to match.

### 5. Write your edit in plain language

Open **Additional edits** and type what should change. Keep it short and visual — appearance edits, not new actions.

See [Prompts](#prompts) for copy-paste examples.

The template merges your line into the GPT Image 2 prompt automatically. You do not need to write the long preservation block yourself.

### 6. Generate the restyled frame

Select **3. GPT Image 2 — Restyle Frame** and click **Generate**.

Inspect results in the node **sink** — arrow through variants and pick the one where skin tone, hands, and text look correct.

Regenerate if hands look older than the face or if text garbles.

**Important:** If you change the source video or extracted frame, re-run **Extract First Frame**, then GPT Image 2 again so inputs stay in sync.

![Sample output](https://storage.googleapis.com/saquib-sh.appspot.com/thefluxtrain/v02/image-generation/35ae2291-a199-4a2e-9742-f9b0c43c3152/51yss6e.png)
