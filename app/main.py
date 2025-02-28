import logging
from fastapi import FastAPI

from app.routers.router import router
from app.utils.metrics import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    # Saving logs to a file, as described in the exercise.
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s %(message)s",
)

app = FastAPI()

app.include_router(router)
