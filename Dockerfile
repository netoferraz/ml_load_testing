FROM python:3.7.9-slim-buster as base

WORKDIR /app

FROM base as builder

ARG LOCAL_USER_ID=1000

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1\
    PYTHONWARNINGS="ignore"

RUN adduser --system -u ${LOCAL_USER_ID:-1000} app && \
    apt-get update && \
    apt-get -qq -y install curl && \ 
    apt-get install gcc libpq-dev -y && \
    apt-get install python-dev python-pip -y && \
    apt-get install python3-dev python3-pip python3-venv python3-wheel -y && \
    pip install wheel

COPY lmodel-requirements.txt ./
RUN pip install -r lmodel-requirements.txt

COPY . .

RUN chown app -R /app/
USER app
CMD [ "python", "api.py" ]
