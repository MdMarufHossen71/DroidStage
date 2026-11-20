"""Physical Android device discovery and metadata via official adb."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from typing import List, Optional

ADB_TIMEOUT = 15


def find_adb() -> Optional[str]:
    env = os.environ.get("DROIDSTAGE_ADB")
    if env and os.path.isfile(env):
        return env
    # Common Android SDK locations (best-effort, no hard-coded user paths beyond env)
    for name in ("adb", "adb.exe"):
        path = shutil.which(name)
        if path:
            return path
    return None


class AdbNotFoundError(RuntimeError):
    pass


@dataclass
class Device:
    serial: str
    state: str  # device | unauthorized | offline | unknown
    model: Optional[str] = None
    product: Optional[str] = None
    device_name: Optional[str] = None
    transport_id: Optional[str] = None

    def to_dict(self, redact: bool = False) -> dict:
        data = asdict(self)
        if redact:
            data["serial"] = redact_serial(data["serial"])
        return data


# avoid circular import for redact; import lazily
def redact_serial(value: Optional[str]) -> str:
    from .security import redact_serial as _r

    return _r(value or "")


def _run_adb(args: List[str], serial: Optional[str] = None, timeout: int = ADB_TIMEOUT) -> subprocess.CompletedProcess:
    adb = find_adb()
    if not adb:
        raise AdbNotFoundError("adb not found. Install Android platform-tools from the official Android developer site.")
    cmd = [adb]
    if serial:
        cmd += ["-s", serial]
    cmd += args
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)


DEVICE_LINE_RE = re.compile(r"^(\S+)\s+(\S+)(.*)$")


def parse_devices_output(output: str) -> List[Device]:
    devices: List[Device] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue
        m = DEVICE_LINE_RE.match(line)
        if not m:
            continue
        serial, state, rest = m.group(1), m.group(2), m.group(3)
        dev = Device(serial=serial, state=state)
        # parse key:value tokens
        for token in rest.split():
            if ":" in token:
                k, v = token.split(":", 1)
                if k == "model":
                    dev.model = v
                elif k == "product":
                    dev.product = v
                elif k == "device":
                    dev.device_name = v
                elif k == "transport_id":
                    dev.transport_id = v
        devices.append(dev)
    return devices


def list_devices() -> List[Device]:
    cp = _run_adb(["devices", "-l"])
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or "adb devices failed")
    return parse_devices_output(cp.stdout)


def device_metadata(serial: str) -> dict:
    props = {}
    try:
        cp = _run_adb(["shell", "getprop"], serial=serial)
        for line in cp.stdout.splitlines():
            # [key]: [value]
            m = re.match(r"\[(.+?)\]:\s*\[(.*)\]", line)
            if m:
                props[m.group(1)] = m.group(2)
    except Exception:
        pass
    keys = {
        "ro.product.model": "model",
        "ro.product.brand": "brand",
        "ro.build.version.release": "android_version",
        "ro.build.version.sdk": "sdk_level",
        "ro.product.cpu.abi": "abi",
    }
    result = {}
    for src, dst in keys.items():
        if src in props:
            result[dst] = props[src]
    # storage (best effort)
    try:
        cp = _run_adb(["shell", "df", "/data"], serial=serial)
        lines = cp.stdout.splitlines()
        if len(lines) >= 2:
            parts = lines[-1].split()
            if len(parts) >= 4:
                result["storage_total"] = parts[1]
                result["storage_available"] = parts[3]
    except Exception:
        pass
    return result


def redact_device_for_log(dev: Device) -> dict:
    return {
        "state": dev.state,
        "model": dev.model,
        "product": dev.product,
        "serial": redact_serial(dev.serial),
    }
