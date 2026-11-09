# COVAS Verity handoff — 2026-11-09

This is a sanitized research handoff. No extracted game assets, recordings, WEM files, or derivative audio packages are included. The private Windows handoff archive and scan-only package stay outside this public repository.

## Confirmed scan replacement

- Tested on No Man's Sky build `26386568` on Steam Deck / Proton.
- `Pl_Ship_Scanned` (`3802358087`) with streamed media `21310480`, `503523820`, `596880451`, and `634936773` carries the custom “Scan detected” voice.
- User gameplay confirmed the voice during a cargo scan and when Sentinel interceptors scanned the player ship. This supports those observed contexts; it does not prove additional conditions.
- A private scan-only package is installed as the current known-good baseline. It is not included in this public repository because it contains derivative game audio.

## Gear probe result

A temporary phase probe assigned one high tone to `Pl_Ship_Buildable_LandingGear_Start` (`3748782323`) and two low tones to `Pl_Ship_Buildable_LandingGear_End` (`204463560`). The high tone played on occupied Corvette landing and takeoff, on planets and at stations, and during an outdoor summon landing while the player was outside. Earlier voice replacement testing showed the End route on both station landing and takeoff. These are shared gear phase routes, not direction-specific triggers. Gear voice is excluded from release.

The phase probe has been removed from the active mod folder and retained only in the user's private workspace/backups. The current public branch contains no associated WEM assets.

## Other cue decisions

- **Target destroyed:** `NOTIFY_HOSTILES_DEFEATED` did not play for tested Sentinel interceptor kills. The test does not establish player kill attribution; do not substitute this trigger.
- **Shields offline:** local player-ship zero-shield condition remains unverified, and candidate localized media collide with another active mod.
- **Runtime Full:** MBINCompiler and HGPAKtool successfully inspected/round-tripped vanilla globals. These expose static tuning values, not live occupied Corvette identity, gear direction, or summon provenance. No exact-build runtime integration has demonstrated those signals together or a way to layer voice while preserving native gear SFX. No runtime hook was installed.
- **In-game toggles:** not investigated.

## Next steps

Continue Full runtime research only if a build-compatible path can log occupied player ship identity, actual gear direction, summon state, and a safe voice overlay while preserving vanilla gear SFX. Log those conditions in game before adding gear audio. If they cannot be demonstrated, keep both gear voices excluded. Preserve the scan-only baseline and unrelated mods. Do not invent event IDs or infer direction from Wwise event names.
