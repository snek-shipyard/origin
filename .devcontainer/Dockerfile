# [Choice] Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED 1

# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then groupmod --gid $USER_GID vscode && usermod --uid $USER_UID --gid $USER_GID vscode; fi

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.

# Add pre-installation requirements:
ADD requirements/ /requirements/

# Update, install and cleaning:
RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        libexpat1-dev \
        libjpeg62-turbo-dev \
        libpcre3-dev \
        libpq-dev \
        zlib1g-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && python -m venv /venv \
    && chown -R 1000:1000 /venv \
    && /venv/bin/pip install -U pip \
    && /venv/bin/pip install --no-cache-dir -r /requirements/production.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS

RUN set -ex \
    && RUN_DEPS=" \
        libexpat1 \
        libjpeg62-turbo \
        libpcre3 \
        libpq5 \
        mime-support \
        procps \
        zlib1g \
        tini \
    " \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends $RUN_DEPS

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_DEBUG=on \
    DJANGO_SETTINGS_MODULE=esite.settings.development

# The ASGI configuration (customize as needed):
ENV ASGI_VIRTUALENV=/venv \
	ASGI_CONFIG=bifrost.asgi:application \
    ASGI_HOST=0.0.0.0 \
	ASGI_PORT=8000 \
    ASGI_VERBOSITY=1 \
    ASGI_ACCESS_LOG=-

# The uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv \
	UWSGI_WSGI_FILE=esite/wsgi_production.py \
	UWSGI_HTTP=:8000 \
	UWSGI_MASTER=1 \
	UWSGI_WORKERS=2 \
	UWSGI_THREADS=1

# Place init, make it executable and
# make sure venv files can be used by uWSGI process:
ADD .devcontainer/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Call collectstatic with dummy environment variables:
# DATABASE_URL=postgres://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput

# I personally like to start my containers with tini
# which start uWSGI, using a wrapper script to allow us to easily add
# more commands to container startup:
ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
