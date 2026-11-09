"""Build one platform-neutral MODS ZIP with the HUD countdown cue.

Private source recordings and derived WEMs stay outside the public repository.
The ZIP has game-relative paths and works on Windows and SteamOS/Proton.
"""

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_finale_probe import gain, slice_source, write_pcm
    from .build_warp_sequence_probe import BUILDUP_IDS, RATE, encode, sha
except ImportError:
    from build_finale_probe import gain, slice_source, write_pcm
    from build_warp_sequence_probe import BUILDUP_IDS, RATE, encode, sha


ROOT = 'NMS_FSD_Countdown'
NUMBER_START = 13.55
NUMBER_END = 17.30  # before the observed Engage onset near 17.35 s
LEAD_SECONDS = 1.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--wav2wem', type=Path, required=True)
    parser.add_argument('--vgmstream', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('refusing to overwrite existing ZIP')
    long_source = args.source_root / 'clip_034.55s_75985ea7b6a8.wav'
    if not (NUMBER_END < 17.35 and NUMBER_START < NUMBER_END):
        raise ValueError('countdown source overlaps Engage')
    with tempfile.TemporaryDirectory(prefix='nms-countdown-release-') as temp:
        work = Path(temp)
        number_frames = round((NUMBER_END - NUMBER_START) * RATE)
        numbers = slice_source(long_source, work / 'numbers.wav',
                               round(NUMBER_START * RATE), number_frames)
        tail_frames = 5 * RATE - round(LEAD_SECONDS * RATE) - number_frames
        if tail_frames < 0:
            raise ValueError('countdown longer than five seconds')
        build_raw = work / 'countdown_raw.wav'
        write_pcm(build_raw, [bytes(round(LEAD_SECONDS * RATE) * 6),
                              numbers, bytes(tail_frames * 6)])
        build_loud = work / 'countdown_loud.wav'
        gain(build_raw, build_loud, 15, .85)

        build_wem, build_info = encode(build_loud, work, 'countdown',
                                       args.wav2wem, args.vgmstream)
        if build_info['frames'] != 240000:
            raise ValueError('incorrect decoded duration')
        groups = [
            {'event': 'Pl_Ship_WarpBuildUp', 'media_ids': BUILDUP_IDS,
             **build_info},
        ]
        manifest = {
            'status': 'HUD countdown heard in game; pulse charging removed pending correct event',
            'source_sha256': {'long': sha(long_source.read_bytes())},
            'countdown_composition': '1.00s silence + source 13.55–17.30s + 0.25s silence',
            'gain_db': {'countdown': 15},
            'bnk_files': 0,
            'groups': groups,
        }
        readme = (
            'No Man\'s Sky FSD countdown — Windows and SteamOS/Proton\n\n'
            'Close the game. Extract the NMS_FSD_Countdown folder into '
            'No Man\'s Sky/GAMEDATA/MODS/. The result must be '
            'GAMEDATA/MODS/NMS_FSD_Countdown/AUDIO/WINDOWS/MEDIA/. '
            'Remove earlier NMS_FSD_* countdown/charging probe folders first '
            'to avoid duplicate media IDs. Keep unrelated mods installed.\n\n'
            'The package replaces only the 4-3-2-1 buildup. The charging line '
            'was removed because its loose-media event also fires during normal '
            'pulse drive. It does not replace Engage, jump, wind-down, or any BNK. '
            'To uninstall, remove only NMS_FSD_Countdown.\n'
        )
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            for media_id in BUILDUP_IDS:
                archive.writestr(
                    f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', build_wem)
            archive.writestr(f'{ROOT}/MANIFEST.json',
                             json.dumps(manifest, indent=2) + '\n')
            archive.writestr(f'{ROOT}/README.txt', readme)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert len([name for name in archive.namelist()
                    if name.endswith('.wem')]) == 5
        assert not any(name.lower().endswith('.bnk') for name in archive.namelist())
        for group in groups:
            for media_id in group['media_ids']:
                path = f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem'
                assert sha(archive.read(path)) == group['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
