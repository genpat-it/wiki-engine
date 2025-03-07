FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DRAWIO_VERSION=26.0.9

# Set the working directory
WORKDIR /app

# Install system dependencies for WeasyPrint and Draw.io
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libjpeg-turbo8 \
    libpng-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libfontconfig1 \
    libharfbuzz-dev \
    libfribidi-dev \
    libglib2.0-0 \
    libmagic1 \
    openjdk-17-jre-headless \
    plantuml \
    wget \
    unzip \
    xvfb \
    dbus \
    dbus-x11 \
    libgtk-3-0 \
    libxtst6 \
    libnss3 \
    libasound2t64 \
    libxss1 \
    libgbm1 \
    ca-certificates \
    libnotify4 \
    xdg-utils \
    libsecret-1-0 \
    graphviz \
    && apt-get clean

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && apt-get clean

# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment and install dependencies
RUN /venv/bin/pip install --no-cache-dir mkdocs==1.2.4 \
    mkdocs-izsam-search==0.1.8 \
    mkdocs-bionformatic-izsam-theme==1.0.6 \
    mkdocs-izsam-video==1.0.3 \
    mkdocs-redirects==1.2.0 \
    mkdocs-izsam-mermaid-to-images==1.0.8 \
    mkdocs-macros-plugin==1.3.7 \
    plantuml-markdown==3.5.2 \
    pymdown-extensions==10.9 \
    pygments==2.12.0 \
    mkdocs-with-pdf==0.9.3 \
    qrcode==7.3.1 \
    weasyprint==62.3

# Ensure the virtual environment is activated when running commands
ENV PATH="/venv/bin:$PATH"

# Copy the bin folder (including sh directory) into the Docker image
COPY . /app

# Install custom plugins
RUN /venv/bin/pip install -e /app/plugins/custom

# Set the working directory back to /app
WORKDIR /app

# Detect architecture and install the correct version of Pandoc
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    wget https://github.com/jgm/pandoc/releases/download/2.5/pandoc-2.5-linux.tar.gz && \
    tar xvfz pandoc-2.5-linux.tar.gz && \
    mv pandoc-2.5/bin/pandoc /usr/local/bin/ && \
    mv pandoc-2.5/bin/pandoc-citeproc /usr/local/bin/ && \
    rm -rf pandoc-2.5 pandoc-2.5-linux.tar.gz

# Install draw.io
RUN wget -q https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb && \
    dpkg -i drawio-amd64-${DRAWIO_VERSION}.deb || apt-get -f install -y && \
    rm -f drawio-amd64-${DRAWIO_VERSION}.deb

# Copy draw.io conversion script
COPY bin/sh/drawio-converter.sh /usr/local/bin/drawio-converter
# Ensure it is executable
RUN chmod +x /usr/local/bin/drawio-converter

# Ensure the entrypoint.sh file has the correct permissions to be executed
RUN chmod +x /app/entrypoint.sh

# Create the fonts and cache directories
RUN echo '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir recursive="yes">/wiki/fonts</dir><cachedir>/wiki/cache</cachedir></fontconfig>' > /etc/fonts/fonts.conf

# Set execute permissions only for .sh and .pl files
RUN find /app/bin -type f \( -name "*.sh" \) -exec chmod +x {} \;

# Expose the application port
EXPOSE 8000

# Set the entrypoint to the shell script
ENTRYPOINT ["/app/entrypoint.sh"]