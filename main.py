import os

from fastapi import FastAPI

from rest import controller

app = FastAPI()
app.include_router(controller.router)

if __name__ == "__main__":
    os.execlp(
        "gunicorn",
        "gunicorn",
        "--bind",
        "0.0.0.0",
        "--workers",
        "2",
        "--worker-class",
        "uvicorn.workers.UvicornWorker",
        "main:app",
    )
