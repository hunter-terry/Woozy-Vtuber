# Runtime

The full `WoozyLiveSetup.js` controller (1,193 lines, 8.7MB — most of it embedded
fitted mesh data) ships in the checkpoint Releases rather than being committed
here. What's in the repo:

- `src/fitting/` — the Python scripts that compute the fitted data the controller embeds
- `src/obs/` — the Lua stream controls and OBS configuration
- `docs/case-study.md` — how the runtime's systems (droop, recovery, tracking-loss
  safety, accessory presets) were specified and verified
