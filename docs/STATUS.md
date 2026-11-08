# Project status

**2026-11-08 — Source-only handoff; no proven audible FSD mod yet.**

- Canonical upstream: https://github.com/QuantumPickleJar/nms-elite-fsd-audio-mod
- Primary runtime: No Man's Sky Forsaken on Windows tower; user's second computer is a Windows-like Linux distro (distro not specified). A Codespace URL was shared, but the live workspace has **not** been authenticated/inspected by this assistant.
- Published: overview, safety policies, historical mapping for **old** WEM ZIP, failure diagnosis and separate Windows Luna / Linux-Codespaces Copilot prompts.
- Most likely confirmed bug: registered FSD root has accidental nested subfolder; fix path before replacing codecs.
- Independent positive control required: known-triggering in-game quick-menu opening SFX, truly distinct and Wwise-compatible WEM, A/B tested.
- Current converted 23-WEM package and prior Windows diagnostic outputs are still **not** checked into repo and have not been personally inspected in this chat; don't equate them with old manifest.
- Current state: **NO GAME-TESTED RELEASE**. Mod-ready packaging and working event dispatch remain unverified.
- Next Windows action: compare installed FSD registered root to directory containing AUDIO and repair nesting; retest; if no audible change, generate single-file quick-menu audible control.
- Next Linux/Codespaces action: implement and test cross-platform packaging, RIFF inspection, media-ID mapping utilities; document all missing proprietary inputs.

Private media/assets must never be put into this public repository. Only report steps that actually executed.
