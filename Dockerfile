# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libjpeg62-turbo \
    libpng-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libfontconfig1 \
    libharfbuzz-dev \
    libfribidi-dev \
    libglib2.0-0 \
    libmagic1 \
    wget \
    && apt-get clean

# pandoc 2.5
RUN wget https://github.com/jgm/pandoc/releases/download/2.5/pandoc-2.5-1-amd64.deb && \
    dpkg -i pandoc-2.5-1-amd64.deb && \
    rm pandoc-2.5-1-amd64.deb

# Install MkDocs and the specified plugins and extensions
RUN pip install --no-cache-dir mkdocs==1.2.4 \
    mkdocs-izsam-search==0.1.8 \
    mkdocs-bionformatic-izsam-theme==0.2.8 \
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

# Copy the bin folder (including sh directory) into the Docker image
COPY . /app

RUN chmod +x /app/entrypoint.sh

# Create the fonts and cache directories
RUN echo '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir recursive="yes">/wiki/fonts</dir><cachedir>/wiki/cache</cachedir></fontconfig>' > /etc/fonts/fonts.conf

# Set execute permissions only for .sh and .pl files
RUN find /app/bin -type f \( -name "*.sh" \) -exec chmod +x {} \;

# Set the entrypoint to the shell script
ENTRYPOINT ["/app/entrypoint.sh"]