"""Package an exact native persistent-bank copy as a private loader control.

This diagnostic does not add the charging line. Its sole purpose is to test
whether a MODS-root BNK override preserves the already working loose WEMs.
Never publish the resulting ZIP or source bank.
"""

import argparse
import json
import zipfile
from pathlib import Path

try:
    from .build_warp_sequence_probe import sha
except ImportError:
    from build_warp_sequence_probe import sha


NATIVE_SHA = 'b725ae4cd02c1556e4054e79c88810e46c35ce36c479793b51573ac7234bdef4'
ROOT = 'NMS_FSD_NativeBank_Control'
BANK_PATH = f'{ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-bank', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('refusing to overwrite an existing ZIP')
    data = args.native_bank.read_bytes()
    if sha(data) != NATIVE_SHA:
        parser.error('bank fingerprint differs from the audited game build')
    manifest = {
        'purpose': 'native bank loader control; no audio change intended',
        'bank_sha256': NATIVE_SHA,
        'modified_hirc_objects': 0,
        'replaced_media': 0,
        'loose_wems': 0,
        'gameplay_status': 'untested',
    }
    readme = (
        'PRIVATE native-bank loader control — no charging line included.\n\n'
        'Keep NMS_FSD_Countdown installed. With the game closed, extract only '
        'this NMS_FSD_NativeBank_Control folder into GAMEDATA/MODS. Ensure no '
        'other MODS folder contains NMS_AUDIO_PERSISTENT.BNK. Make one system '
        'warp and check whether the existing 4-3-2-1 custom countdown and '
        'ordinary game audio still play. If either becomes silent, remove only '
        'this control folder; the countdown package remains installed.\n\n'
        'This copied bank is valid only for the exact audited game build. '
        'Do not redistribute this ZIP.\n'
    )
    with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(BANK_PATH, data)
        archive.writestr(f'{ROOT}/MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
        archive.writestr(f'{ROOT}/README_TEST.txt', readme)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert sha(archive.read(BANK_PATH)) == NATIVE_SHA
        assert len([name for name in archive.namelist()
                    if name.lower().endswith('.bnk')]) == 1
        assert not any(name.lower().endswith('.wem') for name in archive.namelist())
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
