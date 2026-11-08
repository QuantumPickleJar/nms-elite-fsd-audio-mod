## Verified install, negative warp test, and current-build event mapping — 2026-11-08

The user repeated the pulse-to-system warp with the 23-WEM package installed and heard no custom audio. Immediately before that test, a read-only audit found all 23 files at `GAMEDATA/MODS/NMS_FSD_Warp_StereoVorbis/AUDIO/WINDOWS/MEDIA`, each with the expected ZIP hash and no duplicate target ID. The latest `GCMODSETTINGS.MXML` registered `NMS_FSD_WARP_STEREOVORBIS` with `Enabled=true` and `DisableAllMods=false`. The game log has no audio event trace. This is evidence against a missing installation; it does not alone prove which event fired.

HGPAKtool 1.1.3 extracted `audio/windows/soundbanksinfo.xml` from the installed `NMSARC.audio.pak` for private inspection. All 23 historical media IDs are referenced by `Pl_Ship_MiniWarp_Countdown_02` through `_05` or `Pl_Ship_MiniWarp_Jump`. The current metadata also contains distinct `Pl_Ship_Warp_Countdown` (event 1026633671; 10 memory-resident media), `Pl_Ship_Warp_Countdown_End` (998544585; 5 memory-resident media), `Pl_Ship_WarpBuildUp` (679898858; 5 streamed loose media), and `Pl_Ship_WarpBuildUp_End` (3113682208; 5 streamed loose media). This static mapping suggests the old 23 IDs miss the tested route, but runtime event dispatch is still unverified.

A private diagnostic ZIP, `NMS_FSD_WarpBuildUp_5Variant_Probe_2026-11-08.zip` (SHA-256 `98fc30d21539f2875cca862561df8aa32d634bd5a250d48d0857e645117ba54b`), puts the previously audible 1.5-second custom WEM in all five streamed `Pl_Ship_WarpBuildUp` media slots: 293625877, 317366338, 332067571, 722656460, 978671379. It has direct-root AUDIO, seven entries, no BNK, and is not installed or game tested. Remove the prior 23-WEM folder before installing this isolated probe. If it plays during the same pulse-to-system route, proceed with event-specific timing; the countdown voices still require a separate supported approach to memory-resident media. No game assets or private audio are committed.

The recovered original recording has source offsets 4 at 13.550 s, 3 at 14.550 s, 2 at 15.550 s, 1 at 16.550 s, jump at 18.050 s (48 kHz sample boundaries). Local waveform correlation confirms clip labels at 98.63–99.58%. These are source-recording offsets, not verified Forsaken trigger times; the separate Engage offset remains unknown.

## Stereo fix confirmed; full warp package prepared — 2026-11-08

The user heard the distinct custom rising cue with the subtype-corrected probe, then removed it and confirmed vanilla quick-menu audio returned. This is a successful user-observed A/B test of the stereo configuration fix. The zero-config Vorbis candidate had previously been silent. The codebook UID and compressed stream were unchanged between those candidates.

The user authorized extending conversion to the remaining sounds. All six recovered WAVs were encoded with FFmpeg libvorbis quality 6, wav2wem pinned revision, and standard stereo config 0x3102. Each output passed full packet framing and vgmstream decoding with exact source frame count. A private 23-WEM package preserves the historical mapping and original durations (1s, 1.5s, 34.55s). No precise prior countdown offsets were recovered from the available notes; the user was asked for those while conversion continued. No new trim, delay, or bank timing was guessed. Warp event IDs and sequence alignment still need the seamless-warp game test.

The package has direct mod-root AUDIO/WINDOWS/MEDIA, no quick-menu overrides, and no BNK. No installed mods or saves were changed. Reproduce with tools/build_warp_package.py; output media and manifests remain private.

---

## Issue #1: subtype-only candidate prepared — 2026-11-08

The failed playback result is committed. A new isolated StereoConfig quick-menu ZIP changes only fmt+0x14 from zero to the standard stereo configuration 0x3102. Codebook UID, setup, seek table, and audio packets are unchanged. Thirteen tests passed; packet framing and vgmstream decode passed; decoded PCM matches the failed baseline. All four staged paths/hashes are verified. Candidate gameplay is pending. No installed mod or save was changed. See ISSUE_1_STEREO.md for findings and the Wwise Console fallback. Do not convert the 23 warp sounds.

---

## Quick-menu Vorbis probe: silent — 2026-11-08

- The user reports silence when opening the quick menu with the Linux-generated Vorbis probe installed. A gameplay clip was provided; it contains an audio stream, but the user's report is the playback observation.
- A read-only inspection of the Steam Deck MODS directory found all four diagnostic WEMs at the expected paths, each matching the packaged custom WEM SHA-256. No other copies of those four target IDs or BNK files were found under MODS at inspection time.
- This is a negative NMS runtime result despite successful vgmstream decoding. The differing Wwise extension fields and the converter's stereo output remain possible causes; no single cause is established. Do not expand to the 23 target files. Next investigate an actual Wwise Console Vorbis conversion or a verified stereo encoder against the native reference.

---

## Linux Wwise Vorbis probe — 2026-11-08

- Created branch codex/linux-wem-vorbis-2026-11-08 from clean main; existing repository work was preserved.
- Inspected the private recovered recordings and used only the 1.5-second 48 kHz stereo source for this milestone. The other 23 media targets were not converted.
- FFmpeg 8.1.2 with libvorbis generated a temporary Ogg Vorbis stream at quality 6. Pinned wav2wem commit 38e916953bec63862b13b449d780d1303a1bf29c repacketized it into a Wwise Vorbis WEM. The file has tag 0xFFFF, 66-byte fmt, 2 channels, 48 kHz, 72,000 frames, and fmt/hash/data chunks.
- The custom WEM matched the private native NMS reference's outer RIFF layout. vgmstream identified it as Custom Vorbis and decoded all 72,000 samples to a 1.5-second stereo WAV.
- The WEM header's subtype and codebook UID differ from the native reference. Those fields were not normalized or guessed; their effect on NMS remains unverified. See the Wwise Vorbis conversion notes in WEM_VORBIS.md.
- Prepared a personal-use diagnostic ZIP with the same custom WEM in the four known streamed UI_Quickmenu_Open slots. AUDIO is directly under the ZIP's mod root. The ZIP contains no persistent BNK and is not in the public repository.
- Offline Python tests pass. No game files or installed mods were changed. The user subsequently tested this first build and reported silence.

Result: The first Vorbis diagnostic was silent in the user’s Steam Deck test. A subtype-only diagnostic is the next investigation. Do not convert the remaining 23 files until that test passes.

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

## Steam Deck FSD-path negative test — 2026-11-08

- The user reports **no noticeable audio changes** during a locally launched Steam Deck **pulse-to-system seamless warp**, documented by a 16-second gameplay clip. The clip visually shows the correct warp route and countdown; auditory assessment remains the user's report. This followed the earlier **successful** native-WEM quick-menu test.
- The user also reported that the **latest FSD revision remained in the MODS directory**. Whether multiple active FSD package roots (or a BNK override) competed during this test is **not independently established**. Therefore the negative result does **not** conclusively resolve event mapping vs codec vs package overlap.
- Inspection of the recovered 23-WEM no-BNK path-test archive confirms all 23 copies retain `0xFFFE` WAVEFORMATEXTENSIBLE PCM16 headers (24-byte fmt chunk). This contrasts with the native current-game donor WEM (`0xFFFF`, 66-byte fmt chunk) heard successfully in the quick-menu test. A custom-WEM runtime decode test is still needed.
- Prepared *private, not publicly committed*: `NMS_FSD_Deck_CustomWEM_Decode_Probe_2026-11-08.zip` (~1 MB; SHA-256 `1c709aca8563e1aa5c554f14a7c5c967b59f3c99f5eb5373708249978691625f`). It places **byte-for-byte** former 1.5-second FSD WEM `1026697357.wem` (`edc6a03fe4815f06cc84dfda52ce4976884d7d9fbb83b295eda2aa06dc0ac50e`) in all four known-responding UI_Quickmenu_Open slots (84247370, 544349961, 750436623, 794331107), without a BNK. This is to isolate *custom codec decoding* from *warp event trigger*.
- **Next playtest (Deck):** exit NMS, temporarily move prior FSD and quick-menu probe folders **entirely outside** `GAMEDATA/MODS`; install only the custom decoder probe; relaunch and repeatedly open the quick menu. Report changed custom cue / silence / vanilla. Remove and relaunch for A/B confirmation. Do **not** mark final FSD playable based solely on an unrelated quick-menu control.

---

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
