FROM python:3.8-alpine

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache libxslt openblas libstdc++ dos2unix mariadb-connector-c-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc g++ linux-headers libc-dev libxml2-dev libxslt-dev libffi-dev python3-dev \
    libxml2 libxslt-dev libjpeg-turbo-dev zlib-dev \
    gfortran build-base freetype-dev libpng-dev openblas-dev \
    && pip install --upgrade pip \
    && apk del .tmp-build-deps 

RUN pip install -r requirements.txt 
RUN apk update && apk add bash

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./scripts /scripts

RUN chmod +x /scripts/* && dos2unix /scripts/* 

# CMD [ "script.sh" ]
CMD ["/scripts/script.sh"]

