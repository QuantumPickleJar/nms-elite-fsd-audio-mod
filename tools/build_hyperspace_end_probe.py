"""Build a private warp probe with wind-down on the hyperspace completion event."""

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


ROOT = 'NMS_FSD_WarpSequence_HyperspaceEnd'
HYPERSPACE_END_IDS = (106241036, 225120771, 246304501, 297993109,
                      324387532, 396125112, 525528231, 545054570,
                      552053220, 630489935, 691709851, 694032990)


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
    jump_source = args.source_root / 'clip_001.50s_e66530bbbade.wav'
    with tempfile.TemporaryDirectory(prefix='nms-hyperspace-end-') as temp:
        work = Path(temp)
        numbers = slice_source(long_source, work / 'numbers.wav',
                               int(13.55 * RATE), int(3.87 * RATE))
        buildup = work / 'buildup.wav'
        write_pcm(buildup, [bytes(RATE * 6), numbers,
                            bytes(int(.13 * RATE) * 6)])
        build_loud = work / 'buildup_loud.wav'
        gain(buildup, build_loud, 15, .85)

        jump_loud = work / 'wind_down_loud.wav'
        wind_down = gain(jump_source, jump_loud, 11, .90)
        if len(wind_down) != int(1.5 * RATE) * 6:
            raise ValueError('wind-down source changed length')
        end_wav = work / 'hyperspace_end.wav'
        write_pcm(end_wav, [bytes(int(.5 * RATE) * 6), wind_down])

        build_wem, build_info = encode(build_loud, work, 'build',
                                       args.wav2wem, args.vgmstream)
        end_wem, end_info = encode(end_wav, work, 'end',
                                   args.wav2wem, args.vgmstream)
        if build_info['frames'] != 240000 or end_info['frames'] != 96000:
            raise ValueError('unexpected decoded frame count')
        manifest = {
            'status': 'hyperspace completion placement needs gameplay test',
            'source_sha256': {'long': sha(long_source.read_bytes()),
                              'jump': sha(jump_source.read_bytes())},
            'build_composition': '1.00s silence + source 13.55–17.42s + 0.13s silence',
            'end_composition': '0.50s silence + original 1.50s jump/wind-down; no Engage',
            'gain_db': {'build': 15, 'wind_down': 11},
            'bnk_files': 0,
            'groups': [
                {'event': 'Pl_Ship_WarpBuildUp', 'media_ids': BUILDUP_IDS,
                 **build_info},
                {'event': 'Pl_Ship_Hyperspace_End', 'media_ids': HYPERSPACE_END_IDS,
                 **end_info},
            ],
        }
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            for ids, data in ((BUILDUP_IDS, build_wem),
                              (HYPERSPACE_END_IDS, end_wem)):
                for media_id in ids:
                    archive.writestr(
                        f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', data)
            archive.writestr(f'{ROOT}/MANIFEST.json',
                             json.dumps(manifest, indent=2) + '\n')
            archive.writestr(f'{ROOT}/README_TEST.txt',
                             'Gameplay diagnostic: retain the delayed charging intro mod. '
                             'During warp, check 4–3–2–1 against the HUD; after the long '
                             'tunnel, listen for a distinct wind-down before music. '
                             'The Engage voice is intentionally absent. No BNK included.\n')
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert len([n for n in archive.namelist() if n.endswith('.wem')]) == 17
        assert not any(n.lower().endswith('.bnk') for n in archive.namelist())
        for group in manifest['groups']:
            for media_id in group['media_ids']:
                path = f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem'
                assert sha(archive.read(path)) == group['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
