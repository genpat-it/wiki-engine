FROM ubuntu:20.04

ENV TZ=Europe/Rome DEBIAN_FRONTEND=noninteractive

COPY *.zip /usr/local/share/fonts/

WORKDIR /usr/local/share/fonts/

RUN apt-get update && apt-get install build-essential python3-dev python3-pip \
python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 \
libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info pip -y \
unzip libasound2 xvfb wget plantuml && \
pip install mkdocs==1.2.4 plantuml-markdown==3.5.2 pygments==2.12.0 mkdocs-with-pdf==0.9.3 \
qrcode==7.3.1 mkdocs-drawio-exporter==0.8.0 mkdocs-izsam-search==0.1.8 mkdocs-bionformatic-izsam-theme==0.2.2 mkdocs-izsam-video==1.0.3 mkdocs-redirects==1.2.0 && \
unzip -o '*.zip' && rm *.zip && fc-cache

COPY geant-ov-rsa-ca-4.crt /usr/local/share/ca-certificates/

RUN update-ca-certificates