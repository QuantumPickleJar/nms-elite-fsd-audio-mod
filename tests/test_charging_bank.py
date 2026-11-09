"""Synthetic bank tests; no game or third-party media fixtures."""
import struct
import unittest
from unittest.mock import patch

from tools import build_charging_bank_probe as bank


def fixture():
    sound = bytearray(53)
    struct.pack_into('<II', sound, 0, bank.FIRST_SOUND, 0x40001)
    struct.pack_into('<I', sound, 9, bank.FIRST_MEDIA)
    struct.pack_into('<I', sound, 17, 3)
    container = bytearray(211)
    struct.pack_into('<I', container, 0, bank.CONTAINER)
    container[83:85] = b'\x00\x12'
    struct.pack_into('<I', container, 131, bank.FIRST_SOUND)
    objects = [(2, bytes(sound)), (5, bytes(container))]
    objects += [(4, struct.pack('<IBI', event, 1, 123)) for event in bank.END_EVENTS]
    objects += [(2, struct.pack('<I', 999)+b'unrelated-object')]
    hirc = struct.pack('<I', len(objects)) + b''.join(
        struct.pack('<BI', kind, len(body))+body for kind, body in objects)
    chunks = [(b'BKHD', b'unchanged-header'),
              (b'DIDX', struct.pack('<III', bank.FIRST_MEDIA, 0, 3)),
              (b'DATA', b'old'), (b'HIRC', hirc), (b'STID', b'unchanged-strings')]
    return b''.join(struct.pack('<4sI', tag, len(body))+body for tag, body in chunks)


class ChargingBankTests(unittest.TestCase):
    def test_unknown_bank_rejected(self):
        with self.assertRaises(ValueError):
            bank.patch_bank(fixture(), b'new-wem')

    def test_media_append_preserves_original_and_unrelated_objects(self):
        native = fixture()
        with patch.object(bank, 'NATIVE_SHA', bank.sha(native)):
            result, report = bank.patch_bank(native, b'new-wem')
        before, after = dict(bank.split_chunks(native)), dict(bank.split_chunks(result))
        self.assertEqual(after[b'DATA'][:3], b'old')
        id, offset, size = struct.unpack('<III', after[b'DIDX'])
        self.assertEqual((id, size, offset % 16), (bank.FIRST_MEDIA, 7, 0))
        self.assertEqual(after[b'DATA'][offset:offset+size], b'new-wem')
        self.assertEqual(before[b'BKHD'], after[b'BKHD'])
        self.assertEqual(before[b'STID'], after[b'STID'])
        records = {bank.u32(body): body for _, body in bank.records(after[b'HIRC'])}
        self.assertEqual(records[999], struct.pack('<I', 999)+b'unrelated-object')
        self.assertEqual(bank.u32(records[bank.FIRST_SOUND], 17), 7)
        self.assertEqual(report['patched_hirc_count'], report['original_hirc_count']+1)

    def test_step_sequence_and_both_end_resets(self):
        native = fixture()
        with patch.object(bank, 'NATIVE_SHA', bank.sha(native)):
            result, _ = bank.patch_bank(native, b'new-wem')
        records = {bank.u32(body): body for _, body in bank.records(dict(bank.split_chunks(result))[b'HIRC'])}
        self.assertEqual(records[bank.CONTAINER][83:85], b'\x01\x10')
        for event in bank.END_EVENTS:
            self.assertEqual(records[event][4], 2)
            self.assertEqual(bank.u32(records[event], 9), bank.RESET_ACTION)
        reset = records[bank.RESET_ACTION]
        self.assertEqual(struct.unpack_from('<HI', reset, 4), (0x2203, bank.CONTAINER))


if __name__ == '__main__':
    unittest.main()
