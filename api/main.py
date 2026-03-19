"""
main.py
=======
FastAPI application entry point.

Run with:
    python -m api.main
"""

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
        "docs"    : "http://localhost:8000/docs",
        "health"  : "http://localhost:8000/health",
        "predict" : "POST http://localhost:8000/predict",
    }


if __name__ == "__main__":
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)