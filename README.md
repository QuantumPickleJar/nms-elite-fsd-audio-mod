# NMS Elite Dangerous FSD Audio Mod

**Status: diagnostics / not yet audibly verified.** This is a cross-device engineering workspace for an in-development *No Man's Sky* Forsaken seamless-warp sound replacement: an Elite Dangerous-style FSD engine crescendo and COVAS “4 … 3 … 2 … 1” countdown.

**No playable mod release is established yet.** Prior 23-WEM builds made no detectable change in-game. Do not install the archived early media as if it were a working release.

## Current findings (2026-11-08)

- **Confirmed local installation defect (per Windows agent audit):** Registered mod root `GAMEDATA/MODS/NMS_FSD_SeamlessWarp_MODS_Install` contains another `NMS_FSD_SeamlessWarp` directory before `AUDIO`. NMS expects `AUDIO` directly below the *registered root*. Fix and verify that before changing codecs again.
- **Confirmed in the recovered old 42 MB ZIP:** 23 attempted WEM files with nonstandard `0xFFFE` PCM-like headers (not proven Wwise-runtime compatible). That ZIP is **not** the newest converted build.
- **Later Windows audit, not independently reproduced here:** 23 candidate IDs map statically to the persistent audio bank; the three `Sequence_End` targets were reported *memory resident*, contradicting an “all streamed” characterization. Reconcile per-ID storage and mappings against the installed Forsaken build.
- **Unverified:** Newest converted WEM runtime playback; Forsaken seamless-warp event dispatch; FSD engine and countdown timing; any bank patch compatibility. A one-file probe replacing a game sound with itself is *not* an audible pass/fail test.
- **Known-positive user observation:** Subnautica PDA exosuit voice replacement works on the same installation. Its localized WEM path does **not** establish that warp SFX event IDs work.
- **New external lead:** [Unmute Pulse Drive (Forsaken)](https://www.nexusmods.com/nomanssky/mods/4765) notes a soundbank muting interaction and modifies `AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK`. Do not combine competing BNK replacements blindly. [Warframe UI Sounds](https://www.nexusmods.com/nomanssky/mods/4218) describes a known quick-menu open/close loose-WEM replacement: good candidate for an *audibly distinct*, isolated loader probe.

## Work order

1. Fix registered mod-root path, preserve unrelated mods, compare installed hashes.
2. Make a one-file in-game **quick-menu opening** diagnostic with a clearly distinguishable sound. Verify the actual media ID and whether the sound is streamed. No ordinary unmodified game WEM as the “probe”.
3. Demonstrate the sound switches back to vanilla when the probe is removed. If no audible change, debug loader / WEM format / bank ownership, not the full warp sequence.
4. Investigate pulse/seamless warp event-to-media dispatch against installed Forsaken banks, and interference from the Forsaken pulse audio muting problem.
5. Integrate the original private source recordings only after a passed gate; assemble and time the FSD voice/countdown/engine event layers.
6. Produce a versioned MODS-compatible ZIP, install/rollback instructions, SHA-256 manifest and game test report (explicitly label any untested result).

## Handoffs

- [Windows Luna / local game prompt](docs/LUNA_WINDOWS.md)
- [Copilot / Codespaces upstream prompt](docs/COPILOT_CODESPACES.md)
- [Detailed project evidence and suspects](docs/DIAGNOSTICS.md)
- [Private assets / restoration guide](docs/ASSETS.md)
- [Historical mapping information](data/README.md)

## Local paths from previous sessions

- Game (tower): `F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky`
- Workspace (tower): `C:\Users\vmorr\Documents\ChatGPT\NMS Modding\NMS_FSD_Working\Build_Sequence`

These are historical targets, not paths accessible from a Linux Codespace.

## Safety, rights, and attribution

This **public** repository holds documentation, metadata, reusable original scripts, and agent instructions only. It deliberately excludes extracted Hello Games game data, persistent soundbanks, the author's Subnautica / Warframe / Unmute mod archives, copyrighted Elite Dangerous recordings, and finished derivative WEM audio without redistribution clearance. Bring required materials into a **private local workspace** for builds; the repository documents hashes/mappings where useful.

Reference resources (do not vendor): [NMSAO](https://www.nexusmods.com/nomanssky/mods/4500), [sound2wem](https://github.com/EternalLeo/sound2wem), [HGPAKtool](https://github.com/monkeyman192/HGPAKtool).
