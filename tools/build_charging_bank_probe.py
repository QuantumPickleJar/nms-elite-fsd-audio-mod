"""Private exact-build BNK diagnostic: charging on first countdown tick.

Requires the user's authorization for a persistent-bank override. Never publish
the output ZIP, bank, or audio. Sequence/reset behavior requires a game test.
"""
import argparse
import json
import struct
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_warp_sequence_probe import encode, run, sha
except ImportError:
    from build_warp_sequence_probe import encode, run, sha

NATIVE_SHA = 'b725ae4cd02c1556e4054e79c88810e46c35ce36c479793b51573ac7234bdef4'
CONTAINER = 113103304
FIRST_SOUND = 249399417
FIRST_MEDIA = 753617385
RESET_ACTION = 4000000123
END_EVENTS = (998544585, 3113682208)
ROOT = 'NMS_FSD_WarpCharging_BankProbe'


def u32(data, offset=0):
    return struct.unpack_from('<I', data, offset)[0]


def split_chunks(data):
    result = []
    p = 0
    while p < len(data):
        if p + 8 > len(data):
            raise ValueError('truncated bank chunk')
        tag, size = struct.unpack_from('<4sI', data, p)
        end = p + 8 + size
        if end > len(data):
            raise ValueError('invalid bank chunk length')
        result.append((tag, data[p+8:end]))
        p = end
    return result


def records(hirc):
    p = 4
    result = []
    for _ in range(u32(hirc)):
        kind, size = struct.unpack_from('<BI', hirc, p)
        body = hirc[p+5:p+5+size]
        if len(body) != size or size < 4:
            raise ValueError('invalid HIRC record')
        result.append((kind, body))
        p += size + 5
    if p != len(hirc):
        raise ValueError('trailing HIRC data')
    return result


def patch_bank(native, wem):
    if sha(native) != NATIVE_SHA:
        raise ValueError('unsupported native bank: exact fingerprint required')
    chunks = split_chunks(native)
    c = dict(chunks)
    original = records(c[b'HIRC'])
    by_id = {u32(b): (k, b) for k, b in original}
    if RESET_ACTION in by_id:
        raise ValueError('reset action ID collision')
    # Same embedded media identity/cache, new data and explicit memory size.
    sound = bytearray(by_id[FIRST_SOUND][1])
    assert len(sound) == 53 and u32(sound, 4) == 0x40001
    assert sound[8] == 0 and u32(sound, 9) == FIRST_MEDIA
    struct.pack_into('<I', sound, 17, len(wem))
    container = bytearray(by_id[CONTAINER][1])
    assert len(container) == 211 and container[83:85] == b'\x00\x12'
    assert u32(container, 131) == FIRST_SOUND
    container[83] = 1  # Sequence, step mode retained.
    container[84] &= ~2  # Keep sequence cursor between tick events.
    changed = {FIRST_SOUND: bytes(sound), CONTAINER: bytes(container)}
    for event in END_EVENTS:
        kind, body = by_id[event]
        assert kind == 4 and body[4] < 127 and len(body) == 5 + 4 * body[4]
        changed[event] = body[:4] + bytes([body[4]+1]) + body[5:] + struct.pack('<I', RESET_ACTION)
    # v154: ResetPlaylist_E_O; target; bus flag; zero property bundles;
    # linear curve; empty exception list. Independently parse with wwiser.
    action = struct.pack('<IHI', RESET_ACTION, 0x2203, CONTAINER) + bytes([0, 0, 0, 4, 0])
    updated = [(k, changed.get(u32(b), b)) for k, b in original] + [(3, action)]
    c[b'HIRC'] = struct.pack('<I', len(updated)) + b''.join(
        struct.pack('<BI', k, len(b)) + b for k, b in updated)
    data = c[b'DATA']
    offset = (len(data) + 15) & ~15
    c[b'DATA'] = data + bytes(offset-len(data)) + wem
    didx = bytearray(c[b'DIDX'])
    found = 0
    for p in range(0, len(didx), 12):
        if u32(didx, p) == FIRST_MEDIA:
            struct.pack_into('<II', didx, p+4, offset, len(wem))
            found += 1
    assert found == 1
    c[b'DIDX'] = bytes(didx)
    output = b''.join(struct.pack('<4sI', tag, len(c[tag])) + c[tag] for tag, _ in chunks)
    # Verify scope: four existing objects, one action, one media-index entry.
    check = dict(split_chunks(output))
    after = {u32(b): (k, b) for k, b in records(check[b'HIRC'])}
    assert set(after) == set(by_id) | {RESET_ACTION}
    assert {id for id in by_id if by_id[id] != after[id]} == set(changed)
    assert check[b'DATA'][:len(data)] == data
    assert check[b'DATA'][offset:offset+len(wem)] == wem
    for tag, value in chunks:
        if tag not in (b'HIRC', b'DIDX', b'DATA'):
            assert check[tag] == value
    return output, {'native_sha256': sha(native), 'patched_sha256': sha(output),
                    'modified_hirc_ids': sorted(changed), 'added_action_id': RESET_ACTION,
                    'replaced_media_id': FIRST_MEDIA, 'media_sha256': sha(wem),
                    'original_hirc_count': len(original), 'patched_hirc_count': len(updated)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native-bank', type=Path, required=True)
    p.add_argument('--charging-mp3', type=Path, required=True)
    p.add_argument('--sequence-zip', type=Path, required=True)
    p.add_argument('--wav2wem', type=Path, required=True)
    p.add_argument('--vgmstream', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('refusing to overwrite ZIP')
    with tempfile.TemporaryDirectory(prefix='nms-charging-bank-') as tmp:
        work = Path(tmp)
        wav = work/'charging.wav'
        run(['ffmpeg', '-v', 'error', '-i', args.charging_mp3, '-t', '3',
             '-af', 'volume=16dB', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', wav])
        wem, info = encode(wav, work, 'charging', args.wav2wem, args.vgmstream)
        assert info['frames'] == 144000
        bank, report = patch_bank(args.native_bank.read_bytes(), wem)
        report.update(charging=info, charging_source_sha256=sha(args.charging_mp3.read_bytes()),
                      status='offline validated; sequence, repeat and abort behavior untested in game')
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as z:
            with zipfile.ZipFile(args.sequence_zip) as sequence:
                names = [n for n in sequence.namelist() if n.endswith('.wem')]
                assert len(names) == 10
                for name in names:
                    target = ROOT + '/' + name.split('/', 1)[1]
                    z.writestr(target, sequence.read(name))
            z.writestr(ROOT+'/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK', bank)
            z.writestr(ROOT+'/MANIFEST_BANK.json', json.dumps(report, indent=2)+'\n')
            z.writestr(ROOT+'/README_TEST.txt',
                'PRIVATE experimental bank diagnostic. Contains a persistent bank override. '
                'Use alone; conflicts with any other mod replacing NMS_AUDIO_PERSISTENT.BNK. '
                'Charging should play on the first countdown tick (HUD 10), then native ticks. '
                'Verify a complete warp, a second warp, and abort/retry. Report repeats, missing '
                'charging, timing and audio side effects. Remove the entire mod folder to roll back.\n')
    with zipfile.ZipFile(args.output) as z:
        assert z.testzip() is None
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
