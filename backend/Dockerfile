FROM ubuntu:latest
LABEL authors="user"

ENTRYPOINT ["top", "-b"]


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /home/app/backend


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

