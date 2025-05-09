FROM --platform=linux/arm64 python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


RUN adduser --disabled-password --gecos '' appuser
USER appuser


CMD ["python", "-m", "rq.cli", "worker", "order_processing"]