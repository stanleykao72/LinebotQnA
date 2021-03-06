
# ARG BASE_IMAGE_PREFIX
# FROM ${BASE_IMAGE_PREFIX}python:3.7.7-slim-buster
ARG BASE_IMAGE_PREFIX
FROM ${BASE_IMAGE_PREFIX}python:3.8.2-alpine3.11

# see hooks/post_checkout
ARG ARCH

# HACK: don't fail when no qemu binary provided
COPY .gitignore qemu-${ARCH}-static* /usr/bin/


# ================
# FROM alpine AS builder

# Download QEMU, see https://github.com/docker/hub-feedback/issues/1261
# ENV QEMU_URL https://github.com/balena-io/qemu/releases/download/v3.0.0%2Bresin/qemu-3.0.0+resin-aarch64.tar.gz
# RUN apk add curl && curl -L ${QEMU_URL} | tar zxvf - -C . --strip-components 1


# FROM arm64v8/python:3.7.6

# add QEMU
# COPY --from=builder qemu-aarch64-static /usr/bin
# ================

# APK Install dependencies
RUN apk --update add --no-cache \
        wget \ 
        gcc \
        g++ \
        make \
        libgfortran \
        libxml2-dev  \
        libxslt-dev \
        libxml2
RUN apk --update add --no-cache \
        build-base\
        libstdc++ \
        libpng \
        libpng-dev \
        freetype \
        freetype-dev

# Install data science
RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update
RUN apk add py3-numpy@community py3-scipy@community py3-matplotlib@community
RUN apk add py3-pandas@testing

# set python path
ENV PYTHONPATH=/usr/local/lib/python3.8/site-packages:/usr/lib/python3.7/site-packages:/usr/lib/python3.8/site-packages

# install postgress client
RUN apk add --no-cache postgresql-client postgresql-dev

# APT install dependencies
# RUN apt-get -qq update \
#    && apt-get install -yqq --no-install-recommends \
#       curl \
#    && apt-get install -yqq --no-install-recommends \
#       gnupg2 \
#       libpq-dev \
#       libxml2-dev \
#       libxslt-dev \
#       liblz-dev \
#       liblmdb-dev \ 
#       liblmdb++-dev \
#       python3-dev \
#       python3-lxml \
#       build-essential \
#    && echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >> /etc/apt/sources.list.d/postgresql.list \
#    && curl -SL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
#    && apt-get update \
#    && apt-get install -yqq --no-install-recommends postgresql-client \
#    && rm -rf /var/lib/apt/lists/* \
#    && rm -rf /usr/share/doc && rm -rf /usr/share/man \
#    && apt-get autopurge -yqq \
#    && apt-get clean \
#    && sync
    

RUN pip install lxml

# Stage 1
# Create project directory (workdir)
# RUN mkdir /app
# WORKDIR /app

# Add requirements.txt to WORKDIR and install dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Cleanup
RUN apk del --purge build-base libpng-dev freetype-dev
RUN rm -vrf /var/cache/apk/*

# Add the remaining source code files to WORKDIR
# COPY . .

ENTRYPOINT ["/bin/sh"]

# The script to start on startup
# YOU PROBABLY NEED TO EDIT THE FOLLOWING LINE
# CMD ["manage.py","runserver"]
