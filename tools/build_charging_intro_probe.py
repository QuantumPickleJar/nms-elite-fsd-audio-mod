"""Probe ten streamed MiniWarp intro variants with a charging voice line."""
import argparse
import json
import tempfile
import zipfile
from pathlib import Path

try:
    from .build_warp_sequence_probe import encode, run, sha
except ImportError:
    from build_warp_sequence_probe import encode, run, sha

ROOT = 'NMS_FSD_Charging_IntroProbe'
INTRO_IDS = (26565765, 58670338, 461106478, 610890837, 617463454,
             734832107, 866340710, 989937096, 1013624608, 1058430415)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--charging-mp3', type=Path, required=True)
    p.add_argument('--wav2wem', type=Path, required=True)
    p.add_argument('--vgmstream', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('refusing to overwrite ZIP')
    with tempfile.TemporaryDirectory(prefix='nms-charging-intro-') as tmp:
        work = Path(tmp)
        wav = work / 'charging.wav'
        run(['ffmpeg', '-v', 'error', '-i', args.charging_mp3, '-t', '3',
             '-af', 'volume=16dB', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', wav])
        wem, info = encode(wav, work, 'charging', args.wav2wem, args.vgmstream)
        if info['frames'] != 144000:
            raise ValueError('charging cue must be exactly 3 seconds')
        manifest = {
            'status': 'early event mapping unverified; gameplay diagnostic only',
            'event': 'Pl_Ship_MiniWarp_Countdown', 'event_id': 1348784714,
            'media_ids': INTRO_IDS, 'source_sha256': sha(args.charging_mp3.read_bytes()),
            'gain_db': 16, 'bnk_files': 0, **info,
        }
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as z:
            for media_id in INTRO_IDS:
                z.writestr(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', wem)
            z.writestr(f'{ROOT}/MANIFEST.json', json.dumps(manifest, indent=2)+'\n')
            z.writestr(f'{ROOT}/README_TEST.txt',
                'Experimental early-event diagnostic. Ten streamed MiniWarp intro variants '
                'contain the same three-second charging line. Whether this event fires on '
                'the current pulse-to-system route, and when, is unverified. Record the HUD '
                'number at voice onset. Remove this folder to restore the original intros. '
                'No persistent bank is included.\n')
    with zipfile.ZipFile(args.output) as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if n.endswith('.wem')]) == 10
        assert not any(n.lower().endswith('.bnk') for n in z.namelist())
        for media_id in INTRO_IDS:
            assert sha(z.read(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem')) == info['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
