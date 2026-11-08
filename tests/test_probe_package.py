from __future__ import annotations

import unittest

from tools.build_quickmenu_probe import (
    MEDIA_PREFIX,
    MOD_ROOT,
    QUICKMENU_IDS,
    expected_archive_paths,
    validate_archive_paths,
)


class ProbePackageTests(unittest.TestCase):
    def test_expected_layout_places_audio_directly_under_mod_root(self) -> None:
        paths = expected_archive_paths()
        validate_archive_paths(sorted(paths))
        for media_id in QUICKMENU_IDS:
            self.assertIn(f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA/{media_id}.wem", paths)
        self.assertEqual(MEDIA_PREFIX, f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA")

    def test_rejects_a_persistent_bank(self) -> None:
        paths = expected_archive_paths() | {
            f"{MOD_ROOT}/AUDIO/WINDOWS/NMS_AUDIO_PERSISTENT.BNK"
        }
        with self.assertRaisesRegex(RuntimeError, "must not contain"):
            validate_archive_paths(sorted(paths))

    def test_rejects_a_nested_audio_root(self) -> None:
        paths = expected_archive_paths()
        paths.remove(f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA/{QUICKMENU_IDS[0]}.wem")
        paths.add(
            f"{MOD_ROOT}/NMS_FSD_SeamlessWarp/AUDIO/WINDOWS/MEDIA/"
            f"{QUICKMENU_IDS[0]}.wem"
        )
        with self.assertRaisesRegex(RuntimeError, "unexpected ZIP layout"):
            validate_archive_paths(sorted(paths))

    def test_rejects_a_missing_variant(self) -> None:
        paths = expected_archive_paths()
        paths.remove(f"{MOD_ROOT}/AUDIO/WINDOWS/MEDIA/{QUICKMENU_IDS[0]}.wem")
        with self.assertRaisesRegex(RuntimeError, "unexpected ZIP layout"):
            validate_archive_paths(sorted(paths))


if __name__ == "__main__":
    unittest.main()
