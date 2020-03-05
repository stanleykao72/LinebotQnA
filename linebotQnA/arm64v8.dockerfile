FROM alpine AS builder

# Download QEMU, see https://github.com/docker/hub-feedback/issues/1261
ENV QEMU_URL https://github.com/balena-io/qemu/releases/download/v3.0.0%2Bresin/qemu-3.0.0+resin-arm.tar.gz
RUN apk add curl && curl -L ${QEMU_URL} | tar zxvf - -C . --strip-components 1


FROM arm64v8/python:3.7.6

# add QEMU
COPY --from=builder qemu-aarch64-static /usr/bin

# Create project directory (workdir)
RUN mkdir /app
WORKDIR /app

# Add requirements.txt to WORKDIR and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add the remaining source code files to WORKDIR
COPY . .

ENTRYPOINT ["python"]

# The script to start on startup
# YOU PROBABLY NEED TO EDIT THE FOLLOWING LINE
CMD ["manage.py","runserver"]
