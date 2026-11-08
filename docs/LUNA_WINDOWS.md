# Luna High prompt — Windows tower, game-side validation

Continue the No Man's Sky Forsaken seamless-warp audio replacement. The objective is a **working, audibly validated** Elite Dangerous FSD engine crescendo with COVAS “4…3…2…1” countdown timed to the actual jump. **Do not start with another blind 23-file rebuild.**

First pull and read https://github.com/QuantumPickleJar/nms-elite-fsd-audio-mod (main), especially README.md, docs/DIAGNOSTICS.md, docs/ASSETS.md and data/legacy_wem_mapping.json. Commit non-proprietary diagnostics and status regularly so work can resume from the user's **second machine, which runs a Windows-like Linux distro**, or a GitHub Codespace. Neither has an assumed F: drive or Windows tools.

## Environment on Windows tower
- NMS game: `F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky`
- Local working dir: `C:\Users\vmorr\Documents\ChatGPT\NMS Modding\NMS_FSD_Working\Build_Sequence`
- Existing repository: `QuantumPickleJar/nms-elite-fsd-audio-mod` (PUBLIC). Verify before any push.
- User can personally test NMS. If autonomous in-game testing isn't possible, create a conspicuous diagnostic sample and clear test instructions; never claim in-game success without a completed listening test.
- Preserve unrelated mods, saves, and installation state.

## Findings to test, not assume
- The previous Windows agent found `GAMEDATA\MODS\NMS_FSD_SeamlessWarp_MODS_Install\NMS_FSD_SeamlessWarp\AUDIO\...` — an extra directory level below the **registered** FSD mod root. `AUDIO` must be directly under the registered root. This may explain all prior silence.
- Mods were enabled; FSD was registered at priority 1; no overlapping active WEM IDs were reported. Re-verify on current installation.
- User's Subnautica PDA exosuit voice mod works: NMS is capable of some loose WEM replacement; voice and SFX may use different media paths and banks.
- Initial archived 23-WEM package was unusable WAV-like pseudo-WEM. A newer converted package reportedly uses 48 kHz PCM16 WEM files but decoding and exact files were never independently checked. **The GitHub historical manifest is for an older artifact only.**
- Previous agent listed all 23 IDs as streamed, but separately called three `Sequence_End` IDs memory resident; investigate this contradiction using actual Forsaken metadata.
- MiniWarp event names are only statically associated with older countdown/jump IDs. Actual *pulse-drive seamless warp* event dispatch is unproven.
- The old 483379598 one-file probe used the **unmodified vanilla sound**; it is not a valid audible positive control.
- Investigate [Unmute Pulse Drive (Forsaken)](https://www.nexusmods.com/nomanssky/mods/4765), which reportedly modifies the persistent BNK to undo muting; do not overwrite an existing BNK or blindly combine with other audio mods.

## Ordered execution and gates

1. **Local audit and backup.** Record game version; enumerate installed FSD mod root, active MODS entries, exact on-disk WEM and BNK hashes, other audio mods, actual config path and flags. Inspect `GAMEDATA\MODS` and the actual `Binaries\Settings\GCMODESETTINGS.MXML` (verify exact casing/spelling on disk). Do not disable or delete unrelated mods.
2. **Fix registered mod-root nesting only.** The intended structure is `GAMEDATA\MODS\<registered FSD mod>\AUDIO\WINDOWS\MEDIA\<id>.wem`. Make an easily reversible backup. Try the latest converted build (not ancient pseudo-WEMs), initially without modified BNK to avoid bank conflicts. Have user listen for changed FSD sound.
3. **If still no difference, prove loose-SFX loading** with exactly one deliberately *different and unmistakable* WEM for a known-triggering, in-game **quick-menu opening sound**. Existing Warframe UI Sounds mod provides a precedent; determine the correct ID from *installed Forsaken*, confirm streamed-media residency and expected loader path, verify Wwise-compatible encoding. Do not use a vanilla WEM as a probe. Capture an A/B positive/negative control: audible when mod present; vanilla when disabled. If the quick-menu ID is unavailable, use another documented frequently triggered streamed UI effect, not an unverified pulse event.
4. **Only after positive control, determine real warp events.** Read currently installed `NMSARC.audio.pak` and `NMSARC.audioBNK.pak`, analyze bank HIRC mappings, streamed and memory-resident WEM IDs; inspect old MiniWarp and new Forsaken seamless warp; use NMS.py runtime event tracing only if the installed game and hook versions are verified compatible. Never inject a mismatched hook blindly.
5. **Isolate BNK muting/memory residency.** Compare behavior and compatibility implications of third-party Unmute Pulse Drive; resolve event-level and bank-level conflicts without overwriting another mod's changes. Where a bank edit is unavoidable, preserve originals and document compatibility; do not distribute third-party bank bytes publicly.
6. **Produce intended FSD replacement.** Encode private recovered FSD recordings with a verified Wwise-compatible method and the stock codec/settings as appropriate. Time the spoken 4, 3, 2, 1 countdown and engine buildup/engage at the actual jump, including repeatable abort/retry if applicable. Preserve other game sounds.
7. **Deliver.** Test plan, versioned MODS-folder ZIP for *private use*, clear install/uninstall instructions, SHA256 ledger, exact media-ID/event mapping with evidence, and the final in-game tested/not-tested status. Save a local transferable build; do **not** commit copyrighted recordings, extracted game WEM/BNK/PAK or third-party Nexus archives to the public repo.

## Cross-device handoff contract
Before concluding or pausing, push readable source code, sanitized mapping data, build scripts, audio processing configs, reproducible procedure, and results to this repo. Update docs/STATUS.md with:
- date, NMS build, commits, current stage and proof status;
- paths and private assets still residing only on Windows tower;
- passed/failed checks (not planned checks);
- precise next command/test and rollback procedure;
- what a Linux/Codespaces Copilot agent can continue without the tower.

Do not claim any release is functional until an A/B in-game sound change was heard or independently captured.
