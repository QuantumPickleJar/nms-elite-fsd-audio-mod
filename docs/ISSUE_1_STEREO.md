# Issue #1: stereo channel configuration diagnostic

The first FFmpeg/wav2wem stereo Vorbis package FAILED NMS playback: the user heard silence. Installed paths and hashes matched. Offline decoding did not predict runtime compatibility.

## Justified minimal change

The pinned wav2wem function returns 0x4101 for mono and zero for every other channel count. The field at fmt+0x14 is serialized channel configuration. vgmstream documents its modern layout: bits 0–7 channel count, bits 8–11 configuration type, remaining bits speaker mask. Thus stereo standard left/right is 2 | (1 << 8) | (3 << 12) = 0x3102. This independently explains the working native donor value; it is not an arbitrary copied codec tag.

Sources: [pinned writer](https://github.com/pas2k/wav2wem/blob/38e916953bec63862b13b449d780d1303a1bf29c/wem.go), [vgmstream Wwise parser](https://github.com/vgmstream/vgmstream/blob/master/src/meta/wwise.c).

The new experimental diagnostic changes only this four-byte field, with exactly two byte values changing. All other bytes, including codebook UID and compressed payload, remain unchanged. This is a targeted diagnostic rather than a claim that the encoder is now NMS compatible.

## Binary and packet comparison

| Field | Native donor | Failed custom | Subtype candidate |
| --- | --- | --- | --- |
| Codec / fmt | 0xFFFF / 66 bytes | same | same |
| Channels / rate | 2 / 48000 | same | same |
| Channel config | 0x3102 | zero | 0x3102 |
| PCM frames | 77075 | 72000 | 72000 |
| Seek table bytes | 36 | 16 | 16 |
| Setup bytes | 215 | 228 | 228 |
| Audio packets | 121 | 79 | 79 |
| Packet size range | 67–348 | 87–421 | 87–421 |
| UID/common hash | 0xEC69CB18 | 0x20CEF588 | unchanged |

All three files have complete two-byte-length packet framing ending at the data boundary. Native and custom setup packets reference different sets of codebook indices (42 and 44 entries respectively), with some shared indices; different encoding settings may select different books. Equal codec tags or successful framing alone do not validate table compatibility.

## Codebooks investigated separately

The pinned encoder parses every full Ogg codebook and matches it against its bundled aoTuV 6.03 library before writing a 10-bit index. That establishes the relationship between the generated setup and the converter's table. It does not establish the table supported by the NMS runtime. vgmstream can select/fall back between codebook libraries; its successful decoding is insufficient proof of game compatibility. The UID/common-hash semantics are not conclusively established here. Neither a different UID nor a similar index list justifies copying the native UID. No UID or compressed byte was modified.

## Reproduce and validate

Run python3 tools/stereo_subtype_probe.py FAILED_PRIVATE_ZIP OUTPUT_PRIVATE_ZIP. The script requires the exact stereo format, duration, zero configuration, and four identical source WEMs. It writes a new isolated root, four WEMs, README and manifest. It refuses an existing output ZIP.

Thirteen Python tests passed, including byte-preservation and invalid-input tests. The candidate decodes through vgmstream as Custom Vorbis, FL/FR, 48000 Hz, 72000 samples. Its decoded WAV matches the baseline decoded WAV by SHA-256. ZIP contents and all four paths/hashes were validated in private staging. The candidate has not been installed in the game. Existing installed mods and saves were not modified.

## Short Wwise Console fallback

No Wwise Console was found in the checked local tool locations. No speculative Wine or authoring installation was attempted. The shortest established route is the existing Windows tower with Audiokinetic Wwise Authoring including Windows conversion support: privately transfer only the selected WAV, create/open a conversion project containing the Vorbis Quality High preset, then run WwiseConsole convert-external-source against a one-entry wsources list. The current sound2wem helper creates the project and source list and invokes this command; inspect its version/settings before using it:

[Upstream sound2wem command and workflow](https://github.com/EternalLeo/sound2wem/blob/main/zSound2wem.cmd)

Example command on that supported host, with a prepared project and source list:

    WwiseConsole.exe convert-external-source Probe.wproj --source-file one.wsources --output encoded

The one source entry must specify Conversion="Vorbis Quality High". Verify resulting stereo 48 kHz Vorbis WEM with the same inspector/decoder before returning it to Deck. A Wwise-generated WEM still requires the quick-menu game test. The exact runtime-compatible authoring version is not established here.

## One next game test

Exit NMS, move the previous quick-menu diagnostic root entirely outside MODS, and extract the StereoConfig ZIP into GAMEDATA/MODS. Enable the new diagnostic, relaunch, and open the quick menu repeatedly. Report custom cue, silence, or vanilla audio. The root must have AUDIO directly below it; no BNK is included. The issue remains open pending this result.
