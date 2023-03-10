FROM python:3.9.0-slim-buster

ENV TINI_VERSION=0.19.0 \
    TINI_SHA256=93dcc18adc78c65a028a84799ecf8ad40c936fdfc5f2a57b1acda5a8117fa82c

RUN set -x \
    && buildDeps=" \
    wget \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    # grab tini for signal processing and zombie killing
    && wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/v$TINI_VERSION/tini-amd64" \
    && echo "$TINI_SHA256 /usr/local/bin/tini" | sha256sum --check --status \
    && chmod +x /usr/local/bin/tini \ 
    && apt-get purge -y --auto-remove $buildDeps

COPY / /sentry-rate-limit
COPY /ratelimit/config.example.py /sentry-rate-limit/ratelimit/config.py

WORKDIR /sentry-rate-limit

RUN set -x \
    && python setup.py install

ENTRYPOINT ["tini", "--", "sentry-rate-limit"]