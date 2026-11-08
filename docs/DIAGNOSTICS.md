## Linux custom Wwise Vorbis probe — 2026-11-08

### Converter evaluation

- The Steam Deck has FFmpeg 8.1.2 and FFprobe; its FFmpeg build includes the libvorbis encoder. Python 3.14 is present. Rust, Cargo, Go, Wine, vgmstream-cli, ww2ogg, and revorb were not in PATH. NMSAO and HGPAKtool were not found on this host.
- LambdaEd1th/wem-audio is a Rust WEM library under AGPL-3.0-or-later, not a standalone CLI. Its Vorbis writer emits a 24-byte fmt chunk followed by a separate vorb chunk. Its source therefore does not match the current NMS donor's 66-byte fmt plus hash and data chunks. Its tests cover its own conversions; Rust/Cargo were absent, and the project was not selected for this probe.
- pas2k/wav2wem is a Go converter under GPL-2.0. Its source targets modern Wwise Vorbis with a 66-byte fmt chunk, hash chunk, modified packets, external aoTuV 6.03 codebooks, and a seek table. The pinned commit's Go tests pass. Its direct WAV/FLAC path invokes an embedded oggenc2.exe, which fails on this Linux host with exec format error.
- A working Linux path is FFmpeg libvorbis to temporary Ogg, then wav2wem on that Ogg. wav2wem accepts Ogg input without re-encoding and uses its WEM repacketizer. No Wine or Wwise installation was used. FFmpeg created a 48 kHz, 2-channel, quality-6 Ogg from the private source.
- The author's sound2wem workflow sets Wwise Console conversion to Vorbis Quality High; the script is Windows CMD-based and requires Wwise Console. It remains a valid reference workflow, but it is not a Linux-native option on this Deck.

### Encoded output and reference comparison

- One private 1.5-second source was converted. The remaining 23 target IDs were not processed.
- The resulting WEM is 25,236 bytes. It reports Wwise codec tag 0xFFFF, a 66-byte fmt chunk with 48 bytes of Wwise extension data, 2 channels, 48 kHz, 72,000 PCM frames, and chunks fmt/hash/data.
- The private native quick-menu reference also has codec tag 0xFFFF, 66-byte fmt, stereo 48 kHz audio, and chunks fmt/hash/data. These matching outer fields are the current NMS structural basis for the probe.
- vgmstream reported “Custom Vorbis”, 48 kHz, 2 channels, 72,000 samples, and 1.500 seconds, then decoded the WEM to a WAV successfully. This proves a valid decodable Wwise Vorbis stream; it does not prove NMS runtime acceptance.
- Some internal header values differ from the native reference: subtype/channel metadata is 0x00000000 vs 0x00003102, and codebook UID is 0x20CEF588 vs 0xEC69CB18. wav2wem documents its field research as based on a corpus whose structurally matched sample configuration is mono/24 kHz. The meaning and NMS runtime effect of these values are not established here. The diagnostic preserves converter output rather than patching unknown fields by guess.

### Diagnostic package

- The private ZIP replaces all four known streamed UI_Quickmenu_Open IDs (84247370, 544349961, 750436623, 794331107) with the same custom WEM.
- Its root contains AUDIO/WINDOWS/MEDIA directly, plus a test readme and a generated manifest. It contains no BNK.
- The package is local-only and omitted from Git. It must be tested with the earlier FSD, PCM16, and quick-menu probes disabled so only this one variable is active.
- Offline parser/package tests pass. The user will perform the Steam Deck playback and removal/restore check. No game files or other mods were changed during preparation.

Reproduction and tool details are in WEM_VORBIS.md.

---

## Steam Deck custom-WEM decode failure — 2026-11-08

### Observed
- User tested locally on Steam Deck and reported **quick-menu opening went silent** when the four proven quick-menu IDs were all overridden with the 1.5-second converted custom FSD file. The same four slots audibly played an unmodified native game WEM in the previous positive control.
- Local byte comparison: native successful donor `84247370.wem` in `NMS_FSD_SteamDeck_QuickMenu_All4_Audible_Control_2026-11-08.zip` is 25,903 bytes, RIFF tag `0xFFFF`, `fmt` size 66, chunks `fmt/hash/data`; failed custom donor `84247370.wem` in `NMS_FSD_Deck_CustomWEM_Decode_Probe_2026-11-08.zip` is 288,064 bytes, RIFF tag `0xFFFE`, `fmt` size 24, chunks `fmt/JUNK/data`, PCM16 48 kHz stereo.
- `0xFFFE` means WAVEFORMATEXTENSIBLE: its `cbSize` in the failed file is `6`, below the **required 22 bytes** that describe valid bits, channel mask and subtype GUID. Therefore the file is an invalid WAVEFORMATEXTENSIBLE representation, not a demonstrated Wwise Vorbis encoding. See https://learn.microsoft.com/en-us/previous-versions/dd757713(v=vs.85).
- Independently inspected **all 181 WEMs** in the user-uploaded working `Subnautica PDA Exosuit Voice-3893-1-1-1762025763.7z`: every WEM has RIFF tag `0xFFFF` and `fmt` chunk size 66, with `AUDIO/WINDOWS/MEDIA/ENGLISH(US)/<id>.wem` paths. The author's published workflow uses `sound2wem` and therefore real Wwise Console: https://www.nexusmods.com/nomanssky/mods/3893 and https://github.com/EternalLeo/sound2wem .
- The separate `Warframe UI Sounds` mod author documents loose SFX WEMs under `AUDIO/WINDOWS/MEDIA` (https://www.nexusmods.com/nomanssky/mods/4218); the `Unmute Pulse Drive` mod edits the persistent **BNK** for a distinct Forsaken muting issue (https://www.nexusmods.com/nomanssky/mods/4765), not the solution to an invalid WEM header.
- Prior community report with nearly identical symptom required changing Wwise conversion from default PCM to **Vorbis**: https://www.reddit.com/r/NoMansSkyMods/comments/xb4p84/ . Corroboration only; still verify with a new in-game pass.

### Updated priority
1. **Do not run the existing 23 PCM16 files again.** Their container format is the leading proven defect. Do not merely change `.wav` filename to `.wem`, change RIFF tags by hand, or repackage the old bytes.
2. Use a **genuine Wwise Console conversion**: `sound2wem` with `--conversion:Vorbis Quality High`, 48kHz and target channel count as appropriate, or verified Wwise authoring conversion settings. Requires Wwise installation/availability on an appropriate machine; Linux Steam Deck can still run the game and test a WEM produced elsewhere.
3. Re-encode just **one** privately recovered FSD WAV, then place that genuine new WEM in **all four** known quick-menu opening slots (disable all other FSD/quick-menu probes while testing). Pass gate: audible replacement on Steam Deck. If still silent, inspect Wwise version/conversion/decoder and test the new WEM metadata against the proven reference before scaling.
4. Once that passes, identify **actual Forsaken seamless pulse-to-system warp event IDs**, which remain unverified. Only then convert the complete 23 sound map as needed and synchronize 4→3→2→1 + FSD engine. Don't mistake successful quick-menu codec testing for proof the warp event IDs are right.
5. Keep the author's third-party WEMs, source recordings and any licensed derivative audio out of this **public** repository; commit only procedural metadata, code, hashes and test outcomes.

---

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
