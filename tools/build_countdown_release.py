"""Build one platform-neutral MODS ZIP with charging and HUD countdown cues.

Private source recordings and derived WEMs stay outside the public repository.
The ZIP has game-relative paths and works on Windows and SteamOS/Proton.
"""

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_charging_intro_probe import INTRO_IDS
    from .build_finale_probe import gain, slice_source, write_pcm
    from .build_warp_sequence_probe import BUILDUP_IDS, RATE, encode, run, sha
except ImportError:
    from build_charging_intro_probe import INTRO_IDS
    from build_finale_probe import gain, slice_source, write_pcm
    from build_warp_sequence_probe import BUILDUP_IDS, RATE, encode, run, sha


ROOT = 'NMS_FSD_Countdown'
NUMBER_START = 13.55
NUMBER_END = 17.30  # before the observed Engage onset near 17.35 s
LEAD_SECONDS = 1.0
CHARGING_DELAY_MS = 2200


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--charging-mp3', type=Path, required=True)
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

        charging_wav = work / 'charging.wav'
        run(['ffmpeg', '-v', 'error', '-t', '3', '-i', args.charging_mp3,
             '-af', f'volume=16dB,adelay={CHARGING_DELAY_MS}:all=1',
             '-ar', RATE, '-ac', '2', '-c:a', 'pcm_s24le', charging_wav])
        build_wem, build_info = encode(build_loud, work, 'countdown',
                                       args.wav2wem, args.vgmstream)
        charging_wem, charging_info = encode(charging_wav, work, 'charging',
                                             args.wav2wem, args.vgmstream)
        if build_info['frames'] != 240000 or charging_info['frames'] != 249600:
            raise ValueError('incorrect decoded duration')
        groups = [
            {'event': 'Pl_Ship_WarpBuildUp', 'media_ids': BUILDUP_IDS,
             **build_info},
            {'event': 'Pl_Ship_MiniWarp_Countdown', 'media_ids': INTRO_IDS,
             **charging_info},
        ]
        manifest = {
            'status': 'countdown alignment observed in two videos; trimmed tail needs gameplay test',
            'source_sha256': {'long': sha(long_source.read_bytes()),
                              'charging_mp3': sha(args.charging_mp3.read_bytes())},
            'countdown_composition': '1.00s silence + source 13.55–17.30s + 0.25s silence',
            'charging_composition': '2.20s silence + first 3.00s of charging MP3',
            'gain_db': {'countdown': 15, 'charging': 16},
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
            'The package replaces the charging line and 4-3-2-1 buildup only. '
            'It does not replace Engage, jump, wind-down, or any BNK. '
            'A remaining Engage line may come from native game audio. '
            'To uninstall, remove only NMS_FSD_Countdown.\n'
        )
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            for ids, data in ((BUILDUP_IDS, build_wem),
                              (INTRO_IDS, charging_wem)):
                for media_id in ids:
                    archive.writestr(
                        f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', data)
            archive.writestr(f'{ROOT}/MANIFEST.json',
                             json.dumps(manifest, indent=2) + '\n')
            archive.writestr(f'{ROOT}/README.txt', readme)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert len([name for name in archive.namelist()
                    if name.endswith('.wem')]) == 15
        assert not any(name.lower().endswith('.bnk') for name in archive.namelist())
        for group in groups:
            for media_id in group['media_ids']:
                path = f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem'
                assert sha(archive.read(path)) == group['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
