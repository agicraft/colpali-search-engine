FROM python:3.12.3

WORKDIR /app

RUN apt -y update && \
  apt install -y --no-install-recommends poppler-utils libreoffice && \
  rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY ./requirements.txt ./requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache \
  pip install -r requirements.txt

COPY ./src ./src

CMD ["python", "-m", "uvicorn", "src.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "3000"]
