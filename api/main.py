"""
main.py
=======
FastAPI application entry point.

Run with:
    python -m api.main
"""

import os                          # ADD THIS LINE
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_HOST, API_PORT
from api.routes import router

app = FastAPI(
    title       = API_TITLE,
    description = API_DESCRIPTION,
    version     = API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(router)


@app.get("/", tags=["System"])
def root():
    return {
        "message" : "Islamabad House Price Predictor API",
        "docs"    : "/docs",           # CHANGED from hardcoded localhost
        "health"  : "/health",         # CHANGED from hardcoded localhost
        "predict" : "POST /predict",   # CHANGED from hardcoded localhost
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", API_PORT))   # CHANGED — reads Render's PORT
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=False)  # CHANGED