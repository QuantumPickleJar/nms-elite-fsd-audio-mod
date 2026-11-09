"""Synthetic scope checks for the media-only bank diagnostic."""

import struct
import unittest
from unittest.mock import patch

from tests.test_charging_bank import fixture
from tools import build_charging_bank_probe as bank
from tools import build_charging_media_probe as media


class MediaOnlyBankTests(unittest.TestCase):
    def test_unknown_bank_rejected(self):
        with self.assertRaises(ValueError):
            media.patch_media_only(fixture(), b'new-wem', 12345)

    def test_only_one_sound_and_media_entry_change(self):
        native = fixture()
        with patch.object(media, 'NATIVE_SHA', bank.sha(native)):
            output, report = media.patch_media_only(native, b'new-wem', 12345)
        before = dict(bank.split_chunks(native))
        after = dict(bank.split_chunks(output))
        for tag in (b'BKHD', b'STID'):
            self.assertEqual(after[tag], before[tag])
        self.assertEqual(after[b'DATA'][:len(before[b'DATA'])], before[b'DATA'])
        target, offset, size = struct.unpack('<III', after[b'DIDX'])
        self.assertEqual((target, size, offset % 16), (bank.FIRST_MEDIA, 7, 0))
        self.assertEqual(after[b'DATA'][offset:offset + size], b'new-wem')
        original = {bank.u32(body): body for _, body in bank.records(before[b'HIRC'])}
        changed = {bank.u32(body): body for _, body in bank.records(after[b'HIRC'])}
        self.assertEqual(set(original), set(changed))
        self.assertEqual({key for key in original if original[key] != changed[key]},
                         {bank.FIRST_SOUND})
        self.assertEqual(bank.u32(changed[bank.FIRST_SOUND], 13), 12345)
        self.assertEqual(bank.u32(changed[bank.FIRST_SOUND], 17), 7)
        self.assertEqual(report['new_hirc_count'], 0)


if __name__ == '__main__':
    unittest.main()
