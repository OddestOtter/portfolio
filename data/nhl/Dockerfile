FROM quay.io/jupyter/scipy-notebook:latest

USER root
RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*
USER ${NB_UID}

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV DBT_PROFILES_DIR=/home/jovyan/work/dbt_project