import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.device import parse_devices_output


SAMPLE = """List of devices attached
ABC123 device product:bar device:foo model:Pixel_7 transport_id:3
XYZ999 unauthorized
OFF111 offline
"""


def test_parse_devices():
    devs = parse_devices_output(SAMPLE)
    assert len(devs) == 3
    assert devs[0].serial == "ABC123"
    assert devs[0].state == "device"
    assert devs[0].model == "Pixel_7"
    assert devs[1].state == "unauthorized"
    assert devs[2].state == "offline"


def test_empty():
    assert parse_devices_output("List of devices attached\n") == []
