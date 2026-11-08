import struct
import unittest
from tools.stereo_subtype_probe import fix_stereo_config
from test_wem_inspect import make_wem

class StereoSubtypeTests(unittest.TestCase):
    def source(self):
        data = bytearray(make_wem())
        struct.pack_into('<I', data, 40, 0)
        return bytes(data)

    def test_changes_only_channel_configuration(self):
        source = self.source()
        fixed = fix_stereo_config(source)
        self.assertEqual(struct.unpack_from('<I', fixed, 40)[0], 0x3102)
        self.assertEqual(source[:40], fixed[:40])
        self.assertEqual(source[44:], fixed[44:])
        self.assertEqual(len(source), len(fixed))

    def test_rejects_already_configured_input(self):
        with self.assertRaises(ValueError):
            fix_stereo_config(fix_stereo_config(self.source()))

    def test_rejects_mono_input(self):
        data = bytearray(self.source())
        struct.pack_into('<H', data, 22, 1)
        with self.assertRaises(ValueError):
            fix_stereo_config(bytes(data))
