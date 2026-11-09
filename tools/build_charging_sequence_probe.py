"""Private bank probe with the charging cue first in the countdown sequence.

Uses a deterministic Wwise sequence over the ten existing countdown sounds.
This should place charging on the first HUD countdown call; gameplay must
confirm timing and repeat/abort behavior. Never publish the bank or ZIP.
"""

import argparse
import json
import struct
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_charging_bank_probe import CONTAINER, NATIVE_SHA, records, split_chunks, u32
    from .build_charging_media_probe import identify_embedded_wem, patch_media_only
    from .build_warp_sequence_probe import encode, run, sha
except ImportError:
    from build_charging_bank_probe import CONTAINER, NATIVE_SHA, records, split_chunks, u32
    from build_charging_media_probe import identify_embedded_wem, patch_media_only
    from build_warp_sequence_probe import encode, run, sha


ROOT = 'NMS_FSD_ChargingSequence_Probe'


def set_first_child_sequence(bank):
    chunks = split_chunks(bank)
    payloads = dict(chunks)
    original = records(payloads[b'HIRC'])
    found = 0
    updated = []
    for kind, body in original:
        if u32(body) != CONTAINER:
            updated.append((kind, body))
            continue
        if kind != 5 or len(body) != 211 or body[83:85] != b'\x00\x12':
            raise ValueError('audited random countdown container changed')
        value = bytearray(body)
        value[83] = 1  # Sequence mode; first child is charging sound.
        value[84] &= ~2  # Keep the sequence cursor between one-second calls.
        updated.append((kind, bytes(value)))
        found += 1
    if found != 1:
        raise ValueError('expected one audited countdown container')
    payloads[b'HIRC'] = struct.pack('<I', len(updated)) + b''.join(
        struct.pack('<BI', kind, len(body)) + body for kind, body in updated)
    result = b''.join(struct.pack('<4sI', tag, len(payloads[tag])) + payloads[tag]
                      for tag, _ in chunks)
    after = dict(split_chunks(result))
    assert all(after[tag] == value for tag, value in chunks if tag != b'HIRC')
    changed = {u32(body) for (_, body), (_, new_body)
               in zip(original, records(after[b'HIRC'])) if body != new_body}
    assert changed == {CONTAINER}
    assert len(original) == len(records(after[b'HIRC']))
    return result


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
    with tempfile.TemporaryDirectory(prefix='nms-charging-sequence-') as temp:
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
        bank = set_first_child_sequence(bank)
        report.update(patched_sha256=sha(bank),
                      charging_source_sha256=sha(args.charging_mp3.read_bytes()),
                      charging_frames=info['frames'], sequence_container_id=CONTAINER,
                      modified_hirc_count=2,
                      status='first countdown call should play charging; gameplay untested')
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(f'{ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK', bank)
            archive.writestr(f'{ROOT}/MANIFEST.json', json.dumps(report, indent=2) + '\n')
            archive.writestr(f'{ROOT}/README_TEST.txt',
                             'PRIVATE charging-at-ten sequence diagnostic. Keep the '
                             'NMS_FSD_Countdown loose WEM folder installed. This changes '
                             'the countdown container from random to sequence so its first '
                             'child, the charging cue, plays on the first countdown call. '
                             'The remaining nine native ticks follow in order. Test first '
                             'warp, second warp, and abort/retry. If audio fails, remove '
                             'only this folder. No other events or completion sounds changed.\n')
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert sha(archive.read(f'{ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK')) == report['patched_sha256']
        assert len([name for name in archive.namelist()
                    if name.lower().endswith('.bnk')]) == 1
        assert not any(name.lower().endswith('.wem') for name in archive.namelist())
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
