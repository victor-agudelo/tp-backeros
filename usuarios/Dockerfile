# ---- Base python ----
FROM python:3.13 AS base
WORKDIR /usuarios

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt requirements.txt
RUN python -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache

# ---- Builder ----
FROM dependencies AS builder
COPY . .

# --- Release with Slim ----
FROM python:3.13-slim AS runner
WORKDIR /usuarios
RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY --from=dependencies /venv /venv

# --- Install dependencies ----
COPY --from=builder /usuarios /usuarios

# --- Set environment variables for virtualenv ---
ENV PATH="/venv/bin:$PATH"

RUN addgroup --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser appuser \
    && chown -R appuser:appuser /usuarios

USER appuser

EXPOSE 8001

# --- Run the app ---
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]