
FROM python:3.11-slim

RUN groupadd -r praktikum && useradd -r -g praktikum praktikum
WORKDIR /app
RUN chown -R praktikum:praktikum /app
COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY --chown=praktikum . ./
EXPOSE 8000
USER praktikum