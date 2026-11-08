"""Build a louder 10-second warp probe using recovered charging and countdown audio."""

import argparse
import json
import tempfile
import wave
import zipfile
from pathlib import Path

try:
    from .build_warp_sequence_probe import (
        BUILDUP_IDS, END_IDS, RATE, START_FRAME, BUILDUP_FRAMES, encode, run, sha,
    )
except ImportError:
    from build_warp_sequence_probe import (
        BUILDUP_IDS, END_IDS, RATE, START_FRAME, BUILDUP_FRAMES, encode, run, sha,
    )

ROOT = 'NMS_FSD_WarpTimed_Probe'
INTRO_START_FRAME = 2 * RATE
INTRO_FRAMES = 5 * RATE


def compose(source, output):
    with wave.open(str(source), 'rb') as src:
        params = src.getparams()
        if (params.framerate, params.nchannels, params.sampwidth) != (RATE, 2, 3):
            raise ValueError('expected 48 kHz stereo 24-bit source')
        src.setpos(INTRO_START_FRAME)
        charging = src.readframes(INTRO_FRAMES)
        src.setpos(START_FRAME)
        countdown = src.readframes(BUILDUP_FRAMES)
    assert len(charging) == INTRO_FRAMES * 6
    assert len(countdown) == BUILDUP_FRAMES * 6
    with wave.open(str(output), 'wb') as dst:
        dst.setparams(params)
        dst.writeframes(charging + countdown)


def boosted(source, output, gain):
    run(['ffmpeg', '-v', 'error', '-i', source, '-af', f'volume={gain}dB',
         '-c:a', 'pcm_s24le', output])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--wav2wem', type=Path, required=True)
    p.add_argument('--vgmstream', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('refusing to overwrite existing ZIP')
    long_source = args.source_root / 'clip_034.55s_75985ea7b6a8.wav'
    jump_source = args.source_root / 'clip_001.50s_e66530bbbade.wav'
    with tempfile.TemporaryDirectory(prefix='nms-warp-timed-') as tmp:
        work = Path(tmp)
        composed = work / 'composed.wav'
        buildup_wav = work / 'buildup_boosted.wav'
        jump_wav = work / 'jump_boosted.wav'
        compose(long_source, composed)
        boosted(composed, buildup_wav, 10)
        boosted(jump_source, jump_wav, 7)
        build_data, build_info = encode(buildup_wav, work, 'build', args.wav2wem, args.vgmstream)
        end_data, end_info = encode(jump_wav, work, 'end', args.wav2wem, args.vgmstream)
        assert build_info['frames'] == 10 * RATE
        assert end_info['frames'] == 72000
        manifest = {
            'status': 'timing and volume diagnostic; requires gameplay test',
            'reason': 'video countdown suggests 5-second delay from WarpBuildUp onset to source countdown',
            'source_sha256': {'long': sha(long_source.read_bytes()), 'jump': sha(jump_source.read_bytes())},
            'composition': 'source 2–7s (charging fragment/engine); source 13.05–18.05s (4,3,2,1)',
            'expected_cue_seconds_after_buildup': {'charging_fragment_approx': 0.3, '4': 5.5, '3': 6.5,
                                                  '2': 7.5, '1': 8.5},
            'gain_db': {'buildup': 10, 'jump': 7},
            'groups': [
                {'event': 'Pl_Ship_WarpBuildUp', 'media_ids': BUILDUP_IDS, **build_info},
                {'event': 'Pl_Ship_WarpBuildUp_End', 'media_ids': END_IDS, **end_info},
            ],
            'bnk_files': 0,
        }
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as z:
            for ids, data in ((BUILDUP_IDS, build_data), (END_IDS, end_data)):
                for media_id in ids:
                    z.writestr(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', data)
            z.writestr(f'{ROOT}/MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
            z.writestr(f'{ROOT}/README_TEST.txt',
                'Exit NMS; move earlier FSD and quick-menu probe folders outside MODS. '
                'Extract this folder into GAMEDATA/MODS and enable it. During the same '
                'pulse-to-system warp, record whether a charging fragment, 4-3-2-1, and jump '
                'play and how they align with the on-screen timer. Remove this entire folder '
                'to restore vanilla. No BNK included; memory-resident countdown media are unchanged.\n')
    with zipfile.ZipFile(args.output) as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if n.endswith('.wem')]) == 10
        assert not any(n.lower().endswith('.bnk') for n in z.namelist())
        for group in manifest['groups']:
            for media_id in group['media_ids']:
                assert sha(z.read(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem')) == group['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
