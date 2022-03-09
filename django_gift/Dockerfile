FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY django_gift/scripts scripts

RUN ["chmod", "+x", "scripts/web/startup.sh"]

WORKDIR /code

COPY django_gift .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
