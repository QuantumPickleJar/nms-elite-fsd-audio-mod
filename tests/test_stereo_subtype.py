import struct
import unittest
from tools.stereo_subtype_probe import fix_stereo_config, standard_stereo_config
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

class GeneralStereoTests(StereoSubtypeTests):
    def test_long_clip_preserves_frames_and_payload(self):
        source = bytearray(self.source())
        struct.pack_into('<I', source, 44, 1658400)
        fixed = standard_stereo_config(bytes(source))
        self.assertEqual(struct.unpack_from('<I', fixed, 44)[0], 1658400)
        self.assertEqual(source[44:], fixed[44:])
        self.assertEqual(standard_stereo_config(fixed), fixed)

    def test_unknown_config_is_not_overwritten(self):
        source = bytearray(self.source())
        struct.pack_into('<I', source, 40, 0x9999)
        with self.assertRaises(ValueError):
            standard_stereo_config(bytes(source))
