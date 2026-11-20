import os
import secrets
from typing import Optional

from fastapi import HTTPException, Request

# Per-process session token. Can be overridden for tests via env.
SESSION_TOKEN: str = os.environ.get("DROIDSTAGE_TOKEN") or secrets.token_urlsafe(32)

ALLOWED_ORIGINS_ENV = "DROIDSTAGE_ALLOWED_ORIGINS"


def allowed_origins(port: int) -> set[str]:
    base = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
    extra = os.environ.get(ALLOWED_ORIGINS_ENV, "")
    for item in extra.split(","):
        item = item.strip()
        if item:
            base.add(item)
    return base


def validate_origin(request: Request, port: int) -> None:
    origin = request.headers.get("origin")
    if origin is None:
        # Non-browser or same-origin navigation; allow but token still required.
        return
    if origin not in allowed_origins(port):
        raise HTTPException(status_code=403, detail="Origin not allowed")


def require_token(request: Request) -> None:
    token = request.headers.get("x-droidstage-token")
    if token is None:
        token = request.query_params.get("token")
    if not token or not secrets.compare_digest(token, SESSION_TOKEN):
        raise HTTPException(status_code=401, detail="Missing or invalid session token")


def redact_serial(value: Optional[str]) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return "***"
    return value[:2] + "***" + value[-2:]
