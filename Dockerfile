FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN uv pip install --system -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/docker/start_services.sh

EXPOSE 7860 8000

ENV GRADIO_PORT=7860 \
    API_PORT=8000 \
    DEVICE=cpu

CMD ["/app/docker/start_services.sh"]
