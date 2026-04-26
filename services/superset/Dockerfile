# syntax=docker/dockerfile:1

FROM apache/superset:latest

USER root

RUN apt-get update && apt-get install -y --no-install-recommends bash 
RUN pip install --upgrade pip --no-cache-dir
RUN pip install uv --no-cache-dir
RUN uv pip install psycopg2-binary

USER superset

COPY ./services/superset/superset_config.py /app/pythonpath/superset_config.py
