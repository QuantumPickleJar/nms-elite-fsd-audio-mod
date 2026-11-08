"""Inspect modern Wwise seek/setup/audio packet framing; no audio writes."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

def packets(path):
    raw = path.read_bytes()
    chunks = {}
    p = 12
    while p + 8 <= len(raw):
        size = struct.unpack_from('<I', raw, p+4)[0]
        chunks[raw[p:p+4]] = raw[p+8:p+8+size]
        p += 8+size+(size&1)
    fmt, data = chunks[b'fmt '], chunks[b'data']
    seek, audio = struct.unpack_from('<II', fmt, 40)
    setup_size = struct.unpack_from('<H', data, seek)[0]
    assert seek+2+setup_size == audio
    setup = data[seek+2:audio]
    bits = int.from_bytes(setup, 'little')
    count = (bits & 255)+1
    indices = [(bits >> (8+10*i)) & 1023 for i in range(count)]
    lengths=[]
    p=audio
    while p<len(data):
        assert p+2<=len(data)
        size=struct.unpack_from('<H', data, p)[0]
        p+=2
        assert size and p+size<=len(data)
        lengths.append(size)
        p+=size
    assert p==len(data)
    return dict(samples=struct.unpack_from('<I',fmt,24)[0], channel_config=hex(struct.unpack_from('<I',fmt,20)[0]),
        uid=hex(struct.unpack_from('<I',fmt,60)[0]), seek_bytes=seek, setup_bytes=setup_size,
        codebook_indices=indices, audio_packets=len(lengths), min_packet=min(lengths), max_packet=max(lengths),
        data_sha256=hashlib.sha256(data).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wem', type=Path, nargs='+')
    args=parser.parse_args()
    print(json.dumps([packets(p) for p in args.wem], indent=2))
