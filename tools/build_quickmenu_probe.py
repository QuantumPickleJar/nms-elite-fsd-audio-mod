#!/usr/bin/env python3
"""Build a four-variant, no-BNK Wwise Vorbis quick-menu diagnostic ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

if __package__:
    from .wem_inspect import WemFormatError, inspect_wem
    from .stereo_subtype_probe import standard_stereo_config
else:
    from wem_inspect import WemFormatError, inspect_wem
    from stereo_subtype_probe import standard_stereo_config


WAV2WEM_URL = "https://github.com/pas2k/wav2wem"
WAV2WEM_REVISION = "38e916953bec63862b13b449d780d1303a1bf29c"
MOD_ROOT = "NMS_FSD_QuickMenu_WwiseVorbis_Diagnostic"
MEDIA_PREFIX = f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA"
QUICKMENU_IDS = ("84247370", "544349961", "750436623", "794331107")
EXPECTED_DURATION = 1.5
EXPECTED_RATE = 48000
EXPECTED_CHANNELS = 2
EXPECTED_SAMPLE_FRAMES = 72000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], *, capture: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"required executable not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        details = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(
            f"command failed ({exc.returncode}): {' '.join(command)}"
            + (f"\n{details}" if details else "")
        ) from exc


def probe_audio(ffprobe: str, path: Path) -> dict[str, Any]:
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name,sample_rate,channels",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ]
    )
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    if not streams:
        raise RuntimeError(f"no audio stream found in {path}")
    return {
        "codec": streams[0].get("codec_name"),
        "sample_rate": int(streams[0]["sample_rate"]),
        "channels": int(streams[0]["channels"]),
        "duration_seconds": float(payload["format"]["duration"]),
    }


def require_target_audio(metadata: dict[str, Any], label: str) -> None:
    if metadata["sample_rate"] != EXPECTED_RATE:
        raise RuntimeError(
            f"{label} is {metadata['sample_rate']} Hz, expected {EXPECTED_RATE} Hz"
        )
    if metadata["channels"] != EXPECTED_CHANNELS:
        raise RuntimeError(
            f"{label} has {metadata['channels']} channels, expected {EXPECTED_CHANNELS}"
        )
    if abs(metadata["duration_seconds"] - EXPECTED_DURATION) > 0.002:
        raise RuntimeError(
            f"{label} is {metadata['duration_seconds']:.6f}s, expected 1.5s"
        )


def require_target_wem(path: Path):
    info = inspect_wem(path)
    if info.codec_tag != 0xFFFF:
        raise WemFormatError(f"expected Wwise Vorbis tag 0xFFFF, got {info.codec_tag:#06x}")
    if info.channels != EXPECTED_CHANNELS or info.sample_rate != EXPECTED_RATE:
        raise WemFormatError("output WEM does not have 2 channels at 48000 Hz")
    if info.fmt_chunk_size != 66 or info.fmt_extra_size != 48:
        raise WemFormatError("expected the modern 66-byte Wwise Vorbis fmt chunk")
    if [chunk.tag for chunk in info.chunks] != ["fmt ", "hash", "data"]:
        raise WemFormatError("expected WEM chunks in fmt/hash/data order")
    chunk_sizes = {chunk.tag: chunk.size for chunk in info.chunks}
    if chunk_sizes["hash"] != 16 or chunk_sizes["data"] == 0:
        raise WemFormatError("expected a 16-byte hash chunk and non-empty data chunk")
    if info.total_pcm_frames != EXPECTED_SAMPLE_FRAMES:
        raise WemFormatError(
            f"expected {EXPECTED_SAMPLE_FRAMES} PCM frames, got {info.total_pcm_frames}"
        )
    return info


def reference_comparison(reference_path: Path, info) -> dict[str, Any]:
    reference = inspect_wem(reference_path)
    reference_summary = {
        "codec_tag": reference.codec_tag,
        "channels": reference.channels,
        "sample_rate": reference.sample_rate,
        "fmt_chunk_size": reference.fmt_chunk_size,
        "chunks": [chunk.tag for chunk in reference.chunks],
        "hash_chunk_size": next(
            (chunk.size for chunk in reference.chunks if chunk.tag == "hash"), None
        ),
    }
    output_summary = {
        "codec_tag": info.codec_tag,
        "channels": info.channels,
        "sample_rate": info.sample_rate,
        "fmt_chunk_size": info.fmt_chunk_size,
        "chunks": [chunk.tag for chunk in info.chunks],
        "hash_chunk_size": next(
            (chunk.size for chunk in info.chunks if chunk.tag == "hash"), None
        ),
    }
    fields = (
        "codec_tag",
        "channels",
        "sample_rate",
        "fmt_chunk_size",
        "chunks",
        "hash_chunk_size",
    )
    return {
        "reference_kind": "private current-game native WEM",
        "outer_layout_matches": all(
            reference_summary[field] == output_summary[field] for field in fields
        ),
        "reference": reference_summary,
        "output": output_summary,
        "internal_header_differences": {
            "reference_subtype": (
                f"0x{reference.subtype:08X}" if reference.subtype is not None else None
            ),
            "output_subtype": f"0x{info.subtype:08X}" if info.subtype is not None else None,
            "reference_codebook_uid": (
                f"0x{reference.codebook_uid:08X}"
                if reference.codebook_uid is not None
                else None
            ),
            "output_codebook_uid": (
                f"0x{info.codebook_uid:08X}" if info.codebook_uid is not None else None
            ),
        },
    }


def verify_with_vgmstream(
    executable: str, wem_path: Path, ffprobe: str, temp_dir: Path
) -> dict[str, Any]:
    metadata = run([executable, "-m", str(wem_path)]).stdout
    lowered = metadata.lower()
    if "encoding: custom vorbis" not in lowered:
        raise RuntimeError("vgmstream did not identify the output as Custom Vorbis")
    if "sample rate: 48000 hz" not in lowered or "channels: 2" not in lowered:
        raise RuntimeError("vgmstream metadata does not report 48000 Hz stereo")
    if "stream total samples: 72000" not in lowered:
        raise RuntimeError("vgmstream metadata does not report 72000 samples")

    decoded = temp_dir / "decoded.wav"
    run([executable, "-o", str(decoded), str(wem_path)])
    decoded_metadata = probe_audio(ffprobe, decoded)
    if decoded_metadata["sample_rate"] != EXPECTED_RATE:
        raise RuntimeError("vgmstream decoded to an unexpected sample rate")
    if decoded_metadata["channels"] != EXPECTED_CHANNELS:
        raise RuntimeError("vgmstream decoded to an unexpected channel count")
    if abs(decoded_metadata["duration_seconds"] - EXPECTED_DURATION) > 0.002:
        raise RuntimeError("vgmstream decoded to an unexpected duration")
    return {
        "decoder": "vgmstream-cli",
        "encoding_report": "Custom Vorbis",
        "sample_rate": decoded_metadata["sample_rate"],
        "channels": decoded_metadata["channels"],
        "duration_seconds": decoded_metadata["duration_seconds"],
        "pcm_decode_succeeded": True,
    }


def build_readme() -> str:
    return (
        "NMS Steam Deck quick-menu Wwise Vorbis diagnostic\n"
        "\n"
        "This is a personal-use codec probe, not a finished FSD mod. It replaces all four\n"
        "known UI_Quickmenu_Open streamed variants with the same 1.5-second custom FSD\n"
        "sound. The WEM has a Wwise Vorbis RIFF layout and decodes with vgmstream. NMS\n"
        "runtime playback has not yet been verified.\n"
        "\n"
        "Install and test\n"
        "1. Exit No Man's Sky.\n"
        "2. For an isolated test, temporarily disable or move earlier FSD, PCM16 custom-WEM,\n"
        "   and quick-menu probe folders outside GAMEDATA/MODS. Keep them for rollback.\n"
        "3. Extract this ZIP into the game's GAMEDATA/MODS directory. The package root\n"
        "   contains AUDIO directly; do not put the ZIP itself in MODS.\n"
        "4. Launch the game and open the quick menu repeatedly. Listen for the custom FSD cue.\n"
        "5. For the A/B check, exit the game, move only this package folder out of MODS,\n"
        "   relaunch, and check that the ordinary quick-menu sound returns.\n"
        "\n"
        "This package contains four WEM files, a readme, and a manifest. It contains no BNK.\n"
        "Do not merge it over an existing folder of the same name; move that folder aside first.\n"
    )


def zip_write(zip_file: zipfile.ZipFile, name: str, content: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    zip_file.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def expected_archive_paths() -> set[str]:
    return {
        *(f"{MEDIA_PREFIX}/{media_id}.wem" for media_id in QUICKMENU_IDS),
        f"{MOD_ROOT}/README_TEST.txt",
        f"{MOD_ROOT}/PROBE_MANIFEST.json",
    }


def validate_archive_paths(paths: list[str]) -> None:
    actual = set(paths)
    expected = expected_archive_paths()
    if any(path.lower().endswith(".bnk") for path in actual):
        raise RuntimeError("diagnostic ZIP must not contain a persistent BNK")
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise RuntimeError(f"unexpected ZIP layout; missing={missing}, extra={extra}")
    for path in actual:
        if path.startswith(f"{MOD_ROOT}/AUDIO/") and not path.startswith(
            f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA/"
        ):
            raise RuntimeError(f"AUDIO is not directly below the mod root: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-wav", required=True, type=Path)
    parser.add_argument("--output-zip", required=True, type=Path)
    parser.add_argument("--wav2wem", default="wav2wem")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--vgmstream-cli")
    parser.add_argument("--reference-wem", type=Path)
    parser.add_argument("--quality", type=float, default=6.0)
    args = parser.parse_args()

    source = args.source_wav.expanduser().resolve()
    output_zip = args.output_zip.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"source WAV not found: {source}")
    if output_zip.exists():
        raise SystemExit(f"refusing to overwrite existing output: {output_zip}")
    if args.reference_wem and not args.reference_wem.is_file():
        raise SystemExit(f"reference WEM not found: {args.reference_wem}")
    if not -1.0 <= args.quality <= 10.0:
        raise SystemExit("--quality must be in the FFmpeg libvorbis range -1..10")
    if shutil.which(args.ffmpeg) is None:
        raise SystemExit(f"ffmpeg not found: {args.ffmpeg}")
    if shutil.which(args.ffprobe) is None:
        raise SystemExit(f"ffprobe not found: {args.ffprobe}")
    if shutil.which(args.wav2wem) is None:
        raise SystemExit(f"wav2wem not found: {args.wav2wem}")
    if args.vgmstream_cli and shutil.which(args.vgmstream_cli) is None:
        raise SystemExit(f"vgmstream-cli not found: {args.vgmstream_cli}")

    source_metadata = probe_audio(args.ffprobe, source)
    require_target_audio(source_metadata, "source WAV")
    output_zip.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="nms-fsd-wem-") as work:
        temp_dir = Path(work)
        ogg_path = temp_dir / "fsd-source.ogg"
        wem_path = temp_dir / "fsd-source.wem"
        run(
            [
                args.ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(source),
                "-map",
                "0:a:0",
                "-map_metadata",
                "-1",
                "-vn",
                "-sn",
                "-dn",
                "-c:a",
                "libvorbis",
                "-q:a",
                str(args.quality),
                "-ar",
                str(EXPECTED_RATE),
                "-ac",
                str(EXPECTED_CHANNELS),
                str(ogg_path),
            ]
        )
        ogg_metadata = probe_audio(args.ffprobe, ogg_path)
        if ogg_metadata["codec"] != "vorbis":
            raise RuntimeError(f"FFmpeg output codec is {ogg_metadata['codec']!r}, not Vorbis")
        require_target_audio(ogg_metadata, "intermediate Ogg")

        # wav2wem's WAV path calls its embedded oggenc2.exe. Feeding the
        # Linux-generated Ogg uses its WEM repacketizer without that Windows tool.
        run([args.wav2wem, str(ogg_path), "-o", str(wem_path)])
        wem_path.write_bytes(standard_stereo_config(wem_path.read_bytes()))
        wem_info = require_target_wem(wem_path)

        decoder_verification = None
        if args.vgmstream_cli:
            decoder_verification = verify_with_vgmstream(
                args.vgmstream_cli, wem_path, args.ffprobe, temp_dir
            )
        comparison = (
            reference_comparison(args.reference_wem.resolve(), wem_info)
            if args.reference_wem
            else None
        )
        if comparison is not None and not comparison["outer_layout_matches"]:
            raise RuntimeError("output WEM outer structure differs from the supplied reference")

        wem_bytes = wem_path.read_bytes()
        wem_sha256 = hashlib.sha256(wem_bytes).hexdigest()
        manifest = {
            "purpose": "single custom-codec quick-menu diagnostic",
            "nms_runtime_playback": "not yet tested",
            "source_wav_sha256": sha256_file(source),
            "encoder": {
                "ffmpeg_codec": "libvorbis",
                "ffmpeg_quality": args.quality,
                "target_sample_rate_hz": EXPECTED_RATE,
                "target_channels": EXPECTED_CHANNELS,
                "wav2wem_repository": WAV2WEM_URL,
                "wav2wem_revision": WAV2WEM_REVISION,
                "wav2wem_input_mode": "pre-encoded Ogg Vorbis",
            },
            "wem": {
                "sha256": wem_sha256,
                "size_bytes": len(wem_bytes),
                "codec": wem_info.codec,
                "codec_tag": f"0x{wem_info.codec_tag:04X}",
                "channels": wem_info.channels,
                "sample_rate_hz": wem_info.sample_rate,
                "duration_seconds": wem_info.total_pcm_frames / wem_info.sample_rate,
                "total_pcm_frames": wem_info.total_pcm_frames,
                "fmt_chunk_size": wem_info.fmt_chunk_size,
                "fmt_extra_size": wem_info.fmt_extra_size,
                "subtype": f"0x{wem_info.subtype:08X}",
                "codebook_uid": f"0x{wem_info.codebook_uid:08X}",
                "chunks": [
                    {"tag": chunk.tag, "size": chunk.size} for chunk in wem_info.chunks
                ],
                "vgmstream_decode": decoder_verification,
                "reference_comparison": comparison,
            },
            "quickmenu_media_ids": list(QUICKMENU_IDS),
            "zip_root": MOD_ROOT,
            "persistent_bnk_files": 0,
            "archive_files": [
                f"{MEDIA_PREFIX}/{media_id}.wem" for media_id in QUICKMENU_IDS
            ]
            + [
                f"{MOD_ROOT}/README_TEST.txt",
                f"{MOD_ROOT}/PROBE_MANIFEST.json",
            ],
        }

        with zipfile.ZipFile(output_zip, "x") as archive:
            for media_id in QUICKMENU_IDS:
                zip_write(
                    archive,
                    f"{MEDIA_PREFIX}/{media_id}.wem",
                    wem_bytes,
                )
            zip_write(
                archive,
                f"{MOD_ROOT}/README_TEST.txt",
                build_readme().encode("utf-8"),
            )
            zip_write(
                archive,
                f"{MOD_ROOT}/PROBE_MANIFEST.json",
                (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )
            validate_archive_paths(archive.namelist())
            for media_id in QUICKMENU_IDS:
                entry = f"{MEDIA_PREFIX}/{media_id}.wem"
                if archive.read(entry) != wem_bytes:
                    raise RuntimeError(f"ZIP payload does not match the converted WEM: {entry}")

    print(f"created: {output_zip}")
    print(f"WEM SHA-256: {wem_sha256}")
    print(
        f"Wwise Vorbis; {wem_info.channels} ch; {wem_info.sample_rate} Hz; "
        f"{wem_info.total_pcm_frames / wem_info.sample_rate:.3f} s"
    )
    if decoder_verification:
        print("vgmstream decode: passed")
    if comparison:
        print("private native-reference outer layout: matched")
    print("persistent BNK files: 0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, WemFormatError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
