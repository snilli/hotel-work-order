FROM python:3.11-slim-bullseye as python-builder

# System Dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential libpq-dev

# install python dependencies
COPY ./apps/requirements/requirements.txt ./

RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt





FROM python:3.11-slim-bullseye

ENV APP_HOME=/apps

WORKDIR $APP_HOME

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends postgresql

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

COPY --from=python-builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip
RUN pip install --no-cache --no-deps /wheels/*

COPY ./apps .
COPY docker-entrypoint.sh /apps

ENV DJANGO_SETTINGS_MODULE=apps.settings
ENTRYPOINT ["sh", "-c", "/apps/docker-entrypoint.sh"]
