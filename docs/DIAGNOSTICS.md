# Failure analysis and verification gates — 2026-11-08

## Evidence ledger

| Item | Confidence | Evidence |
| --- | --- | --- |
| Initial mod silent | Confirmed user observation | Neither countdown nor altered engine was audible after install |
| Subnautica PDA exosuit voice mod works | Confirmed user observation | Loose localized WEM mechanism works for at least those IDs |
| Latest FSD mod path nested | Confirmed by Windows agent audit (not directly inspected in Codespace) | `MODS/NMS_FSD_SeamlessWarp_MODS_Install/NMS_FSD_SeamlessWarp/AUDIO` rather than `MODS/<registered root>/AUDIO` |
| Game mods enabled and FSD priority 1 | Reported Windows agent observation | `GCMODSETTINGS.MXML`; inspect exact current settings on tower |
| No competing IDs from other mods | Reported agent observation | compare actual files after reinstall |
| Old archived WEMs invalid/unverified | Confirmed via recovered archive | fmt tag `0xFFFE` with non-standard short extension, PCM payload |
| Newest WEMs 48k stereo PCM16 fmt 0xFFFE | Reported Windows agent observation | Runtime decoding not yet demonstrated |
| Three `Sequence_End` ID targets memory-resident | Reported Windows agent static metadata | Conflicts with broader “all 23 streamed” summary; verify per ID |
| `MiniWarp` IDs fire during seamless pulse warp | **Unknown** | Existing map is only static, not runtime event trace |
| Single-file probe successful | **Unknown** | Agent prepared one using original unmodified WEM, not installed or audible |
| NMS.py event logger compatible with build 184271 | **Unknown** | Agent cited NMS.py release 185034.0 and did not inject |
| Forsaken pulse-drive BNK muting affects current warp | **Plausible, not demonstrated** | Third-party mod author describes mute interaction |

## Priority order

1. **Loader proof**: fix only mod root and verify `<registered_mod>/AUDIO/WINDOWS/MEDIA/<id>.wem` exists at the expected location and file hashes match. If changes are needed, back up FSD files, never reset all mods.
2. **Audible control**: known-in-game quick-menu open/close SFX as evidenced by Warframe UI Sounds description. Resolve its *actual original ID* from current Forsaken; replace ONE streamed file with obviously different, correctly encoded sound. Unmodified stock WEM cannot demonstrate success. Test on/off in game. Don't use Forsaken pulse as first control because audio may be muted.
3. **If control fails**: test known-good mod folder arrangement, correct media codec and Wwise decoding and bank/stream ownership; record what NMS actually loads; do not expand IDs.
4. **If control passes**: verify pulse-drive and new seamless warp event dispatch; inspect `NMSARC.audio.pak`, `NMSARC.audioBNK.pak` and persistent bank HIRC data; use runtime audio event capture ONLY if verified NMS.py/game hook compatibility. Note main menu vs gameplay sound paths may differ.
5. **BNK interaction**: compare `Unmute Pulse Drive (Forsaken)` which modifies `NMS_AUDIO_PERSISTENT.BNK` and is incompatible with other mods replacing same BNK. Use it for private diagnostic comparison, do not blindly merge or redistribute author assets.
6. **Build actual FSD sequence**: only after audible control, use original private samples, precise event timing, countdown 4→3→2→1 and engine crescendo; preserve ordinary pulse and menu audio.
7. **Report**: provide installed file hash list, event-ID provenance, before/after test, negative control, rollback, codec verification, exact version. Label every unperformed in-game test.

## External references (do not vendor)

- NMSAO: https://www.nexusmods.com/nomanssky/mods/4500
- Unmute Pulse Drive (Forsaken): https://www.nexusmods.com/nomanssky/mods/4765
- Warframe UI Sounds: https://www.nexusmods.com/nomanssky/mods/4218
- Subnautica PDA Exosuit Voice: https://www.nexusmods.com/nomanssky/mods/3893
- sound2wem script: https://github.com/EternalLeo/sound2wem
- NMS.py (check compatibility before injection): https://github.com/monkeyman192/NMS.py

## Sound categories

Subnautica PDA exosuit voice replacements are localized (`AUDIO/WINDOWS/MEDIA/ENGLISH(US)`) unlike ordinary sound effects (`AUDIO/WINDOWS/MEDIA`); both operate in Wwise but do not prove the same media IDs or events. Voice/bank-embedded and streamed media cannot be conflated. Resolve each exact ID's property before selecting placement and converter settings.
