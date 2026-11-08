# Recovered exact audio cue offsets — 2026-11-08

## Important distinction

The precise times below are **positions in the recovered 34.55-second private PCM recording**, *not* offsets from No Man's Sky's Forsaken warp initiation. Previous handoffs preserved only clip durations, not these offsets. Reconstructed during the current analysis by matching short recovered clips to the same longer recording; offsets are direct sample-index matches at 48 kHz. The numeric voice labels follow their temporal 4→3→2→1 sequence but have not been independently transcript-verified.

| Intended cue | Absolute offset (s) | Source clip SHA-256 prefix | Isolated clip duration (s) | Samples at 48 kHz | Relative to jump |
| --- | ---: | --- | ---: | ---: | ---: |
| 4 | **13.550** | `7e7e7fd5cf16` | 1.00 | 650400 | −4.500 |
| 3 | **14.550** | `b897d2f1df29` | 1.00 | 698400 | −3.500 |
| 2 | **15.550** | `99aa3a1f7584` | 1.00 | 746400 | −2.500 |
| 1 | **16.550** | `f86691e5b4c1` | 1.00 | 794400 | −1.500 |
| Jump/transition clip | **18.050** | `e66530bbbade` | 1.50 | 866400 | 0.000 |

The long/reference clip is `audio_sources/clip_034.55s_75985ea7b6a8.wav`. The source's isolated `Engage` onset **was not preserved** as a separately identifiable recording and has **not been measured**. Do not invent its timestamp or conflate it with the 18.05-second jump clip.

## Reproducible reconstruction

The five short WAVs were recovered losslessly from the legacy 23-WEM pseudo-WEM package, and the long WAV from the same package. For each short clip:

1. Read stereo 48kHz PCM source audio and the 34.55s long audio via a WAV reader (e.g., soundfile).
2. Average channels for alignment, then compute full cross-correlation of the short clip against the long reference in its expected region using `scipy.signal.fftconvolve(base, short[::-1], mode='valid')`.
3. The maximizer's sample index divided by 48000 produces the precise start time. The five exact offsets are `650400, 698400, 746400, 794400, 866400` samples, respectively.
4. Normalized correlations were ~0.9904, 0.9885, 0.9912, 0.9836, 0.9963. Small mismatches are expected from previously processed audio; these are nonetheless unambiguous exact sample-grid alignments.

These are **reconstructed historical source-clip placements**, not proof that the legacy 23 sound ID targets represent currently dispatched Forsaken seamless-warp events. In-game sequencing and offset-to-jump alignment must be measured after a genuine custom WEM plays successfully.

## Codex handoff

**Preserve** the originally derived countdown alignment: voice 4/3/2/1 at jump-minus-4.5 / -3.5 / -2.5 / -1.5 seconds; impact at jump zero. The previous 34.55-second engine track requires new event-aligned editing. No custom `Engage` asset or exact start offset is proven. Do not bulk-convert 23 targets before the quick-menu codec gate passes.
