"""Create an experimental subtype-only diagnostic from the failed private ZIP."""
import argparse
import hashlib
import json
import struct
import zipfile
from pathlib import Path

try:
    from .wem_inspect import inspect_wem_bytes
except ImportError:
    from wem_inspect import inspect_wem_bytes

ROOT = 'NMS_FSD_QuickMenu_StereoConfig_Diagnostic'
IDS = ('84247370', '544349961', '750436623', '794331107')

def standard_stereo_config(data):
    """Set serialized standard FL/FR config, preserving every other byte."""
    info = inspect_wem_bytes(data)
    if (info.codec_tag, info.fmt_chunk_size, info.fmt_extra_size,
        info.channels, info.sample_rate) != (65535, 66, 48, 2, 48000):
        raise ValueError('expected modern 48 kHz stereo Wwise Vorbis')
    if info.subtype not in (0, 0x3102):
        raise ValueError('unexpected channel configuration; refusing replacement')
    pos = 12
    while data[pos:pos+4] != b'fmt ':
        size = struct.unpack_from('<I', data, pos+4)[0]
        pos += 8 + size + (size & 1)
    result = bytearray(data)
    struct.pack_into('<I', result, pos+28, 0x3102)
    return bytes(result)


def fix_stereo_config(data):
    info = inspect_wem_bytes(data)
    if (info.codec_tag, info.fmt_chunk_size, info.channels, info.sample_rate,
        info.total_pcm_frames, info.subtype) != (65535, 66, 2, 48000, 72000, 0):
        raise ValueError('expected the failed 1.5s stereo Vorbis probe with zero configuration')
    return standard_stereo_config(data)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('failed_zip', type=Path)
    parser.add_argument('output_zip', type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.failed_zip) as archive:
        inputs = [archive.read(p) for p in archive.namelist() if p.endswith('.wem')]
    if len(inputs) != 4 or any(b != inputs[0] for b in inputs):
        raise ValueError('expected four identical source WEMs')
    original = inputs[0]
    fixed = fix_stereo_config(original)
    manifest = {
        'status': 'experimental; gameplay pending',
        'change': 'fmt+0x14 channel configuration: 0 -> 0x3102',
        'original_sha256': hashlib.sha256(original).hexdigest(),
        'wem_sha256': hashlib.sha256(fixed).hexdigest(),
        'compressed_payload_and_codebook_uid_unchanged': True,
        'persistent_bnk_files': 0,
        'expected_installed_relative_path': f'GAMEDATA/MODS/{ROOT}/AUDIO/WINDOWS/MEDIA',
        'wem_info': inspect_wem_bytes(fixed).as_dict(),
    }
    with zipfile.ZipFile(args.output_zip, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for media_id in IDS:
            archive.writestr(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', fixed)
        archive.writestr(f'{ROOT}/PROBE_MANIFEST.json', json.dumps(manifest, indent=2)+'\n')
        archive.writestr(f'{ROOT}/README_TEST.txt',
            'Experimental subtype-only probe. Exit NMS; move the previous quick-menu probe\n'
            'outside GAMEDATA/MODS. Extract this ZIP into GAMEDATA/MODS, keeping this\n'
            'package folder and its direct AUDIO child. Relaunch and open the quick menu.\n'
            'Report custom cue / silence / vanilla. Exit and remove only this folder to\n'
            'restore the previous state. No BNK included. Game playback is unverified.\n')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
