FROM python:3.7.4 as build

RUN apt-get update && apt-get install --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN \
    pip --no-cache-dir install --upgrade \
        pip \
        setuptools \
        wheel

COPY ["bot/requirements.txt", "setup.py", "./"]
RUN \
  pip wheel \
    --wheel-dir /wheels \
    --find-links /wheels \
    -r requirements.txt

COPY bot/ ./bot

RUN \
  pip wheel \
    --wheel-dir /wheels \
    --find-links /wheels \
    --no-index \
    .

# run stage
# ===========================
FROM python:3.7.4-slim as run
ENV DOCKER_STAGE=run PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /wheels /wheels

RUN \
  pip --no-cache-dir install \
    --find-links /wheels \
    --no-index \
    bot
RUN useradd botuser
USER botuser

COPY settings.cfg /instance/
ENV BOT_APPLICATION_SETTINGS=/instance/settings.cfg

HEALTHCHECK CMD curl --fail http://localhost:3978/test/hello || exit 1
CMD ["python", "-m", "bot.app"]
