# Woozy — Real-Time VTuber Character System

A webcam-driven slime VTuber character built in Snap Lens Studio, with AI-assisted development under my creative direction. Live in production on my Twitch stream.

<video src="showcase/woozy-v1-vs-v2.mp4" width="400"></video>

*Version 1 → Version 2: smoother geometry, glossy slime material, cleaner silhouette.*

![Woozy live on stream](showcase/live-on-stream.jpg)

*Woozy live on stream — webcam face tracking driving eyes and mouth in real time.*

## What it is

- **Live face tracking** — webcam drives eyes and mouth; integrated goo brows and nose-steered upper-head motion
- **Slime behavior system** — heavy, sticky, slow droop physics with exact neutral recovery (6.6s), tracking-loss cancellation with 0.85s fade, and automatic drips on a 45–90s cycle
- **Accessory system** — four switchable presets (Clean / Helmet / Goggles / Full Tactical) via Lens Studio buttons, with droop-aware goggle fitting computed against the authored body mesh
- **Stream integration** — OBS Lua controls, configured OBS scene, one-tap preset switching mid-stream
- **Verified, not vibes** — 40 automated checks passed plus live observation, with explicit documented limits (see [verification](docs/case-study.md#verification))

## Tech

Lens Studio · JavaScript (1,200-line runtime controller) · Python (mesh-fitting scripts, Blender 5.2 background mode) · Lua (OBS controls) · OBS Studio · Twitch (production)

## How it was built

AI-assisted technical art: I specified every requirement, directed each iteration, reviewed every change against the approved character spec, and verified it live before accepting it. The modeling, controller code, and fitting scripts were produced with AI assistance; the creative direction, review, acceptance testing, and production deployment are mine. I'm early in my 3D journey — this repo documents what AI-assisted iteration can ship when it's directed rigorously.

## Repo layout

```
showcase/      v1→v2 comparison video, stills, live-on-stream frame
docs/          full case study: requirements, iteration, verification
src/
  runtime/     Lens Studio controller (WoozyLiveSetup.js)
  fitting/     Python goggle/droop fitting scripts + JS fitting module
  obs/         Lua stream controls + OBS configuration
checkpoints/   dated full-project archives ship as GitHub Releases (see below)
```

## Checkpoints

Full project snapshots (Oct 4 goo face → Oct 6 stream setup → Oct 11 accepted character) are published as [GitHub Releases](../../releases) rather than committed — 70MB of nested archives would make this repo uncloneable. Each release includes the complete Lens project, controller, fitting sources, OBS config, verification data, and rollback scripts.

## Live

Streaming as [@woozyfilms on Twitch](https://www.twitch.tv/woozyfilms) — the character runs in the top frame of every stream.
