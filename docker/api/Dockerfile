FROM --platform=linux/arm64 python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY migrations/ ./migrations/


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=src.api \
    FLASK_RUN_HOST=0.0.0.0


EXPOSE 5000


RUN adduser --disabled-password --gecos '' appuser

# Copy entrypoint(db migrations) script and make it executable
COPY docker/api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown appuser:appuser /entrypoint.sh
RUN dos2unix /entrypoint.sh 2>/dev/null || true

USER appuser

# Use the entrypoint script as a CMD
CMD ["/bin/sh", "/entrypoint.sh"]