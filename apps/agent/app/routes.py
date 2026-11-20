from __future__ import annotations

import os
import re
import tempfile
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import security
from fastapi.responses import Response

from .apk import (
    ApkError,
    extract_metadata,
    install_apk,
    launch_package,
    list_packages,
    uninstall_package,
    validate_apk_path,
)
from .device import AdbNotFoundError, device_metadata, list_devices
from .files import FileOpError, pull_file, push_file, read_logcat, screenshot_png, validate_device_path

router = APIRouter(prefix="/api", tags=["api"])


def _port(request: Request) -> int:
    return request.url.port or 8787


def _validate_serial(serial: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9:._-]+", serial):
        raise HTTPException(status_code=400, detail="Invalid device serial")


def _guard(request: Request) -> None:
    security.validate_origin(request, _port(request))
    security.require_token(request)


@router.get("/health")
def health():
    from .device import find_adb

    return {"status": "ok", "adb": find_adb() is not None}


@router.get("/devices")
def devices(request: Request):
    _guard(request)
    try:
        devs = list_devices()
    except AdbNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    result = []
    for d in devs:
        meta = {}
        if d.state == "device":
            try:
                meta = device_metadata(d.serial)
            except Exception:
                meta = {}
        item = d.to_dict()
        item["metadata"] = meta
        result.append(item)
    return {"devices": result}


class InstallConfirmRequest(BaseModel):
    serial: str = Field(..., min_length=1, max_length=128)
    path: Optional[str] = None
    confirm: bool = False


@router.post("/apk/metadata")
async def apk_metadata(request: Request, file: UploadFile = File(...)):
    _guard(request)
    if not file.filename or not file.filename.lower().endswith(".apk"):
        raise HTTPException(status_code=400, detail="Only .apk files are supported")
    # size limit
    MAX = 512 * 1024 * 1024
    data = await file.read(MAX + 1)
    if len(data) > MAX:
        raise HTTPException(status_code=413, detail="APK too large")
    tmpdir = tempfile.mkdtemp(prefix="droidstage-")
    path = os.path.join(tmpdir, os.path.basename(file.filename))
    with open(path, "wb") as f:
        f.write(data)
    try:
        meta = extract_metadata(path)
    except ApkError as e:
        raise HTTPException(status_code=400, detail=str(e))
    meta_dict = meta.to_dict()
    meta_dict["staged_path"] = path
    return meta_dict


@router.post("/apk/install")
def apk_install(request: Request, payload: InstallConfirmRequest):
    _guard(request)
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="Explicit confirmation required")
    _validate_serial(payload.serial)
    if not payload.path:
        raise HTTPException(status_code=400, detail="staged_path required")
    # prevent path traversal: must be under temp
    if not os.path.abspath(payload.path).startswith(tempfile.gettempdir()):
        raise HTTPException(status_code=400, detail="Invalid staged path")
    validate_apk_path(payload.path)
    try:
        result = install_apk(payload.serial, payload.path)
    except ApkError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # cleanup
    try:
        os.remove(payload.path)
    except OSError:
        pass
    return result


@router.get("/packages")
def packages(request: Request, serial: str):
    _guard(request)
    _validate_serial(serial)
    try:
        pkgs = list_packages(serial)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"packages": pkgs}


class PackageAction(BaseModel):
    serial: str = Field(..., min_length=1, max_length=128)
    package: str = Field(..., min_length=1, max_length=256)


@router.post("/packages/launch")
def launch(request: Request, payload: PackageAction):
    _guard(request)
    _validate_serial(payload.serial)
    try:
        return launch_package(payload.serial, payload.package)
    except ApkError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/packages/uninstall")
def uninstall(request: Request, payload: PackageAction, confirm: bool = False):
    _guard(request)
    _validate_serial(payload.serial)
    if not confirm:
        raise HTTPException(status_code=400, detail="Explicit confirmation required")
    try:
        return uninstall_package(payload.serial, payload.package)
    except ApkError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/screenshot")
def screenshot(request: Request, serial: str):
    _guard(request)
    _validate_serial(serial)
    try:
        png = screenshot_png(serial)
    except FileOpError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png, media_type="image/png")


@router.post("/files/push")
async def files_push(
    request: Request,
    serial: str = Form(...),
    device_path: str = Form(...),
    file: UploadFile = File(...),
):
    _guard(request)
    _validate_serial(serial)
    try:
        validate_device_path(device_path)
    except FileOpError as e:
        raise HTTPException(status_code=400, detail=str(e))
    MAX = 256 * 1024 * 1024
    data = await file.read(MAX + 1)
    if len(data) > MAX:
        raise HTTPException(status_code=413, detail="File too large")
    tmpdir = tempfile.mkdtemp(prefix="droidstage-push-")
    local = os.path.join(tmpdir, os.path.basename(file.filename or "upload.bin"))
    with open(local, "wb") as f:
        f.write(data)
    try:
        result = push_file(serial, local, device_path)
    except FileOpError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        try:
            os.remove(local)
        except OSError:
            pass
    return result


@router.get("/files/pull")
def files_pull(request: Request, serial: str, device_path: str):
    _guard(request)
    _validate_serial(serial)
    try:
        validate_device_path(device_path)
        local = pull_file(serial, device_path)
    except FileOpError as e:
        raise HTTPException(status_code=400, detail=str(e))
    with open(local, "rb") as f:
        data = f.read()
    try:
        os.remove(local)
    except OSError:
        pass
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{os.path.basename(device_path)}"'},
    )


@router.get("/logcat")
def logcat(request: Request, serial: str, lines: int = 200):
    _guard(request)
    _validate_serial(serial)
    try:
        text = read_logcat(serial, lines)
    except FileOpError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"log": text}
