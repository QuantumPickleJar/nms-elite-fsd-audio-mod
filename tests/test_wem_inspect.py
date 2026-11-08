from __future__ import annotations

import struct
import unittest

from tools.wem_inspect import WemFormatError, inspect_wem_bytes


def make_wem(*, codec_tag: int = 0xFFFF, pad_final_data: bool = False) -> bytes:
    fmt = bytearray(66)
    struct.pack_into("<HHIIHHH", fmt, 0, codec_tag, 2, 48000, 16000, 0, 0, 48)
    struct.pack_into("<I", fmt, 20, 0x20CEF588)
    struct.pack_into("<I", fmt, 24, 72000)
    struct.pack_into("<I", fmt, 60, 0x20CEF588)
    fmt[64:66] = bytes((8, 11))

    def chunk(tag: bytes, body: bytes, *, final: bool = False) -> bytes:
        value = tag + struct.pack("<I", len(body)) + body
        if len(body) & 1 and (not final or pad_final_data):
            value += b"\x00"
        return value

    body = (
        b"WAVE"
        + chunk(b"fmt ", bytes(fmt))
        + chunk(b"hash", bytes(16))
        + chunk(b"data", b"abc", final=True)
    )
    return b"RIFF" + struct.pack("<I", len(body)) + body


class WemInspectTests(unittest.TestCase):
    def test_reads_modern_wwise_vorbis_header(self) -> None:
        info = inspect_wem_bytes(make_wem())
        self.assertEqual(info.codec, "Wwise Vorbis")
        self.assertEqual(info.codec_tag, 0xFFFF)
        self.assertEqual(info.channels, 2)
        self.assertEqual(info.sample_rate, 48000)
        self.assertEqual(info.fmt_chunk_size, 66)
        self.assertEqual(info.total_pcm_frames, 72000)
        self.assertEqual([chunk.tag for chunk in info.chunks], ["fmt ", "hash", "data"])

    def test_accepts_unpadded_odd_final_data_chunk(self) -> None:
        info = inspect_wem_bytes(make_wem(pad_final_data=False))
        self.assertEqual(info.chunks[-1].size, 3)

    def test_accepts_padded_odd_final_data_chunk(self) -> None:
        info = inspect_wem_bytes(make_wem(pad_final_data=True))
        self.assertEqual(info.chunks[-1].size, 3)

    def test_names_extensible_pcm_without_claiming_it_is_vorbis(self) -> None:
        info = inspect_wem_bytes(make_wem(codec_tag=0xFFFE))
        self.assertEqual(info.codec, "WAVEFORMATEXTENSIBLE")

    def test_rejects_truncated_chunk(self) -> None:
        with self.assertRaises(WemFormatError):
            inspect_wem_bytes(make_wem()[:-2])

    def test_rejects_incorrect_riff_size(self) -> None:
        data = bytearray(make_wem())
        struct.pack_into("<I", data, 4, len(data))
        with self.assertRaises(WemFormatError):
            inspect_wem_bytes(bytes(data))


if __name__ == "__main__":
    unittest.main()
