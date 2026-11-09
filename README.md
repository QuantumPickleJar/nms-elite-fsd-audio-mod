# NMS Elite Dangerous FSD Audio Mod

**Status: 4–3–2–1 countdown package installed; charging-at-ten remains unresolved.** This is a cross-device engineering workspace for an in-development *No Man's Sky* Forsaken seamless-warp sound replacement.

The user confirms “Engaged” no longer plays. Two newer recordings show that the charging replacement also fires during ordinary pulse-drive engagement. Its `Pl_Ship_MiniWarp_Countdown` targets have therefore been removed. The current package retains only the HUD-aligned countdown; charging at the start of the ten-second warp timer needs a different event route.

## Current portable countdown package

The private `NMS_FSD_HUD_Countdown_Only_2026-11-08.zip` contains one `NMS_FSD_Countdown` mod folder with five Wwise Vorbis WEMs for the streamed buildup variants. It uses the same `GAMEDATA/MODS/NMS_FSD_Countdown/AUDIO/WINDOWS/MEDIA` layout on Windows and SteamOS/Proton. It has no bank, charging, jump, Engage, or wind-down replacement. No platform-specific absolute path is stored in the ZIP.

Close the game, remove earlier `NMS_FSD_*` countdown/charging probe folders from `GAMEDATA/MODS`, then extract the ZIP there. Keep unrelated mods. To uninstall, remove only `NMS_FSD_Countdown`. The private build is reproducible with [`tools/build_countdown_release.py`](tools/build_countdown_release.py) using the recovered source WAV, FFmpeg, wav2wem, and vgmstream. The public repository does not distribute the ZIP or source audio.

Charging at HUD 10 requires a different trigger. The matching `Pl_Ship_Warp_Countdown` media are embedded in the persistent soundbank. The user confirmed that an exact-native bank control made with [`tools/build_native_bank_control.py`](tools/build_native_bank_control.py) preserves the custom countdown. Inspection then found a cache identity mismatch in the earlier failed edited-bank probe. A narrower, one-media replacement made with [`tools/build_charging_media_probe.py`](tools/build_charging_media_probe.py) is installed for a gameplay test. Its native random container may place the line at any countdown number; see [STATUS.md](docs/STATUS.md) before treating it as a timing fix.

## Earlier investigation (2026-11-08)

- **Confirmed local installation defect (per Windows agent audit):** Registered mod root `GAMEDATA/MODS/NMS_FSD_SeamlessWarp_MODS_Install` contains another `NMS_FSD_SeamlessWarp` directory before `AUDIO`. NMS expects `AUDIO` directly below the *registered root*. Fix and verify that before changing codecs again.
- **Confirmed in the recovered old 42 MB ZIP:** 23 attempted WEM files with nonstandard `0xFFFE` PCM-like headers (not proven Wwise-runtime compatible). That ZIP is **not** the newest converted build.
- **Later Windows audit, not independently reproduced here:** 23 candidate IDs map statically to the persistent audio bank; the three `Sequence_End` targets were reported *memory resident*, contradicting an “all streamed” characterization. Reconcile per-ID storage and mappings against the installed Forsaken build.
- **Initially unverified:** Converted WEM runtime playback and Forsaken seamless-warp event dispatch. Later stereo and countdown gameplay tests are recorded in [STATUS.md](docs/STATUS.md). A one-file probe replacing a game sound with itself is *not* an audible pass/fail test.
- **Known-positive user observation:** Subnautica PDA exosuit voice replacement works on the same installation. Its localized WEM path does **not** establish that warp SFX event IDs work.
- **Offline custom-WEM milestone:** One 1.5-second private source was encoded as 48 kHz stereo Wwise Vorbis, structurally matched the known native quick-menu WEM layout, and decoded through vgmstream. The original zero-subtype ZIP was silent; the stereo configuration fix was later heard in-game and removed to restore vanilla. See [issue #1 findings](docs/ISSUE_1_STEREO.md).
- **New external lead:** [Unmute Pulse Drive (Forsaken)](https://www.nexusmods.com/nomanssky/mods/4765) notes a soundbank muting interaction and modifies `AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK`. Do not combine competing BNK replacements blindly. [Warframe UI Sounds](https://www.nexusmods.com/nomanssky/mods/4218) describes a known quick-menu open/close loose-WEM replacement: good candidate for an *audibly distinct*, isolated loader probe.

## Historical work order

1. Fix registered mod-root path, preserve unrelated mods, compare installed hashes.
2. Make a one-file in-game **quick-menu opening** diagnostic with a clearly distinguishable sound. Verify the actual media ID and whether the sound is streamed. No ordinary unmodified game WEM as the “probe”.
3. Demonstrate the sound switches back to vanilla when the probe is removed. If no audible change, debug loader / WEM format / bank ownership, not the full warp sequence.
4. Investigate pulse/seamless warp event-to-media dispatch against installed Forsaken banks, and interference from the Forsaken pulse audio muting problem.
5. Integrate the original private source recordings only after a passed gate; assemble and time the FSD voice/countdown/engine event layers.
6. Produce a versioned MODS-compatible ZIP, install/rollback instructions, SHA-256 manifest and game test report (explicitly label any untested result).

## Handoffs

- [Luna High: local NMS host, Linux/Proton or Windows](docs/LUNA_LOCAL_HOST.md)
- [Windows-tower-specific fallback](docs/LUNA_WINDOWS.md)
- [Copilot / Codespaces upstream prompt](docs/COPILOT_CODESPACES.md)
- [Detailed project evidence and suspects](docs/DIAGNOSTICS.md)
- [Linux Wwise Vorbis conversion and quick-menu probe](docs/WEM_VORBIS.md)
- [Private assets / restoration guide](docs/ASSETS.md)
- [Historical mapping information](data/README.md)

## Local paths from previous sessions

- Game (tower): `F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky`
- Workspace (tower): `C:\Users\<YOUR_USER>\Documents\ChatGPT\NMS Modding\NMS_FSD_Working\Build_Sequence`

These are **historical Windows targets only**, not paths to assume on the new Linux machine or in a Codespace. Discover the installed game and Steam library before modifying files.

## Safety, rights, and attribution

This **public** repository holds documentation, metadata, reusable original scripts, and agent instructions only. It deliberately excludes extracted Hello Games game data, persistent soundbanks, the author's Subnautica / Warframe / Unmute mod archives, copyrighted Elite Dangerous recordings, and finished derivative WEM audio without redistribution clearance. Bring required materials into a **private local workspace** for builds; the repository documents hashes/mappings where useful.

Reference resources (do not vendor): [NMSAO](https://www.nexusmods.com/nomanssky/mods/4500), [sound2wem](https://github.com/EternalLeo/sound2wem), [HGPAKtool](https://github.com/monkeyman192/HGPAKtool).
