"""File transfer, screenshot, and logcat helpers via official adb."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from typing import Optional

from .device import _run_adb, find_adb

MAX_TRANSFER_SIZE = 256 * 1024 * 1024  # 256 MiB


class FileOpError(Exception):
    pass


_SAFE_DEVICE_PATH_RE = re.compile(r"^/(sdcard|storage|data/local/tmp)(/[A-Za-z0-9._/\-]+)?$")


def validate_device_path(path: str) -> None:
    if not path or not path.startswith("/"):
        raise FileOpError("Device path must be absolute")
    if ".." in path.split("/"):
        raise FileOpError("Path traversal not allowed")
    if not _SAFE_DEVICE_PATH_RE.match(path):
        raise FileOpError("Device path must be under /sdcard, /storage, or /data/local/tmp")


def screenshot_png(serial: str) -> bytes:
    adb = find_adb()
    if not adb:
        raise FileOpError("adb not found")
    try:
        cp = subprocess.run(
            [adb, "-s", serial, "exec-out", "screencap", "-p"],
            capture_output=True, timeout=30, check=False,
        )
    except subprocess.TimeoutExpired:
        raise FileOpError("Screenshot timed out")
    if cp.returncode != 0 or not cp.stdout:
        raise FileOpError(cp.stderr.decode("utf-8", "replace").strip() or "Screenshot failed")
    if not cp.stdout.startswith(b"\x89PNG"):
        raise FileOpError("Device did not return a PNG image")
    return cp.stdout


def push_file(serial: str, local_path: str, device_path: str) -> dict:
    validate_device_path(device_path)
    if not os.path.isfile(local_path):
        raise FileOpError("Local file not found")
    if os.path.getsize(local_path) > MAX_TRANSFER_SIZE:
        raise FileOpError("File too large")
    cp = _run_adb(["push", local_path, device_path], serial=serial, timeout=300)
    output = (cp.stdout + cp.stderr).strip()
    return {"success": cp.returncode == 0, "output": output[-2000:]}


def pull_file(serial: str, device_path: str) -> str:
    validate_device_path(device_path)
    adb = find_adb()
    if not adb:
        raise FileOpError("adb not found")
    fd, local_path = tempfile.mkstemp(prefix="droidstage-pull-")
    os.close(fd)
    os.remove(local_path)
    cp = _run_adb(["pull", device_path, local_path], serial=serial, timeout=300)
    if cp.returncode != 0:
        try:
            os.remove(local_path)
        except OSError:
            pass
        raise FileOpError((cp.stdout + cp.stderr).strip() or "Pull failed")
    return local_path


def read_logcat(serial: str, lines: int = 200) -> str:
    if lines < 1 or lines > 5000:
        raise FileOpError("lines must be between 1 and 5000")
    cp = _run_adb(["logcat", "-d", "-t", str(lines)], serial=serial, timeout=30)
    output = cp.stdout
    if cp.returncode != 0 and not output:
        raise FileOpError(cp.stderr.strip() or "logcat failed")
    return output