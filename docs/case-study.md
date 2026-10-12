# Woozy — Case Study

## The brief

Build a VTuber avatar with a specific personality: a small glossy green slime — heavy, sticky, slow — with live webcam-driven eyes and mouth, switchable tactical accessories, and slime physics behavior (droops, drips, recovery). It had to survive real streaming: hours-long sessions, tracking loss, OBS integration, one-tap controls mid-stream.

## Iteration

**v1 → v2 (showcase/woozy-v1-vs-v2.mp4):** the first pass was angular and matte — it read as a green blob, not slime. The rebuild focused on three things: smoother geometry, a glossy transparent material with proper specular response, and a cleaner silhouette. The difference is visible in a single frame.

**Oct 4 — Goo face accepted.** Live webcam eyes/mouth with integrated goo brows. Face tracking drives the character; the brows sell the expression.

**Oct 6 — Stream setup.** OBS integration: Lua stream controls, configured scene, camera headroom. The character runs in production layout (avatar top, gameplay below).

**Oct 11 — Character accepted.** The current baseline, approved after live review ("looks really good"):
- Four accessory presets on Lens buttons: Clean / Helmet / Goggles / Full Tactical (startup is Clean, gear retained but hidden)
- Goggles re-fitted against the authored body mesh with droop-clearance computation — the strap follows the slime's droop envelope instead of clipping through it
- Night-vision optics re-seated (raised, widened 4%) after clipping was spotted at extreme head angles
- Slime behavior finalized: 6.6-second exact neutral recovery, tracking loss cancels a drop and fades to neutral over 0.85s, automatic drips wait 45–90 tracked seconds

Every checkpoint is preserved with rollback scripts — no iteration step is destructive.

## The hard problems

1. **Droop-aware accessory fitting.** Accessories parented to a deforming slime body will clip or detach. The fix: Python scripts (`src/fitting/`) compute fitted vertex positions against the authored body mesh with a droop-clearance envelope, and the runtime embeds those fitted arrays. 975 contact samples verified minimum strap clearance.
2. **State safety across tracking loss.** Webcam tracking drops mid-stream. The system cancels any in-progress drop on tracking loss, fades to exact neutral over 0.85s, and never resumes a stale drop on reacquisition. Review poses are never saved.
3. **Iteration without regression.** Every change ships with automated preservation checks (core functions unchanged, accessory payloads retained) and a rollback script. The Oct 11 checkpoint passed 40 automated checks.

## Verification

40 automated checks passed (preset selection, tap rejection, drop/recovery flow, function preservation, settings readback) plus live observation (four presets switching, helmet/goggles following head tilt, OBS rendering, scene persistence). Documented limits, stated plainly:

- Extreme head angles at peak droop were not exhaustively observed
- The 13ms figure is a Node VM calculation benchmark, not measured Lens/OBS frame time
- Some post-adjustment angles were not re-observed after their fix

A benchmark is not a frame rate, and a passing check is not a viewed angle. The repo says which is which.

## How it was built (AI-assisted)

I directed this project; AI did the heavy lifting on implementation. Concretely, my contributions: requirements and character spec, every iteration decision (v1→v2 direction, accessory fitting approach, behavior tuning), live review and acceptance testing, production deployment and OBS integration. AI contributions: controller code, fitting scripts, mesh data computation, documentation. I'm early in my 3D career — what's demonstrated here is directing AI systems to a shippable, verified result, not independent modeling mastery. The verification discipline is the transferable skill.
