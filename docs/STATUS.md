## Steam Deck breakthrough — 2026-11-08

**Confirmed by user, with an 8.09-second gameplay clip showing the in-game quick menu:** No Man's Sky launched **locally on Steam Deck** (separate network from Windows tower); after installation of the four-variant quick-menu diagnostic, opening the quick menu audibly played a mini-warp/pulse-engine wind-up in place of its ordinary opening effect. This is the first observed successful **SFX loose WEM replacement under SteamOS/Proton** in this project.

- Probe package: `NMS_FSD_SteamDeck_QuickMenu_All4_Audible_Control_2026-11-08.zip`, four streamed quick-menu variants `84247370`, `544349961`, `750436623`, `794331107` replaced with the **native current-game** donor WEM. This verifies the mod-root layout and playback of **native encoded media**, NOT decoding of the project's custom PCM16 `0xFFFE` WEMs.
- Host/Deck game build, mod config, and installed file hashes were not independently audited during this successful gameplay test. Other FSD target-event IDs remain unverified.
- **Next A/B test:** Exit NMS, remove/disable the quick-menu probe (keep rollback), install the already prepared corrected-root, no-BNK 23-WEM FSD diagnostic and try exactly the requested **pulse-to-system seamless warp**, noting whether custom countdown and engine sounds play.
- **If FSD 23-WEM test remains unchanged:** Use the already-proven quick-menu event as a codec control by substituting one of the exact PCM16 custom WEMs as the quick-menu sound. This distinguishes custom-WEM runtime decoding from a wrong seamless-warp event-ID mapping. Do not modify any persistent BNK until necessary. Explicitly test one variable at a time.
- Only after WEM decoding **and** triggering of actual seamless-warp event IDs are verified should the 4-3-2-1 and engine timing be finalized.
- No finished FSD game release yet. The Deck playtest result is a user-observed success for the loader control, not the FSD sequence.

---

# Project status

**2026-11-08 — Windows host audit complete; no game-tested FSD release yet.**

- Canonical upstream: https://github.com/QuantumPickleJar/nms-elite-fsd-audio-mod
- Audit host: WAYBACK-MACHINE, Windows tower. The newer Linux-like computer and the shared Codespace were not inspected in this run.
- Repository state audited: main at 03cebd5985a97667d3d1793c39e2a8af765c2798.
- Installed game: Steam app 275850, build 26386568; NMS.exe version 184271; root F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky.
- GCMODSETTINGS.MXML confirms DisableAllMods=false and the registered FSD mod enabled at priority 1.
- Confirmed install defect: the registered root NMS_FSD_SeamlessWarp_MODS_Install lacks a direct AUDIO folder; its AUDIO tree is one level deeper under NMS_FSD_SeamlessWarp.
- All 23 installed converted WEMs match the local PCM16_Install files by SHA-256. They use RIFF/WAVEFORMATEXTENSIBLE tag 0xFFFE; game decoding remains unverified.
- The nested FSD package includes a modified NMS_AUDIO_PERSISTENT.BNK. It is the only BNK found in active MODS; it was not tested or changed and is excluded from the no-bank diagnostic package.
- Current soundbanksinfo.xml resolves UI_Quickmenu_Open (4258157981) to four streamed loose variants. The one-file diagnostic replaces only 84247370 (UI_Quickmenu_Open_04) with current-game native WEM 1026697357 (Ship_MiniWarp_Jump_01). Its variant selection needs repeated playback.
- Private local packages now exist for (1) the exact 23-WEM set with no BNK and corrected registered-root layout and (2) the one-file quick-menu audible control. Neither has been installed or game-tested; they are intentionally absent from this public repository.
- Available locally: Python 3.12, FFmpeg/FFprobe, NMSAO 0.1.0, HGPAKtool. NMSAO is a project organizer/importer, not an audio editor or creator. Wwise Authoring/Console was not found in PATH or standard Audiokinetic Program Files locations; no custom WEM encoding path is verified.

**Current state: NO GAME-TESTED RELEASE.** No FSD package was installed and no in-game playback was auditioned during the audit. No game or MODS files were written.

## Next steps

1. Back up the current FSD folder outside MODS and test the private 23-WEM package at the registered root with no persistent BNK present.
2. If the FSD warp remains unchanged, test the one-file quick-menu package with baseline / installed / removed playback and record what was heard.
3. Do not bulk-convert audio until a distinct replacement has been heard. If the quick-menu control passes, resolve Forsaken pulse/seamless-warp event-to-media dispatch and BNK ownership before rebuilding the sequence.
4. Keep private WEMs, banks, Nexus assets, recordings and finished derivative packages out of this public repository.

Private media/assets must never be put into this repository. Only report steps that actually executed.