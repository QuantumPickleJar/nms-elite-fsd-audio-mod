# Historical metadata only

This directory records the **pre-conversion, silent 23-WEM ZIP** from the earlier ChatGPT Library, not the most recent Windows build and not proven Forsaken event assignments.

- Reference original ZIP: `NMS_FSD_SeamlessWarp_MODS_Install.zip`, 42,279,062 compressed bytes; SHA-256 `050425aea1b7c1f73949e9261378f9445053e5e318e2ba7983d1d709b0feb0ae`.
- Each file was at `NMS_FSD_SeamlessWarp/AUDIO/WINDOWS/MEDIA/<wem-id>.wem` inside ZIP. All old WEM containers had format tag 0xFFFE, 24-byte fmt chunks, 48 kHz stereo PCM24 data and were not decoder-verified. This does not describe the newer converted build.
- Six unique PCM payloads, reused across 23 decimal filenames (4x ~34.55 s; 3x ~1.50 s; 16x ~1 s).
- `legacy_wem_mapping.json` preserves **historic media IDs and source-audio hashes only**; it does not imply event dispatch or functional replacement.
- Six recovered WAV recordings (~10.7 MB handoff archive) and the 23 original WEM binaries are intentionally excluded because they are based on extracted proprietary game sound material. Import privately before using.
- Most recently reported installed FSD layout was nested one extra level below registered `GAMEDATA/MODS` mod root. Do not confuse incorrect packaging with a verified codec/event failure.

For authoritative current mapping, the Windows agent must extract and inspect the installed *Forsaken* `NMSARC.audio.pak` and `NMSARC.audioBNK.pak` and log actual triggered events.
