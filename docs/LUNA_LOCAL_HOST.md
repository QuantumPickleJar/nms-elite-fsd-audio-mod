# Luna High prompt — local NMS host (Linux/Proton or Windows)

**First inspect the operating system. The user's newer machine is a Windows-like Linux distro, not necessarily Windows.** The older tower previously ran Windows with an F: game library; do not assume either OS or path applies on the current host. Determine which machine actually has the playable No Man's Sky install.

## Objective

Repair and audibly validate a *No Man's Sky Forsaken seamless pulse-to-system warp* sound replacement that uses Elite Dangerous FSD-style engine audio and the COVAS **4, 3, 2, 1** countdown. Current 23-WEM conversions produced **no noticeable in-game changes**. Do not bulk-convert until a single changed sound is heard.

Canonical public repo: https://github.com/QuantumPickleJar/nms-elite-fsd-audio-mod. Pull/read `README.md`, `docs/DIAGNOSTICS.md`, `docs/STATUS.md`, `docs/ASSETS.md`, `data/legacy_wem_mapping.json` before acting. This repo is for source/metadata/handoff; do **not** commit copyrighted game audio, author-supplied Nexus media, finished derivative WEMs or BNKs to it.

## Environment-sensitive discovery

**On Linux (likely new machine):**
1. Get distro/version, desktop session, Steam install method (system, Flatpak or other), NMS app ID / Steam library roots, and whether NMS launches via Proton. Confirm game is installed *here*, not just on older Windows tower.
2. Locate actual NMS `GAMEDATA/MODS` and `Binaries/Settings/GCMODESETTINGS.MXML` under the detected Steam library; follow case-sensitive paths. Do not use `F:\...` on Linux. If game is not installed locally, restrict to offline upstream work and hand off game testing to the actual host.
3. Identify available audio tooling: Python/FFmpeg, NMSAO/HGPAKtool, soundbank inspection, and a *verified* Wwise conversion path. Wwise Authoring for Windows does not automatically work natively on Linux; assess compatible Wine/Proton workflows without promising they work or installing untrusted software. Prefer Windows host for any necessary Wwise GUI step if not reliably available.
4. Never overwrite Steam/Proton configuration, game files, or unrelated mods. Keep rollback copies in separate work directory.

**On older Windows tower (if this is the active game host):**
- Historical NMS root: `F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky`.
- Historical build dir: `C:\Users\<YOUR_USER>\Documents\ChatGPT\NMS Modding\NMS_FSD_Working\Build_Sequence`.
- Verify paths and actual game build, do not assume they still exist.

## Root cause to fix first

Earlier Windows agent observed FSD mod registered at `GAMEDATA/MODS/NMS_FSD_SeamlessWarp_MODS_Install` but `AUDIO` was nested one level further at `NMS_FSD_SeamlessWarp/AUDIO`. Verify current actual mod registration and correct to `<registered mod>/AUDIO/WINDOWS/MEDIA/<mediaID>.wem`. The older Subnautica PDA exosuit voice mod plays correctly, indicating that at least *some* replacement audio works in this installation. Do not infer SFX loader or event behavior from voice success.

## Strict diagnostic gates

1. Audit game version, active MODS, config, overlap priorities, file hashes, 23-WEM current release and any persistent BNK overrides. Preserve other mods and user saves.
2. Correct only the FSD install-root nesting. Retest **latest converted** FSD build with no conflicting persistent BNK. The GitHub legacy mapping refers to the **older 42MB pseudo-WEM ZIP**, not a newer converted 77.8MB revision. Do not use stale hashes to validate current files.
3. If still silent, prove a **one-file deliberately audible quick-menu opening** SFX replacement. The Warframe UI Sounds mod documents this use case. Identify a *real current Forsaken streamed media ID* and replace it with a distinctive short sound encoded in a game-compatible Wwise format. A vanilla WEM copy is NOT an audible test. Complete on/off game playback check and log heard result. Do not choose a sound muted by Forsaken as the first test.
4. Only after the control passes, determine actual pulse-to-system seamless warp event→sound→media linkage using `NMSARC.audio.pak`, `NMSARC.audioBNK.pak`, soundbank metadata and NMSAO/HGPAKtool. Distinguish old MiniWarp, streamed vs embedded memory-resident `Sequence_End` IDs and language paths. NMS.py runtime injection is conditional on exact game-hook version compatibility.
5. Investigate the **Unmute Pulse Drive (Forsaken)** BNK muting issue and any competing bank replacement. Never blindly install a wholesale persistent bank or overwrite another modder's bank.
6. Once the actual event fires and changed audio plays, edit/encode private source recordings to place COVAS 4–3–2–1 before transition, engine rise/impact at jump, appropriate durations/abort behavior. Preserve normal pulse flight and unrelated UI.
7. Package a correctly rooted, **personally transferable** MODS ZIP and SHA256 manifest, with rollback, exact mapping evidence, tests, and clear **game-tested vs untested** labeling.

## Cross-device persistence

User intends to continue from another computer using the repo and optionally https://glorious-acorn-6vqw676w6pg2gw9.github.dev/ (Codespace not yet verified to point at the renamed repo). After each milestone push **copyright-safe source**, tools, sanitized diagnostics, config and `docs/STATUS.md` with exact tested host, game build, path, branch SHA, passed/failed checks, pending action. Use a separate *private* transfer mechanism for locally derived audio clips or finished personal-use binaries: public GitHub repo is not permission to redistribute those.

Prioritize a **real audible A/B proof** over polished-looking but untested packages. If direct in-game testing is unavailable, provide a minimal unmistakable test build and say explicitly that game playback is unverified.
