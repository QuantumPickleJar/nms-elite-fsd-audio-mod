"""Build private warp cue with a complete late Engage and distinct wind-down."""
import argparse
import json
import tempfile
import wave
import zipfile
from pathlib import Path

try:
    from .build_warp_sequence_probe import BUILDUP_IDS, END_IDS, RATE, encode, run, sha
except ImportError:
    from build_warp_sequence_probe import BUILDUP_IDS, END_IDS, RATE, encode, run, sha

ROOT = 'NMS_FSD_WarpSequence_Probe_Finale'


def slice_source(source, target, start, frames):
    with wave.open(str(source), 'rb') as src:
        params = src.getparams()
        if (params.framerate, params.nchannels, params.sampwidth) != (RATE, 2, 3):
            raise ValueError('source must be 48 kHz stereo PCM24')
        src.setpos(start)
        data = src.readframes(frames)
    if len(data) != frames * 6:
        raise ValueError('source slice incomplete')
    with wave.open(str(target), 'wb') as dst:
        dst.setparams(params)
        dst.writeframes(data)
    return data


def write_pcm(path, parts):
    with wave.open(str(path), 'wb') as dst:
        dst.setnchannels(2)
        dst.setsampwidth(3)
        dst.setframerate(RATE)
        for part in parts:
            dst.writeframes(part)


def gain(source, target, db, ceiling):
    filters = f'volume={db}dB,alimiter=limit={ceiling}:level=0:latency=1'
    run(['ffmpeg', '-v', 'error', '-i', source, '-af', filters,
         '-c:a', 'pcm_s24le', target])
    with wave.open(str(target), 'rb') as w:
        return w.readframes(w.getnframes())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--wav2wem', type=Path, required=True)
    p.add_argument('--vgmstream', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('refusing to overwrite existing ZIP')
    long_source = args.source_root/'clip_034.55s_75985ea7b6a8.wav'
    jump_source = args.source_root/'clip_001.50s_e66530bbbade.wav'
    with tempfile.TemporaryDirectory(prefix='nms-finale-') as tmp:
        work = Path(tmp)
        # HUD-aligned 4,3,2,1. Stop just before the source's Engage onset.
        numbers = slice_source(long_source, work/'numbers.wav', int(13.55*RATE), int(3.87*RATE))
        build_raw = work/'build_raw.wav'
        write_pcm(build_raw, [bytes(RATE*6), numbers, bytes(int(.13*RATE)*6)])
        build_loud = work/'build_loud.wav'
        gain(build_raw, build_loud, 15, .85)
        # At the completion event: allow other effects to pass, speak Engage,
        # pause briefly, then let the wind-down be the final distinct cue.
        slice_source(long_source, work/'engaged.wav', int(17.35*RATE), int(.70*RATE))
        engaged_loud = work/'engaged_loud.wav'
        engaged_pcm = gain(work/'engaged.wav', engaged_loud, 12, .85)
        jump_loud = work/'jump_loud.wav'
        jump = gain(jump_source, jump_loud, 8, .90)
        if len(engaged_pcm) != int(.70*RATE)*6 or len(jump) != int(1.5*RATE)*6:
            raise ValueError('end cue components changed length')
        end_raw = work/'end_raw.wav'
        write_pcm(end_raw, [bytes(int(1.2*RATE)*6),
                            engaged_pcm,
                            bytes(int(.2*RATE)*6), jump])
        build_wem, build_info = encode(build_loud, work, 'build', args.wav2wem, args.vgmstream)
        end_wem, end_info = encode(end_raw, work, 'end', args.wav2wem, args.vgmstream)
        if build_info['frames'] != 240000 or end_info['frames'] != 172800:
            raise ValueError('unexpected cue length')
        manifest = {
            'status': 'completion event timing and audibility need gameplay test',
            'source_sha256': {'long': sha(long_source.read_bytes()),
                              'jump': sha(jump_source.read_bytes())},
            'build_composition': '1.00s silence + source 13.55–17.42s + 0.13s silence',
            'end_composition': '1.20s silence + source 17.35–18.05s Engage + 0.20s gap + 1.50s jump/wind-down',
            'gain_db': {'build': 15, 'engage': 12, 'wind_down': 8},
            'bnk_files': 0,
            'groups': [
                {'event': 'Pl_Ship_WarpBuildUp', 'media_ids': BUILDUP_IDS, **build_info},
                {'event': 'Pl_Ship_WarpBuildUp_End', 'media_ids': END_IDS, **end_info},
            ],
        }
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as z:
            for ids, data in ((BUILDUP_IDS, build_wem), (END_IDS, end_wem)):
                for media_id in ids:
                    z.writestr(f'{ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', data)
            z.writestr(f'{ROOT}/MANIFEST.json', json.dumps(manifest, indent=2)+'\n')
            z.writestr(f'{ROOT}/README_TEST.txt',
                'Experimental final-cue test: 4–3–2–1 during buildup; full Engage then '
                'wind-down after warp completion. Record whether the ending is audible '
                'and finishes before music. No BNK included.\n')
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
