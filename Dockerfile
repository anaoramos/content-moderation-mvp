FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY . /app/

RUN poetry install --no-root

CMD ["poetry", "run", "fastapi", "run", "app/main.py", "--port", "8000"]
