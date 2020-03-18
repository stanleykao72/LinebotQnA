ARG ARCH
FROM stanleykao72/linebot-multiarch:Django-${ARCH}

# HACK: don't fail when no qemu binary provided
COPY .gitignore qemu-${ARCH}-static* /usr/bin/

# ENV MPLLOCALFREETYPE=1
# RUN apk --update add --no-cache \
#    make \
#    libpng-dev \ 
#    freetype>=2.3

# Stage 2
# Create project directory (workdir)
# RUN mkdir /app
WORKDIR /app

# Add requirements.txt to WORKDIR and install dependencies
#COPY requirements_datascience.txt .
#RUN pip install -r requirements_datascience.txt
RUN pip install numpy

# Cleanup
# RUN apk del --purge libpng-dev freetype
# RUN rm -vrf /var/cache/apk/*

# Add the remaining source code files to WORKDIR
COPY . .

ENTRYPOINT ["python"]

# The script to start on startup
# YOU PROBABLY NEED TO EDIT THE FOLLOWING LINE
# CMD ["manage.py","runserver"]
