FROM python:3.12-alpine

COPY src /app

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT [ "/bin/sh", "-c", "fastapi run" ]
