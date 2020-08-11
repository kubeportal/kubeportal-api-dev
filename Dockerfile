# server setup
FROM python:3.8

RUN mkdir api

COPY api/ api/

COPY requirements.txt api/

WORKDIR api

RUN chmod +x requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --compile

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

CMD flask run --host 0.0.0.0