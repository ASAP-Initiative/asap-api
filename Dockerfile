FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY src /app

WORKDIR /app

EXPOSE 8000

ENTRYPOINT [ "/bin/sh", "-c", "fastapi run" ]
