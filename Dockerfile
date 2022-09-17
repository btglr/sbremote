FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install git -y

WORKDIR /app

ENV CONFIG_DIR=/config
RUN git clone https://github.com/btglr/sbremote.git && cd sbremote && ./setup.sh