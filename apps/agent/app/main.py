import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import router
from . import security

DEFAULT_PORT = int(os.environ.get("DROIDSTAGE_PORT", "8787"))
HOST = "127.0.0.1"


def create_app() -> FastAPI:
    app = FastAPI(title="DroidStage Agent", version="0.1.0")
    # CORS only for loopback dev origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=sorted(security.allowed_origins(DEFAULT_PORT)),
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.include_router(router)

    # Serve built web UI if present (production)
    web_dist = Path(__file__).resolve().parents[3] / "apps" / "web" / "dist"
    if web_dist.is_dir():
        app.mount("/", StaticFiles(directory=str(web_dist), html=True), name="web")
    return app


app = create_app()


def run() -> None:
    print(f"DROIDSTAGE_TOKEN={security.SESSION_TOKEN}")
    print(f"DROIDSTAGE_URL=http://127.0.0.1:{DEFAULT_PORT}/?token={security.SESSION_TOKEN}")
    uvicorn.run(app, host=HOST, port=DEFAULT_PORT, log_level="info")


if __name__ == "__main__":
    run()
