"""Build an event-mapping probe for current Forsaken streamed warp media.

This does not edit the source WAVs or any installed game/mod files. The game
event timing is provisional; the recovered source offsets are sample-exact.
"""

import argparse
import hashlib
import json
import subprocess
import tempfile
import wave
import zipfile
from pathlib import Path

try:
    from .stereo_subtype_probe import standard_stereo_config
    from .wem_inspect import inspect_wem_bytes
    from .compare_vorbis_packets import packets
except ImportError:
    from stereo_subtype_probe import standard_stereo_config
    from wem_inspect import inspect_wem_bytes
    from compare_vorbis_packets import packets


ROOT = 'NMS_FSD_WarpSequence_Probe'
BUILDUP_IDS = (293625877, 317366338, 332067571, 722656460, 978671379)
END_IDS = (612082143, 729241301, 815189202, 894251691, 913967941)
RATE = 48000
START_FRAME = 13 * RATE + 2400  # 13.050s: 0.500s before recovered "4"
BUILDUP_FRAMES = 5 * RATE       # ends at recovered jump onset, 18.050s


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(command):
    subprocess.run([str(x) for x in command], check=True, capture_output=True)


def excerpt(source, output, advance_frames=0):
    with wave.open(str(source), 'rb') as source_wav:
        params = source_wav.getparams()
        if (params.framerate, params.nchannels, params.sampwidth) != (RATE, 2, 3):
            raise ValueError('expected 48 kHz, stereo, 24-bit PCM source')
        if source_wav.getnframes() < START_FRAME + BUILDUP_FRAMES:
            raise ValueError('source too short for recovered cue interval')
        source_wav.setpos(START_FRAME)
        audio = source_wav.readframes(BUILDUP_FRAMES)
        audio = audio[advance_frames * 6:] + bytes(advance_frames * 6)
    with wave.open(str(output), 'wb') as dest:
        dest.setparams(params)
        dest.writeframes(audio)


def encode(source, work, suffix, wav2wem, vgmstream):
    with wave.open(str(source), 'rb') as input_wav:
        frames = input_wav.getnframes()
        if (input_wav.getframerate(), input_wav.getnchannels()) != (RATE, 2):
            raise ValueError('expected 48 kHz stereo source')
    ogg = work / f'{suffix}.ogg'
    wem = work / f'{suffix}.wem'
    decoded = work / f'{suffix}_decoded.wav'
    run(['ffmpeg', '-v', 'error', '-i', source, '-map_metadata', '-1',
         '-c:a', 'libvorbis', '-q:a', '6', '-ar', RATE, '-ac', '2', ogg])
    run([wav2wem, ogg, '-o', wem])
    data = standard_stereo_config(wem.read_bytes())
    wem.write_bytes(data)
    info = inspect_wem_bytes(data)
    if info.total_pcm_frames != frames or info.subtype != 0x3102:
        raise ValueError('invalid Wwise stereo configuration or frame count')
    framing = packets(wem)
    run([vgmstream, '-o', decoded, wem])
    with wave.open(str(decoded), 'rb') as decoded_wav:
        if (decoded_wav.getnframes(), decoded_wav.getframerate(),
                decoded_wav.getnchannels()) != (frames, RATE, 2):
            raise ValueError('decoded frame count, rate or channels mismatch')
    return data, {'frames': frames, 'duration_seconds': frames / RATE,
                  'sha256': sha(data), 'audio_packets': framing['audio_packets']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--wav2wem', type=Path, required=True)
    parser.add_argument('--vgmstream', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--buildup-gain-db', type=float, default=0,
                        help='Optional 0–20 dB gain; above 10 dB uses a peak limiter')
    parser.add_argument('--jump-gain-db', type=float, default=0)
    parser.add_argument('--advance-ms', type=int, default=0,
                        help='Advance content and pad its end, preserving five-second duration')
    args = parser.parse_args()
    if not 0 <= args.buildup_gain_db <= 20 or not 0 <= args.jump_gain_db <= 5:
        parser.error('buildup gain must be 0–20 dB and jump gain 0–5 dB')
    if not 0 <= args.advance_ms <= 500:
        parser.error('advance must be 0–500 ms')
    root = ROOT + ('_Louder' if args.buildup_gain_db else '')
    if args.advance_ms or args.jump_gain_db:
        root = ROOT + '_Adjusted'
    if args.output.exists():
        parser.error('refusing to overwrite existing ZIP')
    long_source = args.source_root / 'clip_034.55s_75985ea7b6a8.wav'
    jump_source = args.source_root / 'clip_001.50s_e66530bbbade.wav'
    with tempfile.TemporaryDirectory(prefix='nms-warp-sequence-') as temp:
        work = Path(temp)
        buildup_wav = work / 'buildup_excerpt.wav'
        advance_frames = args.advance_ms * RATE // 1000
        excerpt(long_source, buildup_wav, advance_frames)
        if args.buildup_gain_db:
            boosted = work / 'buildup_louder.wav'
            filters = f'volume={args.buildup_gain_db}dB'
            if args.buildup_gain_db > 10:
                filters += ',alimiter=limit=0.85:level=0:latency=1'
            run(['ffmpeg', '-v', 'error', '-i', buildup_wav, '-af',
                 filters, '-c:a', 'pcm_s24le', boosted])
            buildup_wav = boosted
        buildup, buildup_info = encode(buildup_wav, work, 'buildup', args.wav2wem, args.vgmstream)
        jump_input = jump_source
        if args.jump_gain_db:
            jump_input = work / 'jump_louder.wav'
            run(['ffmpeg', '-v', 'error', '-i', jump_source, '-af',
                 f'volume={args.jump_gain_db}dB', '-c:a', 'pcm_s24le', jump_input])
        jump, jump_info = encode(jump_input, work, 'jump', args.wav2wem, args.vgmstream)
        manifest = {
            'status': 'experimental; event dispatch and timing need gameplay test',
            'buildup_gain_db': args.buildup_gain_db,
            'jump_gain_db': args.jump_gain_db,
            'advance_ms': args.advance_ms,
            'buildup_limiter': args.buildup_gain_db > 10,
            'source_interval_seconds': [13.05 + args.advance_ms / 1000, 18.05],
            'tail_silence_frames': advance_frames,
            'source_offsets_seconds': {'4': 13.55, '3': 14.55, '2': 15.55,
                                       '1': 16.55, 'jump': 18.05},
            'codec': 'Wwise Vorbis; 48 kHz stereo; channel config 0x3102',
            'bnk_files': 0,
            'groups': [
                {'event': 'Pl_Ship_WarpBuildUp', 'event_id': 679898858,
                 'media_ids': BUILDUP_IDS, 'source_sha256': sha(long_source.read_bytes()),
                 'source_excerpt_sha256': sha(buildup_wav.read_bytes()), **buildup_info},
                {'event': 'Pl_Ship_WarpBuildUp_End', 'event_id': 3113682208,
                 'media_ids': END_IDS, 'source_sha256': sha(jump_source.read_bytes()), **jump_info},
            ],
        }
        with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
            for ids, data in ((BUILDUP_IDS, buildup), (END_IDS, jump)):
                for media_id in ids:
                    archive.writestr(f'{root}/AUDIO/WINDOWS/MEDIA/{media_id}.wem', data)
            archive.writestr(f'{root}/MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
            archive.writestr(f'{root}/README_TEST.txt',
                'Experimental Forsaken warp sequence diagnostic. Exit NMS; move earlier FSD '
                'and quick-menu probe folders outside MODS. Extract this mod root into '
                'GAMEDATA/MODS and enable it. Repeat the same pulse-to-system warp. '
                'Report whether 4,3,2,1 and jump play, their timing, and any missing/overlapping '
                'audio. Remove this whole folder to restore vanilla. No BNK is included. '
                'Memory-resident Warp_Countdown media remain unchanged.\n')
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert len([n for n in archive.namelist() if n.endswith('.wem')]) == 10
        assert not any(n.lower().endswith('.bnk') for n in archive.namelist())
        for group in manifest['groups']:
            for media_id in group['media_ids']:
                path = f'{root}/AUDIO/WINDOWS/MEDIA/{media_id}.wem'
                assert sha(archive.read(path)) == group['sha256']
    print(args.output, sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
