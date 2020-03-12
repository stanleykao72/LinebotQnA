ARG BASE_IMAGE_PREFIX
FROM ${BASE_IMAGE_PREFIX}python:3.7.7-alpine3.10

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

# Install dependencies
RUN apk --update add --no-cache \
        wget \ 
        gcc \
        g++ \
        libgfortran
RUN apk --update add --no-cache \
        build-base libstdc++ \
        libpng libpng-dev \
        freetype freetype-dev

# Install data science
RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk update
RUN apk add py3-numpy@community py3-scipy@community py3-matplotlib@community
# Install pandas
RUN wget --quiet --output-document=/etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN apk add --no-cache --repository=https://apkproxy.herokuapp.com/sgerrand/alpine-pkg-py-pandas py-pandas

# install postgress client
RUN apk add --no-cache postgresql-client postgresql-dev

# Create project directory (workdir)
RUN mkdir /app
WORKDIR /app

# Add requirements.txt to WORKDIR and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Cleanup
RUN apk del --purge build-base libgfortran libpng-dev freetype-dev python3-dev && \
RUN rm -vrf /var/cache/apk/*

# Add the remaining source code files to WORKDIR
COPY . .

ENTRYPOINT ["python"]

# The script to start on startup
# YOU PROBABLY NEED TO EDIT THE FOLLOWING LINE
CMD ["manage.py","runserver"]
