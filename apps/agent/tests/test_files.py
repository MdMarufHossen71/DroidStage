import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.files import validate_device_path, FileOpError


def test_valid_paths():
    validate_device_path("/sdcard/Download/x.bin")
    validate_device_path("/data/local/tmp/test.apk")
    validate_device_path("/storage/emulated/0/Pictures")


def test_invalid_paths():
    for p in ["/etc/passwd", "../x", "/sdcard/../etc", "sdcard/x", "/data/x", ""]:
        try:
            validate_device_path(p)
            assert False, p
        except FileOpError:
            pass
