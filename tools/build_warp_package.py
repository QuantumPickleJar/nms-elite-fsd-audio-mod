"""Encode the six recovered sources into the historical 23-media warp map."""
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

ROOT='NMS_FSD_Warp_StereoVorbis'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(args):
    return subprocess.run([str(x) for x in args],check=True,capture_output=True,text=True).stdout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--mapping',type=Path,default=Path('data/legacy_audio_manifest.json'))
    parser.add_argument('--wav2wem',required=True)
    parser.add_argument('--vgmstream',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise SystemExit('refusing to overwrite an existing package')
    mapping=json.loads(args.mapping.read_text())['entries']
    ids=[e['wem_id'] for e in mapping]
    if len(ids)!=23 or len(set(ids))!=23 or not all(i.isdecimal() for i in ids):
        raise ValueError('expected 23 unique decimal media IDs')
    converted={}; reports=[]
    with tempfile.TemporaryDirectory(prefix='nms-fsd-warp-') as tmp:
        work=Path(tmp)
        for relative in sorted({e['recovered_wav'] for e in mapping}):
            source=args.source_root/relative
            with wave.open(str(source),'rb') as w:
                frames,rate,channels=w.getnframes(),w.getframerate(),w.getnchannels()
            if (rate,channels)!=(48000,2):
                raise ValueError('source must be 48 kHz stereo')
            ogg=work/'input.ogg';wem=work/'output.wem';decoded=work/'decoded.wav'
            run(['ffmpeg','-v','error','-y','-i',source,'-map_metadata','-1','-c:a','libvorbis','-q:a','6','-ar','48000','-ac','2',ogg])
            run([args.wav2wem,ogg,'-o',wem])
            raw=wem.read_bytes();fixed=standard_stereo_config(raw);wem.write_bytes(fixed)
            info=inspect_wem_bytes(fixed)
            if info.total_pcm_frames!=frames or info.subtype!=0x3102:
                raise ValueError('WEM frame count or stereo configuration mismatch')
            framing=packets(wem)
            run([args.vgmstream,'-o',decoded,wem])
            with wave.open(str(decoded),'rb') as w:
                if (w.getnframes(),w.getframerate(),w.getnchannels())!=(frames,rate,channels):
                    raise ValueError('decoded WAV does not match source frame count/rate/channels')
            converted[relative]=fixed
            reports.append(dict(source=relative,source_sha256=sha(source.read_bytes()),wem_sha256=sha(fixed),
                duration_seconds=frames/rate,frames=frames,decode_pass=True,audio_packets=framing['audio_packets']))
            print(f'encoded and decoded {relative}: {frames} frames')
        manifest=dict(status='codec passed user quick-menu A/B; warp event dispatch and timing need game test',
            timing_policy='recovered clip durations and mapping preserved; no undocumented offsets added',
            codec='Wwise Vorbis, libvorbis q6, 48kHz stereo, standard channel config 0x3102',
            wav2wem_revision='38e916953bec63862b13b449d780d1303a1bf29c',
            bank_files=0,unique_sources=reports,files=[])
        with zipfile.ZipFile(args.output,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for e in mapping:
                relative=e['recovered_wav'];data=converted[relative]
                path=f'{ROOT}/AUDIO/WINDOWS/MEDIA/{e["wem_id"]}.wem'
                z.writestr(path,data)
                manifest['files'].append(dict(path=path,sha256=sha(data),duration_seconds=next(r['duration_seconds'] for r in reports if r['source']==relative)))
            z.writestr(f'{ROOT}/MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
            z.writestr(f'{ROOT}/README_TEST.txt',
                'Warp audio test: corrected stereo Vorbis, historical 23-media map.\n'
                'Exit NMS. Disable earlier FSD/quick-menu probes. Extract this folder into\n'
                'GAMEDATA/MODS; AUDIO must sit directly under the package root. Enable it\n'
                'and test pulse-to-system seamless warp. Report countdown, engine, timing,\n'
                'and any unchanged or overlapping effects. To roll back, exit and move\n'
                'only this package root outside MODS. No BNK included.\n'
                'Original source durations are preserved: 1s cues, 1.5s cue, 34.55s recording.\n'
                'Earlier precise offsets were not recovered; event IDs remain a historical\n'
                'mapping requiring this game test. This package does not change bank timing.\n')
    with zipfile.ZipFile(args.output) as z:
        assert len([n for n in z.namelist() if n.endswith('.wem')])==23
        assert not any(n.lower().endswith('.bnk') for n in z.namelist())
        for e in manifest['files']:
            assert sha(z.read(e['path']))==e['sha256']
    print('created:',args.output,'SHA-256:',sha(args.output.read_bytes()))

if __name__=='__main__':
    main()
