"""APK validation, metadata extraction, and installation via adb."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, asdict
from typing import Optional

MAX_APK_SIZE = 512 * 1024 * 1024  # 512 MiB
ADB_TIMEOUT = 300


class ApkError(Exception):
    pass


@dataclass
class ApkMetadata:
    filename: str
    size_bytes: int
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    version_code: Optional[str] = None
    min_sdk: Optional[str] = None
    target_sdk: Optional[str] = None
    permissions: list[str] = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []

    def to_dict(self) -> dict:
        return asdict(self)


def validate_apk_path(path: str) -> None:
    if not os.path.isfile(path):
        raise ApkError("APK file not found")
    if not path.lower().endswith(".apk"):
        raise ApkError("File must have .apk extension")
    size = os.path.getsize(path)
    if size <= 0:
        raise ApkError("APK file is empty")
    if size > MAX_APK_SIZE:
        raise ApkError(f"APK exceeds maximum size of {MAX_APK_SIZE} bytes")
    # basic zip sanity
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if "AndroidManifest.xml" not in names:
                raise ApkError("APK is missing AndroidManifest.xml")
    except zipfile.BadZipFile:
        raise ApkError("APK is not a valid zip archive")


def find_aapt() -> Optional[str]:
    env = os.environ.get("DROIDSTAGE_AAPT")
    if env and os.path.isfile(env):
        return env
    for name in ("aapt", "aapt.exe", "aapt2", "aapt2.exe"):
        p = shutil.which(name)
        if p:
            return p
    return None


def extract_metadata(path: str) -> ApkMetadata:
    validate_apk_path(path)
    meta = ApkMetadata(filename=os.path.basename(path), size_bytes=os.path.getsize(path))
    aapt = find_aapt()
    if aapt:
        try:
            cp = subprocess.run(
                [aapt, "dump", "badging", path],
                capture_output=True, text=True, timeout=60, check=False,
            )
            text = cp.stdout
            m = re.search(r"package: name='([^']+)'", text)
            if m:
                meta.package_name = m.group(1)
            m = re.search(r"versionName='([^']*)'", text)
            if m:
                meta.version_name = m.group(1)
            m = re.search(r"versionCode='([^']*)'", text)
            if m:
                meta.version_code = m.group(1)
            m = re.search(r"sdkVersion:'([^']*)'", text)
            if m:
                meta.min_sdk = m.group(1)
            m = re.search(r"targetSdkVersion:'([^']*)'", text)
            if m:
                meta.target_sdk = m.group(1)
            meta.permissions = re.findall(r"uses-permission: name='([^']+)'", text)
        except Exception:
            pass
    return meta


def install_apk(serial: str, path: str, reinstall: bool = False) -> dict:
    validate_apk_path(path)
    adb = None
    from .device import find_adb

    adb = find_adb()
    if not adb:
        raise ApkError("adb not found")
    args = [adb, "-s", serial, "install"]
    if reinstall:
        args.append("-r")
    args.append(path)
    try:
        cp = subprocess.run(args, capture_output=True, text=True, timeout=ADB_TIMEOUT, check=False)
    except subprocess.TimeoutExpired:
        raise ApkError("APK installation timed out")
    output = (cp.stdout + "\n" + cp.stderr).strip()
    success = cp.returncode == 0 and "Success" in output
    return {"success": success, "returncode": cp.returncode, "output": output[-2000:]}


def list_packages(serial: str) -> list[str]:
    from .device import _run_adb

    cp = _run_adb(["shell", "pm", "list", "packages"], serial=serial)
    pkgs = []
    for line in cp.stdout.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            pkgs.append(line.split(":", 1)[1].strip())
    return sorted(pkgs)


def launch_package(serial: str, package: str) -> dict:
    # validate package name
    if not re.fullmatch(r"[A-Za-z0-9_.]+", package):
        raise ApkError("Invalid package name")
    from .device import _run_adb

    cp = _run_adb(["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"], serial=serial)
    output = (cp.stdout + cp.stderr).strip()
    return {"success": cp.returncode == 0, "output": output[-1000:]}


def uninstall_package(serial: str, package: str) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_.]+", package):
        raise ApkError("Invalid package name")
    from .device import _run_adb

    cp = _run_adb(["uninstall", package], serial=serial)
    output = (cp.stdout + cp.stderr).strip()
    success = "Success" in output
    return {"success": success, "output": output[-1000:]}
