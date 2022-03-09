FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY bot .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt