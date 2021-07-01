FROM python:3.9.2

ENV PYTHONUNBUFFERED=1

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt
