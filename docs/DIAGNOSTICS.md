# Failure analysis and verification gates — 2026-11-08

## Evidence ledger

| Item | Confidence | Evidence |
| --- | --- | --- |
| Initial FSD mod silent | Confirmed user observation | Neither countdown nor altered engine was audible after install |
| Active host is the Windows tower | Confirmed this run | Host WAYBACK-MACHINE; No Man's Sky Steam app 275850, build 26386568, NMS.exe 184271 |
| Global mods and FSD registration | Confirmed this run | GCMODSETTINGS.MXML: DisableAllMods=false; NMS_FSD_SEAMLESSWARP_MODS_INSTALL enabled, VR-enabled, priority 1 |
| FSD folder nesting defect | Reproduced this run | Registered root has no direct AUDIO folder; files are under NMS_FSD_SeamlessWarp_MODS_Install/NMS_FSD_SeamlessWarp/AUDIO |
| Current converted 23 WEMs | Confirmed by hashes; runtime unknown | Installed files match PCM16_Install byte-for-byte; WAVEFORMATEXTENSIBLE tag 0xFFFE; no in-game decode test |
| Persistent-bank override | Confirmed this run | FSD nested tree contains modified NMS_AUDIO_PERSISTENT.BNK; only active MODS .bnk found; excluded from no-bank test |
| Competing Unmute Pulse Drive bank | Not present in active MODS | No Unmute folder or second .bnk found. The installed FSD bank was not merged, changed, or played |
| Competing loose target IDs | No duplicates outside FSD | Current FSD IDs occur only in the FSD folder; quick-menu target 84247370 has no active override |
| Quick-menu target | Confirmed from installed-build soundbanksinfo.xml | Event UI_Quickmenu_Open (4258157981) references variants 84247370, 544349961, 750436623, 794331107; each is SFX streamed loose media. 84247370 is UI_Quickmenu_Open_04 |
| One-file quick-menu probe | Prepared; not installed/tested | Replaces only media 84247370 with current-game native WEM 1026697357 (Ship_MiniWarp_Jump_01); it is one of four event variants |
| FSD IDs fire during seamless pulse warp | Unknown | Static metadata associates them with old MiniWarp events; no exact-build runtime event capture |
| Three Countdown Sequence_End media | Memory-resident per current static metadata | IDs 145778974, 479895607, 633190263 are not loose streamed media; loose WEM placement cannot replace them |
| Wwise compatibility of PCM16 files | Unknown | Static RIFF inspection cannot establish NMS runtime acceptance |
| NMS.py hook compatible with build 184271 | Unknown | No exact-build matched logger was found or injected |
| Pulse-drive muting cause | Plausible, not demonstrated here | Unmute Pulse Drive author says Forsaken's persistent bank changes mute other streamed sounds; no bank comparison was performed |

## Priority order

1. **Retest the current conversion without the bank.** Preserve the existing FSD folder outside MODS, then use the private 23-WEM no-bank package so AUDIO is directly under the registered root. Do not modify any other mod or reset mod settings.
2. **Record the pulse-to-system result.** A silent result still leaves event dispatch and runtime decoding unresolved because the candidate 23 IDs statically map to older MiniWarp events.
3. **Run the one-file loader control if the warp test remains silent.** The quick-menu-open event is UI_Quickmenu_Open (4258157981). Test only one streamed loose variant, 84247370, using the distinct native Ship_MiniWarp_Jump_01 WEM. Repeat opens because the event references four variants. Record baseline, replacement, and restored-vanilla audio.
4. **If the control fails,** inspect direct loose-media loading, WEM format, bank ownership and audio routing. Do not expand or reconvert the FSD set.
5. **If the control passes,** resolve Forsaken seamless-warp event-to-media dispatch against the current NMSARC.audio.pak, NMSARC.audioBNK.pak and soundbank metadata. Treat old MiniWarp associations as static hypotheses only. Use runtime capture only with an exact-build-compatible hook.
6. **Investigate the persistent-bank conflict** before any BNK change. Unmute Pulse Drive (Forsaken) documents a same-bank compatibility conflict; never install its wholesale bank or the FSD bank blindly alongside another override.
7. **Build the final sequence only after an audible control passes.** Use the private source audio to time COVAS 4-3-2-1 and engine rise/impact, preserve normal pulse flight and unrelated UI, and report exact hashes, rollback, event provenance and game-tested status.

## Local tooling

- Python 3.12 and FFmpeg/FFprobe are available.
- NMSAO 0.1.0 and HGPAKtool are installed locally. NMSAO organizes and imports WAV/WEM replacement projects; it is not an audio editor or WEM creator.
- Wwise Authoring/Console was not found in PATH or standard Audiokinetic Program Files locations. No custom-audio WEM encoding route was verified in this audit. The quick-menu donor is native current-game Wwise media, so no new conversion is required for the loader control.
- Private diagnostic ZIPs are local-only and are deliberately excluded from this public repository.

## External references

- NMSAO: https://www.nexusmods.com/nomanssky/mods/4500
- Unmute Pulse Drive (Forsaken): https://www.nexusmods.com/nomanssky/mods/4765
- Warframe UI Sounds: https://www.nexusmods.com/nomanssky/mods/4218
- Subnautica PDA Exosuit Voice: https://www.nexusmods.com/nomanssky/mods/3893
- sound2wem script: https://github.com/EternalLeo/sound2wem
- NMS.py (check compatibility before injection): https://github.com/monkeyman192/NMS.py

Subnautica PDA replacements are localized voice WEMs. Their success does not prove ordinary UI/SFX IDs or seamless-warp event dispatch. The quick-menu target is an ordinary SFX streamed file; it is a better loader control.
