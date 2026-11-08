#!/usr/bin/env python3
"""Read-only RIFF/Wwise WEM structure inspector."""

from __future__ import annotations

import argparse
import json
import struct
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class WemFormatError(ValueError):
    """Raised when a file is not a complete RIFF/WAVE WEM."""


@dataclass(frozen=True)
class Chunk:
    tag: str
    size: int


@dataclass(frozen=True)
class WemInfo:
    file_size: int
    riff_size: int
    codec_tag: int
    codec: str
    channels: int
    sample_rate: int
    average_bytes_per_second: int
    block_align: int
    bits_per_sample: int
    fmt_chunk_size: int
    fmt_extra_size: int
    total_pcm_frames: int | None
    subtype: int | None
    codebook_uid: int | None
    chunks: tuple[Chunk, ...]

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["chunks"] = [asdict(chunk) for chunk in self.chunks]
        result["codec_tag_hex"] = f"0x{self.codec_tag:04X}"
        if self.subtype is not None:
            result["subtype_hex"] = f"0x{self.subtype:08X}"
        if self.codebook_uid is not None:
            result["codebook_uid_hex"] = f"0x{self.codebook_uid:08X}"
        return result


def inspect_wem_bytes(data: bytes) -> WemInfo:
    if len(data) < 12:
        raise WemFormatError("file is shorter than a RIFF/WAVE header")
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise WemFormatError("expected RIFF/WAVE signature")

    riff_size = struct.unpack_from("<I", data, 4)[0]
    if riff_size + 8 != len(data):
        raise WemFormatError(
            f"RIFF size declares {riff_size + 8} bytes; file has {len(data)}"
        )

    chunks: list[Chunk] = []
    bodies: dict[str, bytes] = {}
    position = 12
    while position < len(data):
        if position + 8 > len(data):
            raise WemFormatError("truncated chunk header")
        raw_tag = data[position : position + 4]
        try:
            tag = raw_tag.decode("ascii")
        except UnicodeDecodeError as exc:
            raise WemFormatError("chunk tag is not ASCII") from exc
        size = struct.unpack_from("<I", data, position + 4)[0]
        body_start = position + 8
        body_end = body_start + size
        if body_end > len(data):
            raise WemFormatError(f"chunk {tag!r} extends past end of file")
        chunks.append(Chunk(tag, size))
        bodies[tag] = data[body_start:body_end]

        # Some valid WEM producers omit the final RIFF pad byte for an odd
        # sized data chunk. Accept that only when the declared body ends at EOF.
        if body_end == len(data):
            position = body_end
            break
        next_position = body_end + (size & 1)
        if next_position > len(data):
            raise WemFormatError(f"missing pad byte after chunk {tag!r}")
        position = next_position

    if position != len(data):
        raise WemFormatError("unparsed trailing bytes")
    if len([chunk for chunk in chunks if chunk.tag == "fmt "]) != 1:
        raise WemFormatError("expected exactly one fmt chunk")
    if len([chunk for chunk in chunks if chunk.tag == "data"]) != 1:
        raise WemFormatError("expected exactly one data chunk")

    fmt = bodies["fmt "]
    if len(fmt) < 18:
        raise WemFormatError("fmt chunk is shorter than WAVEFORMAT")
    codec_tag, channels = struct.unpack_from("<HH", fmt, 0)
    sample_rate, average_bytes = struct.unpack_from("<II", fmt, 4)
    block_align, bits_per_sample, extra_size = struct.unpack_from("<HHH", fmt, 12)
    if channels == 0 or sample_rate == 0:
        raise WemFormatError("fmt chunk has zero channels or sample rate")
    if extra_size > len(fmt) - 18:
        raise WemFormatError("fmt extra-size field exceeds the fmt chunk")

    frames: int | None = None
    subtype: int | None = None
    codebook_uid: int | None = None
    if codec_tag == 0xFFFF and len(fmt) >= 66 and extra_size >= 48:
        subtype = struct.unpack_from("<I", fmt, 20)[0]
        frames = struct.unpack_from("<I", fmt, 24)[0]
        codebook_uid = struct.unpack_from("<I", fmt, 60)[0]

    codec_names = {
        0x0001: "PCM",
        0x0002: "Microsoft ADPCM",
        0x0011: "IMA ADPCM",
        0xAAC0: "Wwise AAC",
        0xFFFE: "WAVEFORMATEXTENSIBLE",
        0xFFFF: "Wwise Vorbis",
    }
    return WemInfo(
        file_size=len(data),
        riff_size=riff_size,
        codec_tag=codec_tag,
        codec=codec_names.get(codec_tag, "unknown"),
        channels=channels,
        sample_rate=sample_rate,
        average_bytes_per_second=average_bytes,
        block_align=block_align,
        bits_per_sample=bits_per_sample,
        fmt_chunk_size=len(fmt),
        fmt_extra_size=extra_size,
        total_pcm_frames=frames,
        subtype=subtype,
        codebook_uid=codebook_uid,
        chunks=tuple(chunks),
    )


def inspect_wem(path: Path) -> WemInfo:
    return inspect_wem_bytes(path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wem", type=Path, help="WEM file to inspect")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()
    info = inspect_wem(args.wem)
    if args.json:
        print(json.dumps(info.as_dict(), indent=2))
    else:
        print(f"file: {args.wem}")
        print(f"codec: {info.codec} ({info.codec_tag:#06x})")
        print(f"channels/rate: {info.channels} / {info.sample_rate} Hz")
        print(f"fmt chunk: {info.fmt_chunk_size} bytes (extra {info.fmt_extra_size})")
        print(f"chunks: {', '.join(f'{chunk.tag}:{chunk.size}' for chunk in info.chunks)}")
        if info.total_pcm_frames is not None:
            print(f"total PCM frames: {info.total_pcm_frames}")
        if info.subtype is not None:
            print(f"subtype: {info.subtype:#010x}")
        if info.codebook_uid is not None:
            print(f"codebook UID: {info.codebook_uid:#010x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
