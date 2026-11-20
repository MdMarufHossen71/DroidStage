import os
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.apk import ApkError, validate_apk_path, extract_metadata


def make_apk(path, bad=False):
    with zipfile.ZipFile(path, "w") as z:
        if not bad:
            z.writestr("AndroidManifest.xml", "<manifest/>")


def test_validate_ok():
    fd, p = tempfile.mkstemp(suffix=".apk")
    os.close(fd)
    make_apk(p)
    validate_apk_path(p)  # no exception
    os.remove(p)


def test_validate_missing_manifest():
    fd, p = tempfile.mkstemp(suffix=".apk")
    os.close(fd)
    make_apk(p, bad=True)
    try:
        validate_apk_path(p)
        assert False, "expected error"
    except ApkError:
        pass
    os.remove(p)


def test_validate_wrong_ext():
    fd, p = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        validate_apk_path(p)
        assert False
    except ApkError:
        pass
    os.remove(p)


def test_extract_metadata_no_aapt():
    fd, p = tempfile.mkstemp(suffix=".apk")
    os.close(fd)
    make_apk(p)
    m = extract_metadata(p)
    assert m.filename.endswith(".apk")
    assert m.size_bytes > 0
    os.remove(p)
