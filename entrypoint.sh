#!/bin/bash

if [ "$1" = "build-docx" ]; then
	echo "perl /app/entrypoint.pl "
	echo "$@"
	perl /app/entrypoint.pl "$@"
else
    exec "$@"
fi

# Ensure draw.io script is executable
if [ ! -x /usr/local/bin/drawio-converter ]; then
    chmod +x /usr/local/bin/drawio-converter
fi

