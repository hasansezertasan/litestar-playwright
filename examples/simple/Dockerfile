# syntax=docker/dockerfile:1.7

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates tini \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies first for better layer caching.
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN pip install --upgrade pip \
    && pip install .

# Install browser binaries and required system packages.
RUN playwright install --with-deps chromium

# Copy only the example app code.
COPY examples/simple /app/examples/simple

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser
WORKDIR /app/examples/simple

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')"

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "main.py"]
