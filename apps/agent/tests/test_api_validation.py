import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DROIDSTAGE_TOKEN", "test-token")
os.environ.setdefault("DROIDSTAGE_PORT", "8787")

from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())
H = {"X-DroidStage-Token": "test-token"}


def test_install_requires_confirm():
    r = client.post(
        "/api/apk/install",
        json={"serial": "ABC", "path": "/tmp/x.apk", "confirm": False},
        headers=H,
    )
    assert r.status_code == 400


def test_install_requires_path():
    r = client.post(
        "/api/apk/install",
        json={"serial": "ABC", "confirm": True},
        headers=H,
    )
    assert r.status_code == 400


def test_invalid_serial_rejected():
    r = client.post(
        "/api/apk/install",
        json={"serial": "bad serial!", "path": "/tmp/x.apk", "confirm": True},
        headers=H,
    )
    assert r.status_code == 400


def test_uninstall_requires_confirm():
    r = client.post(
        "/api/packages/uninstall?confirm=false",
        json={"serial": "ABC", "package": "com.example.app"},
        headers=H,
    )
    assert r.status_code == 400
