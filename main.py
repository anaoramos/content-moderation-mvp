import logging

import uvicorn
from fastapi import FastAPI
from app.api.router import router

logging.basicConfig(
    filename="server.log",
    # Saving logs to a file, as described in the exercise.
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s %(message)s'
)

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
