# Private asset restoration / Codespaces portability

This is a **public** GitHub repository. Do **not** commit extracted No Man's Sky game files, unlicensed third-party Nexus archives, the Subnautica PDA voice WEMs, unmodified banks, the Elite Dangerous FSD recording/recovered WAVs, or derivative final WEMs without permission.

## Available in earlier ChatGPT handoff, not in Git

- `NMS_FSD_Copilot_Handoff_2026-11-08.zip` (10.7MB) containing `audio_manifest.json`, six PCM WAV sources, `README.md`, `COPILOT_PROMPT.md`. The six WAVs are **reference only, not installable WEMs**; old WEM IDs/hashes are captured in `data/legacy_wem_mapping.json`.
- `NMS_FSD_SeamlessWarp_MODS_Install.zip` (42.3MB) old pseudo-WEM package from ChatGPT Library; **not working**.
- Most recent Windows converted build (reported ~77.8MB) and new diagnostic reports are **not present** in this repo or the present ChatGPT container; retrieve from Windows tower. Do not infer current content/hashes from old ZIP.
- User-downloaded Nexus reference mods: [Unmute Pulse Drive](https://www.nexusmods.com/nomanssky/mods/4765), [Warframe UI Sounds](https://www.nexusmods.com/nomanssky/mods/4218), [Subnautica PDA Exosuit Voice](https://www.nexusmods.com/nomanssky/mods/3893). Local download presence is not established by opening/downloading in a client browser; inspect machine explicitly. Respect mod authors' distribution restrictions.

## Portable handoff

1. Clone this repo on Windows tower or open the Codespace.
2. Keep private sources outside this public clone or under `private/` (ignored by git). Never commit them. E.g. privately copy `audio_sources/*.wav` to `private/source_wav/`.
3. Commit metadata, software, reproducible build configuration, sanitized logs, SHA256 manifests and prompts; do not commit proprietary media.
4. Run build/test on tower where the installed game and Wwise are present. Linux Codespaces generally cannot launch this Windows game or run Wwise authoring tools.
5. For a personal ZIP handoff, use direct Codespaces workspace download or private storage with appropriate rights; do not publish copyrighted game/third-party media to a public release. Avoid leaving unreleased sources in a Codespace if unintended.
6. Write `docs/STATUS.md` or update `docs/DIAGNOSTICS.md` with latest hashes, branch, tested game version, and exact next steps before pausing.

## Paths (historical)

- Game: `F:\Program Files (x86)\Steam\steamapps\common\No Man's Sky`
- Working copy: `C:\Users\<YOUR_USER>\Documents\ChatGPT\NMS Modding\NMS_FSD_Working\Build_Sequence`
- Previously registered (wrong nested root): `GAMEDATA\MODS\NMS_FSD_SeamlessWarp_MODS_Install\NMS_FSD_SeamlessWarp\AUDIO\...`

Do not store per-user Steam IDs or machine-specific secrets in committed reports.
