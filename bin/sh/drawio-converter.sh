#!/bin/bash

# Start dbus if not already running
if [ ! -e /var/run/dbus/pid ]; then
  mkdir -p /var/run/dbus
  dbus-daemon --system --fork
fi

if [ "$1" = "-x" ] && [ "$2" = "-f" ] && [ -n "$3" ] && [ "$4" = "-o" ] && [ -n "$5" ] && [ -n "$6" ]; then
  dbus-run-session -- xvfb-run drawio --no-sandbox -x -f "$3" -o "$5" "$6" --disable-gpu
  exit $?
else
  dbus-run-session -- xvfb-run drawio --no-sandbox "$@"
fi
