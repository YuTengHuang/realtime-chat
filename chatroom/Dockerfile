## 環境build
FROM python:3.11.2 AS build

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && apt-get --no-install-recommends install -y gcc

COPY ./requirements.txt ./

RUN --mount=type=cache,target=~/.cache/pip \
    pip wheel --wheel-dir /app/wheels \
    -r /app/requirements.txt


## production
FROM python:3.11.2-slim-bullseye AS production

ENV PYTHONDONTWRITEBYTECODE=1

ARG APP_USER='django_user'

WORKDIR /app

COPY --from=build /app/wheels ./wheels
COPY --from=build /app/requirements.txt .

RUN pip install --no-cache ./wheels/* \
    && rm -r ./wheels

COPY . .

RUN useradd -r -s /bin/false ${APP_USER} && \
    chown -R ${APP_USER}:${APP_USER} /app && \
    chmod +x /app/start.sh

USER ${APP_USER}

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "./start.sh"]