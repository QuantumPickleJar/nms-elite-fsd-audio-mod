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