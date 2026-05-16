FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY medcontrol/ ./medcontrol/
COPY data/ ./data/ 2>/dev/null || true

RUN pip install --no-cache-dir requests

RUN mkdir -p data

CMD ["python", "-m", "medcontrol.app"]
