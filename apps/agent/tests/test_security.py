import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("DROIDSTAGE_TOKEN", "test-token")
os.environ.setdefault("DROIDSTAGE_PORT", "8787")

from fastapi.testclient import TestClient

from app.main import create_app
from app import security

app = create_app()
client = TestClient(app)


def test_health_no_token():
    r = client.get("/api/health")
    assert r.status_code == 200


def test_devices_requires_token():
    r = client.get("/api/devices")
    assert r.status_code == 401


def test_devices_with_token():
    r = client.get("/api/devices", headers={"X-DroidStage-Token": "test-token"})
    # adb may be missing => 503, but not 401/403
    assert r.status_code in (200, 503)


def test_origin_rejected():
    r = client.get(
        "/api/devices",
        headers={"X-DroidStage-Token": "test-token", "Origin": "http://evil.example"},
    )
    assert r.status_code == 403


def test_redact_serial():
    assert security.redact_serial("ABCDEF1234") == "AB***34"
    assert security.redact_serial("ab") == "***"
