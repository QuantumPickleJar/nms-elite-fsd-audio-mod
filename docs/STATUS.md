## Portable countdown-only package installed — 2026-11-08

The user reports that “Engaged” is still audible and the prior post-warp replacement plays the wrong engine sound in `/home/deck/Videos/clip_1,794,187,934,288.mp4` and `/home/deck/Videos/clip_1,794,187,875,232.mp4`. They asked to stop work on wind-down and package only the countdown integration for either OS. This supersedes the untested completion-probe status below.

The installed five-second buildup WEM has a strong audio waveform match at 10.440 s in the 62.085 s video (correlation 0.543) and at 9.938 s in the 66.798 s video (0.434). The recovered “4” onset is one second into that WEM, and the cockpit HUD shows 4 at roughly 11.5 s and 11.0 s respectively. The charging WEM also matches both recordings at 3.389 s and 2.984 s (correlations 0.254 and 0.295 in magnitude). These observations support retaining the existing cue timing; exact perceived voice onset is still a listening judgment.

The earlier buildup included source 13.55–17.42 s, overlapping roughly 70 ms of the recovered Engage onset near 17.35 s. `tools/build_countdown_release.py` stops at 17.30 s and fills the remainder of the same five-second cue with silence. The previously installed `Hyperspace_End` wind-down and all other end-event overrides are removed. The 2.2-second delayed charging WEM is byte-identical to the previous working candidate. The package itself has no Engage audio; an audible remaining Engage could be native game audio and has not been isolated.

Private `NMS_FSD_Countdown_Portable_2026-11-08.zip` (SHA-256 `e49469f0f017381ed42f757dc2499433d7f390134e9a1a4eb298c655d2e2b113`) contains one `NMS_FSD_Countdown` MODS root, 15 Wwise Vorbis WEMs, and no BNK or platform-specific paths. Both cues decode at 48 kHz stereo with exact 240000/249600 frames and no clipped samples (peaks 0.824/0.712). With NMS closed, the two previous FSD probe folders were moved to a private backup outside MODS, and all 15 installed WEM hashes were verified. Other mods and saves were unchanged. **This trimmed countdown package has not yet been tested in gameplay.**

## Hyperspace completion wind-down probe installed — 2026-11-08

The user reports that the prior finale still cuts off “Engaged” and does not produce a distinct post-warp wind-down in `/home/deck/Videos/clip_1,794,186,501,513.mp4`. The user authorized omitting “Engaged” temporarily. That gameplay result supersedes the earlier statement below that the finale was awaiting its first test.

The prior finale mapped both Engage and wind-down to the five loose `Pl_Ship_WarpBuildUp_End` media. The current game's `soundbanksinfo.xml` also lists twelve loose, streamed media for `Pl_Ship_Hyperspace_End` (event 3249434187). Two extracted native media from that latter event correlate with the recording at approximately 43.652 s (0.282) and 45.152 s (0.207), near warp completion. This supports `Hyperspace_End` as a completion route; correlation alone does not prove every variant or guarantee the custom cue will survive game mixing. The earlier custom end WEM had no convincing whole-cue match at completion.

`tools/build_hyperspace_end_probe.py` builds private `NMS_FSD_HyperspaceEnd_2026-11-08.zip` (SHA-256 `8cfe25c37b9f343f3d91d1405437b3652f7f76e631e6b997e3bb7b8948e2b585`). It retains the same five-second, +15 dB HUD countdown cue; the new completion cue has 0.5 s silence followed by the original 1.5 s jump/wind-down source at +11 dB with a limiter. There is no Engage excerpt. The cue replaces all twelve `Pl_Ship_Hyperspace_End` loose media, and the old `WarpBuildUp_End` replacements are removed. The delayed charging intro package remains installed. Sources are unchanged.

The ZIP has 17 Wwise Vorbis WEMs, 48 kHz stereo config 0x3102, exact 240000 and 96000 decoded frames, matching manifest hashes, and no BNK. The 21 existing tests pass. With NMS closed, the prior finale folder was moved to a private backup outside MODS and this revision installed; all 17 installed WEM hashes match. Other mods and saves were untouched. **Gameplay playback of the new completion cue is untested.** The next recording should show whether the wind-down is audible after the tunnel and whether it finishes before music.

## Engage and wind-down moved to completion cue — 2026-11-08

The user reports the delayed charging cue is close to final quality, but the “Engaged” word is still cut off near jump and the end/wind-down is masked by other sounds. The 56.257-second gameplay video shows the warp completion display late in the recording and a brief interval before normal cockpit view returns. Audio correlation for the end cue is weak and cannot establish an exact music onset; this is a placement trial guided by the visible completion interval and user listening report.

Private `NMS_FSD_WarpFinale_2026-11-08.zip` (SHA-256 `c416d9722fe6e7651bf83dcdb4c174bec46bb6fee8d31c1a24d9b271bafea206`) retains the HUD-aligned 4,3,2,1 voice arrangement in the five-second buildup, but ends that cue before the source's partial Engage begins. The 3.6-second completion cue is composed from 1.2 s silence, the full recovered 17.35–18.05 s Engage source segment at +12 dB, a 0.2 s gap, and the 1.5 s wind-down/jump recording at +8 dB. The intent is to let other completion effects pass, then speak Engage and finish with a distinct wind-down before music. The WEMs decode to exact 240000 and 172800 frames; peaks are 0.847 and 0.910 with no clipping. The original six WAVs and supplied charging MP3 are unchanged.

With NMS closed, backed up the previous `NMS_FSD_WarpSequence_Probe_EngageTail` outside MODS, installed the new finale root and verified ten exact WEM hashes with no duplicate target IDs. The delayed charging intro probe remains installed. No persistent BNK override, unrelated mod or save was changed. The 21 existing tests and the end-to-end private build/decoder checks pass. Gameplay of this later end cue remains pending; neither full-word audibility nor separation from music is yet confirmed.

## Charging and end-cue refinement installed — 2026-11-08

The user reports the separate charging line plays during the earlier pulse-engagement countdown, wants it when the warp timer first shows 10, hears “Engaged” cut off, and wants the end/wind-down sound another 3 dB louder and separated from jump completion. In the 42.048-second recording, the 3-second charging WEM has its strongest waveform match at video 1.188 s, while visual frames show warp HUD 10 around 3.5 s: a 2.2-second delay is a concrete next timing trial. The buildup WEM matches near video 8.185 s. The end cue's strongest match is less distinct, around warp completion; its placement requires a game test.

Private `NMS_FSD_Charging_IntroDelayed_2026-11-08.zip` (SHA-256 `d4867203463cfbb2e834eb06cd6d2ebd37456beaa6fcd2ac563c8215d8fffe7e`) maps the same complete MP3 phrase to the ten streamed MiniWarp intro media with 2.2 seconds of leading silence. Encoded duration is 5.2 s / 249600 frames. This relies on the intro event continuing to play after pulse engagement; if it stops at warp initiation, the line may be cut or silent. No bank is modified.

Private `NMS_FSD_WarpEngageTail_2026-11-08.zip` (SHA-256 `76340869a871a1765bea6007c07204840d6ec6fca22c1c2953d8ea7a9daaca25`) keeps the prior one-second lead and number timing, but extends the buildup from 5.0 to 5.6 seconds so the source through 18.15 s includes the complete “Engaged” word. It raises the end cue from +5 to +8 dB over source (3 dB increment) and adds 350 ms leading silence after its event to distinguish it from warp completion. Full Wwise Vorbis decode confirms exact 268800 and 88800 frames, peaks 0.879 and 0.883, with no clipping. Event lifetime is still unverified; the extended word may be stopped by the game despite the longer WEM.

With NMS closed, backed up both previous mod roots outside MODS and installed these two new roots. All 20 WEM hashes match the ZIPs, every target ID appears once, and no persistent BNK override is present. Other mods and saves were unchanged. Gameplay audibility/timing remain pending. Do not claim these refinements are confirmed until the next recording.

## HUD countdown alignment and separate no-BNK charging probe — 2026-11-08

The user confirms sound restored after removal of the failed bank diagnostic, but reports that the spoken numbers are disjoint from the on-screen countdown and the full charging line is absent. In the new 43.438-second gameplay recording, the five-second louder buildup has its strongest full-waveform match at video 7.962 s (normalized correlation 0.165); the HUD shows 5 near 8.5 s, 4 near 9.5 s, 3 near 10.5 s, 2 near 11.5 s, and 1 near 12.5 s. Source cue starts at buildup +0.5, +1.5, +2.5, +3.5 s, placing the voiced clips during the preceding HUD numbers. A one-second delay is the smallest whole-number correction supported by this recording; exact perceptual word onset remains a gameplay check.

`NMS_FSD_WarpSequence_HUD_v2_2026-11-08.zip` (SHA-256 `7903d8f26ab25a5361ae4ecfa7928b2166cd0a4e6a986054c32e46e275c4ec00`) uses one second of silence followed by source 13.55–17.55 s. This contains all four recovered one-second number clips, preserves the five-second WEM duration that has played reliably, and keeps the previous +15 dB limited buildup and +5 dB jump settings. The separate end event carries the jump clip. The source’s later engine/Engage tail is excluded from this diagnostic. A sample-level PCM comparison verified the inserted silence and exact source range; the WEM fully decodes to 240000 frames with peak 0.863. It has no BNK.

The supplied MP3 contains the complete charging line in its first 2.5 s. The failed bank attempt remains rolled back. The separate `NMS_FSD_Charging_IntroProbe_2026-11-08.zip` (SHA-256 `3367651c817664e568fb72176d18347aa83d6c60407ae2aeaa2ef9a8cd0834c0`) encodes its first 3 s as a Wwise Vorbis cue and maps it to all ten streamed `Ship_MiniWarp_BuildUp_Intro` variants associated with `Pl_Ship_MiniWarp_Countdown` (event 1348784714). Whether that event fires on the current pulse-to-system route or at HUD 10 is unverified. The probe contains no BNK.

With NMS closed, backed up the last audible mod outside MODS and installed the HUD-aligned package and separate charging-intro probe. All 20 installed WEM hashes match their ZIPs, each target media ID appears once under MODS, and no persistent bank override is installed. Other mods and saves were unchanged. Neither new package has passed gameplay. The next recording should establish whether 4 lands at HUD 4 and whether charging plays at HUD 10, another number, or not at all.

## Bank diagnostic rejected by gameplay; audible package restored — 2026-11-08

The user reports no sound whatsoever with the charging bank diagnostic. This is a runtime regression despite successful Wwiser parsing and offline WEM decoding. The 250 ms advance and additional gain cannot be evaluated from that silent test and remain unproven. The failure does not identify a specific cause: bank override loading, modified event behavior, or bank/media runtime compatibility require isolation. Do not describe the charging-at-ten implementation as working or reinstall it as a playable revision.

With NMS closed, moved `NMS_FSD_WarpCharging_BankProbe` outside MODS to a private rollback backup and restored `NMS_FSD_WarpSequence_Probe_Louder` from the exact ZIP the user previously heard clearly (`NMS_FSD_WarpSequence_Louder_Control_2026-11-08.zip`, SHA-256 694f7977f39f317e507ad99324e670363da569f49415cfa6c661023bae310b2c). All ten installed WEM hashes match, each target ID appears once, and no NMS_AUDIO_PERSISTENT.BNK override remains under MODS. This restores the original five-second arrangement and +10 dB buildup; it does not include the charging sentence or latest timing/gain changes. Other mods, native game files and saves were untouched. Recovered playback after rollback still needs user confirmation.

Next gate: confirm the restored known-audible package plays on the same route. Then change timing/gain independently of any BNK. Before attempting a new modified-bank test, isolate whether an unmodified exact-native BNK override preserves known-positive loose-WEM playback. Successful parsing alone is not an adequate runtime compatibility gate.

## Charging-at-ten persistent-bank diagnostic installed — 2026-11-08

The user supplied an MP3 with the complete “Frame shift drive charging” line and explicitly authorized a separate bank diagnostic, making an exception to the earlier no-BNK constraint. A local speech recognizer identifies the full line within its first 2.5 seconds. Encoded the first 3 seconds as 48 kHz stereo Wwise Vorbis with the proven 0x3102 channel config, +16 dB source gain, 144000 decoded frames, peak 0.712 and no clipping. The downloaded recording and derived media remain private.

Installed-build Wwiser v20260808 analysis identifies countdown event 1026633671 → play action 896412856 → random step container 113103304, selecting among ten approximately half-second embedded ticks. Replacing all ten with the charging sentence would risk repeated lines. The diagnostic changes that container to a step sequence with persistent cursor, replaces its first playlist item's embedded WEM (media 753617385; sound 249399417), and adds ResetPlaylist_E_O action 4000000123 to countdown-end 998544585 and buildup-end 3113682208. This is an experimental way to play charging on the first tick and retain the nine other native tick variants. It relies on game event invocation and end/reset behavior; initial, consecutive-warp and abort/retry playback remain unverified.

The builder refuses any native bank except SHA-256 b725ae4cd02c1556e4054e79c88810e46c35ce36c479793b51573ac7234bdef4. Four existing HIRC objects change; one reset action is added (46767 → 46768 objects). Other HIRC objects, BKHD and STID remain identical. The original DATA bytes are preserved, with a new aligned media payload appended; only one DIDX entry's offset/size changes. The existing media/cache identity is retained; no codebook UID or compressed packets are patched. Wwiser independently parses the rebuilt bank, including the new reset action, without error fields. All 21 tests pass, including three synthetic bank tests for fingerprint rejection, scope/data preservation and end-reset references.

Private ZIP: `NMS_FSD_WarpCharging_BankProbe_2026-11-08.zip`, SHA-256 ad628eb0e8ff584e321d388b411a70169a252066b6aee521a1a041e603185348. It includes the ten byte-identical WEMs from the latest 250 ms advance/+5 dB adjusted package plus one modified persistent bank. With NMS closed and no competing persistent-bank override found, backed up the adjusted mod outside MODS and installed `NMS_FSD_WarpCharging_BankProbe`. All 11 installed audio hashes match the ZIP and have unique filenames under MODS. No native game file, unrelated mod or save was overwritten. This package must not coexist with another NMS_AUDIO_PERSISTENT.BNK override; remove its entire mod root to roll back. No game assets, recordings or derivative binaries are committed publicly.

## Louder playback confirmed; small countdown advance and gain increase — 2026-11-08

The user confirms the louder five-second control plays clearly, with spoken numbers slightly behind the HUD. In the latest 58.801-second gameplay recording, independent waveform matches for the full buildup, 4, 3, and 1 consistently imply buildup onset at video 9.670 seconds. Frame review at 10 Hz places the HUD change to 4 near 10.6 seconds. Spoken-word development within the source interval contributes perceived lag; a 250 ms advance is a trial correction, not a precisely established perceptual offset. The consistent match near HUD 5 contradicts the earlier weak inference of buildup onset at HUD 10. Do not add a five-second delay again on that evidence.

The private `NMS_FSD_WarpSequence_Adjusted_2026-11-08.zip` (SHA-256 `ed0f6a6536dee8c17ad203e141a680871ee2c00c9917279fe7394a5d17d9efd2`) advances buildup content 12000 frames and pads its end with silence to preserve the proven 240000-frame duration. Buildup gain is now +15 dB over source (+5 dB over the last audible version), with peak limiting; the jump clip is +5 dB over the last audible version. Decoded peaks are 0.895 and 0.653, with no clipped samples. Packet framing, exact 240000/72000 decoded frame counts, ZIP integrity and paths passed validation. With NMS closed, backed up the previous louder mod outside MODS and installed `NMS_FSD_WarpSequence_Probe_Adjusted`; all ten installed hashes match and each target ID appears once. No BNK, unrelated mods, or saves changed. Gameplay of this adjustment remains pending.

The user requires the full “Frameshift drive charging” phrase at HUD 10, and will supply a local MP3 because the six recovered sources have no verified complete copy. This remains pending source delivery and an earlier trigger: the current buildup event plays near HUD 5. The current Warp_Countdown and Countdown_End media are memory-resident, so merely adding loose WEMs for them cannot implement the charging phrase. Do not label the current package as containing that line.

## Retimed probe silent; restore audible arrangement with gain only — 2026-11-08

The user subsequently authorized management of the game MODS folder before tests. With NMS closed, moved the silent `NMS_FSD_WarpTimed_Probe` outside MODS to a timestamped private backup, installed `NMS_FSD_WarpSequence_Probe_Louder`, and verified all ten installed hashes against the louder-control ZIP with no duplicate media IDs. Other mods and saves were not modified. Game playback of this gain-only control is pending.

The user reports no custom cues with the 10-second retimed v2 probe. Read-only inspection confirms all ten installed WEM hashes match that ZIP, one copy per media ID, and `NMS_FSD_WARPTIMED_PROBE` enabled in game settings. Both the audible 5-second and silent 10-second versions have stereo config 0x3102 and codebook UID 0x20CEF588. No codebook fields were altered. This does not establish the cause: event lifetime, timing, media-specific behavior, or other runtime conditions remain possible. The prior video correlation of only 0.088 is insufficient to establish a five-second adjustment; treat that offset as unconfirmed. Speech recognition of the charging fragment was inconsistent and does not establish a usable full charging line.

Prepared a private gain-only control, `NMS_FSD_WarpSequence_Louder_Control_2026-11-08.zip`, SHA-256 `694f7977f39f317e507ad99324e670363da569f49415cfa6c661023bae310b2c`. It restores the exact source interval and five-second buildup duration the user heard, raises only buildup by 10 dB, and retains byte-identical jump WEMs from the audible package. No intro or delay is added. All ten paths, hashes, packet framing and exact decoding passed offline checks; no BNK is included. No installed files were changed. Remove the timed probe before installing this control. A fresh video of the louder original arrangement is needed before making another timing change.

## Gameplay video timing and louder probe — 2026-11-08

The user heard the sequence diagnostic but reports low volume, incorrect timing, and no “frameshift drive charging.” The 14.786-second video `/home/deck/Videos/clip_1,794,178,988,371.mp4` contains stereo 48 kHz audio. Half-second frame review places the on-screen warp timer 10 near video 3.5–4.0 s, 5 near 8.5–9.0 s, and 1 near 12.5–13.0 s. A full-sequence cross-correlation against the recorded audio peaks at about video 4.037 s, but normalized correlation is only 0.088 because of game mixing/processing; this is an approximate alignment, not an isolated speech detection. With the prior package's source 4 cue at +0.5 s, the custom numbers appear approximately five seconds early relative to the HUD. The separate jump clip correlation is also weak, so its event timing needs another game test.

The previous source excerpt began at 13.050 s and excluded the long recording's start, where a speech recognizer inconsistently detects a “charging” utterance. No complete “frameshift drive charging” phrase has been verified in the six recovered WAVs; there is no dedicated source clip for it. The new private `NMS_FSD_WarpTimed_Probe_v2_2026-11-08.zip` (SHA-256 `7f525c77b11f23635b6a8c4342a0ef4b3ef226b5511e2f1254b17b32e4bc5f34`) combines long-source 2–7 s and 13.05–18.05 s into a 10-second buildup WEM, placing 4, 3, 2, 1 at buildup +5.5, +6.5, +7.5, +8.5 s. It boosts buildup by 10 dB and jump by 7 dB. The source WAVs remain unchanged. Decoded peaks are 0.859 and 0.828, with no samples clipped; all WEMs decode to exact 480000/72000 frames. Ten streamed loose target paths, ZIP integrity and hashes passed offline checks; no BNK is included. The package is uninstalled and untested in game. Test it alone after removing the previous sequence probe, then report whether the charging phrase or only a fragment is audible and whether 4–3–2–1 aligns with the HUD.

## Warp sequence probe prepared after tentative buildup cue — 2026-11-08

The user reports a possible custom sound near five seconds remaining in the warp countdown with the isolated five-variant `Pl_Ship_WarpBuildUp` probe. Its character was hard to distinguish, so event dispatch remains tentative. A new private `NMS_FSD_WarpSequence_Probe_2026-11-08.zip` (SHA-256 `184d932d13b9cd35a575cd7bb908032479e6fad7b6597dd7d434cac684ec6bdd`) maps a derived 5.000-second excerpt from the original 34.55-second recording to all five streamed `Pl_Ship_WarpBuildUp` media and the separate original 1.500-second jump clip to all five streamed `Pl_Ship_WarpBuildUp_End` media. The excerpt spans source 13.050–18.050 seconds, placing the recovered 4, 3, 2, 1 onsets 0.5, 1.5, 2.5, 3.5 seconds into it. This is an event/timing diagnostic, not a validated final arrangement. All six recovered source WAVs remain unchanged.

The converter is `tools/build_warp_sequence_probe.py`. Offline validation confirms 10 Wwise Vorbis WEMs, 48 kHz stereo config 0x3102, exact 240000/72000 PCM frames, full packet framing and vgmstream decode, correct MODS-root paths and hashes, and no BNK. `Pl_Ship_Warp_Countdown`/`_End` media are memory-resident in the current bank, so the probe does not replace those bank-resident sounds; the audible numbers in the excerpt come from the recovered long source recording. The new ZIP has not been installed or game-tested. Before the next test, remove the earlier five-variant buildup probe from MODS to avoid duplicate media IDs.

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
