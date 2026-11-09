"""Private one-media bank diagnostic; leave countdown container unchanged.

One of the ten native random countdown ticks is replaced by the charging cue.
It may play at any countdown number. This tests embedded-media replacement,
not final charging-at-ten timing. Never publish the output bank or ZIP.
"""

import argparse
import hashlib
import json
import struct
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_charging_bank_probe import (FIRST_MEDIA, FIRST_SOUND, NATIVE_SHA,
                                            records, split_chunks, u32)
    from .build_warp_sequence_probe import encode, run, sha
    from .wem_inspect import inspect_wem_bytes
except ImportError:
    from build_charging_bank_probe import (FIRST_MEDIA, FIRST_SOUND, NATIVE_SHA,
                                           records, split_chunks, u32)
    from build_warp_sequence_probe import encode, run, sha
    from wem_inspect import inspect_wem_bytes


ROOT = 'NMS_FSD_ChargingMedia_Probe'


def identify_embedded_wem(wem):
    """Give the generated WEM a nonzero content identity and return cacheID.

    All ten audited native tick WEMs have cacheID equal to the little-endian
    first four bytes of their 16-byte `hash` chunk. The native hash algorithm
    is unknown; MD5 of the generated WEM with its zero hash is a deterministic
    candidate identity. Gameplay must establish runtime acceptance.
    """
    info = inspect_wem_bytes(wem)
    if (info.codec, info.channels, info.sample_rate, info.subtype) != (
            'Wwise Vorbis', 2, 48000, 0x3102):
        raise ValueError('expected 48 kHz stereo Wwise Vorbis')
    positions = []
    cursor = 12
    while cursor < len(wem):
        size = u32(wem, cursor + 4)
        if wem[cursor:cursor + 4] == b'hash':
            positions.append(cursor)
        cursor += 8 + size + (size & 1)
    if len(positions) != 1:
        raise ValueError('expected exactly one hash chunk')
    pos = positions[0]
    if u32(wem, pos + 4) != 16 or wem[pos + 8:pos + 24] != bytes(16):
        raise ValueError('expected generated zeroed 16-byte hash chunk')
    digest = hashlib.md5(wem).digest()
    if digest[:4] == bytes(4):
        raise ValueError('zero cache identity')
    result = wem[:pos + 8] + digest + wem[pos + 24:]
    assert inspect_wem_bytes(result) == info
    return result, int.from_bytes(digest[:4], 'little')


def patch_media_only(native, wem, cache_id):
    if sha(native) != NATIVE_SHA:
        raise ValueError('unsupported native bank fingerprint')
    chunks = split_chunks(native)
    payloads = dict(chunks)
    original = records(payloads[b'HIRC'])
    by_id = {u32(body): (kind, body) for kind, body in original}
    kind, sound_body = by_id[FIRST_SOUND]
    if kind != 2 or len(sound_body) != 53 or u32(sound_body, 9) != FIRST_MEDIA:
        raise ValueError('audited sound object changed')
    if u32(sound_body, 4) != 0x40001 or sound_body[8] != 0:
        raise ValueError('audited source format changed')
    old_data = payloads[b'DATA']
    didx = bytearray(payloads[b'DIDX'])
    matches = [offset for offset in range(0, len(didx), 12)
               if u32(didx, offset) == FIRST_MEDIA]
    if len(matches) != 1:
        raise ValueError('expected one target DIDX entry')
    didx_pos = matches[0]
    old_size = u32(didx, didx_pos + 8)
    if u32(sound_body, 17) != old_size:
        raise ValueError('source size and DIDX disagree')
    aligned_offset = (len(old_data) + 15) & ~15
    payloads[b'DATA'] = old_data + bytes(aligned_offset - len(old_data)) + wem
    struct.pack_into('<II', didx, didx_pos + 4, aligned_offset, len(wem))
    payloads[b'DIDX'] = bytes(didx)
    new_sound = bytearray(sound_body)
    struct.pack_into('<II', new_sound, 13, cache_id, len(wem))
    # Preserve record order while replacing precisely one sound object.
    payloads[b'HIRC'] = struct.pack('<I', len(original)) + b''.join(
        struct.pack('<BI', record_kind, len(body)) +
        (bytes(new_sound) if u32(body) == FIRST_SOUND else body)
        for record_kind, body in original)
    result = b''.join(struct.pack('<4sI', tag, len(payloads[tag])) + payloads[tag]
                      for tag, _ in chunks)
    after = dict(split_chunks(result))
    assert after[b'DATA'][:len(old_data)] == old_data
    assert after[b'DATA'][aligned_offset:aligned_offset + len(wem)] == wem
    assert all(after[tag] == value for tag, value in chunks
               if tag not in (b'DIDX', b'DATA', b'HIRC'))
    changed = {u32(body) for (kind, body), (_, next_body)
               in zip(original, records(after[b'HIRC'])) if body != next_body}
    assert changed == {FIRST_SOUND}
    assert len(original) == len(records(after[b'HIRC']))
    return result, {'native_sha256': sha(native), 'patched_sha256': sha(result),
                    'replaced_media_id': FIRST_MEDIA, 'modified_sound_id': FIRST_SOUND,
                    'new_cache_id': cache_id, 'media_sha256': sha(wem),
                    'modified_hirc_count': 1, 'new_hirc_count': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-bank', type=Path, required=True)
    parser.add_argument('--charging-mp3', type=Path, required=True)
    parser.add_argument('--wav2wem', type=Path, required=True)
    parser.add_argument('--vgmstream', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('refusing to overwrite ZIP')
    with tempfile.TemporaryDirectory(prefix='nms-charging-media-') as temp:
        work = Path(temp)
        wav = work / 'charging.wav'
        run(['ffmpeg', '-v', 'error', '-i', args.charging_mp3, '-t', '3',
             '-af', 'volume=16dB', '-ar', '48000', '-ac', '2',
             '-c:a', 'pcm_s24le', wav])
        wem, info = encode(wav, work, 'charging', args.wav2wem, args.vgmstream)
        if info['frames'] != 144000:
            raise ValueError('charging source changed duration')
        wem, cache_id = identify_embedded_wem(wem)
        bank, report = patch_media_only(args.native_bank.read_bytes(), wem, cache_id)
        report['charging_source_sha256'] = sha(args.charging_mp3.read_bytes())
        report['charging_frames'] = info['frames']
        report['status'] = 'media-only diagnostic; random tick position and gameplay compatibility untested'
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(f'{ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK', bank)
            archive.writestr(f'{ROOT}/MANIFEST.json', json.dumps(report, indent=2) + '\n')
            archive.writestr(f'{ROOT}/README_TEST.txt',
                             'PRIVATE one-media countdown diagnostic. Keep the five-WEM '
                             'NMS_FSD_Countdown folder. This replaces one of ten random '
                             'native HUD countdown ticks with the charging phrase; it '
                             'may play at any number, possibly cut by the next tick. '
                             'If custom countdown or ordinary game audio becomes silent, '
                             'remove only this probe folder. No completion audio changed.\n')
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert sha(archive.read(f'{ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK')) == report['patched_sha256']
        assert len([name for name in archive.namelist()
                    if name.lower().endswith('.bnk')]) == 1
        assert not any(name.lower().endswith('.wem') for name in archive.namelist())
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
