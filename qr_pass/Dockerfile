FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD gunicorn --bind 0.0.0.0:8000 --chdir qr_pass/ qr_pass.wsgi
