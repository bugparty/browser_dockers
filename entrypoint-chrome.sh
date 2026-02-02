#!/bin/bash
set -e

# Remove stale X11 locks
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99

# Create Xauthority file if it doesn't exist
touch /home/appuser/.Xauthority
export XAUTHORITY=/home/appuser/.Xauthority

# Start Xvfb in the background
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!

# Wait for Xvfb to start
sleep 2

# Start fluxbox in the background
DISPLAY=:99 fluxbox &
FLUXBOX_PID=$!

# Start x11vnc in the background
DISPLAY=:99 x11vnc -display :99 -forever -nopw -listen 0.0.0.0 -rfbport 5900 &
X11VNC_PID=$!

# Wait a bit for the display to be fully ready
sleep 1

# Export DISPLAY for the application
export DISPLAY=:99

# Start Chrome and wait for it to bind to port 9222
"$@" &
APP_PID=$!

# Wait for Chrome's debugging port to be available
echo "Waiting for Chrome to start debugging interface..."
for i in {1..30}; do
  if curl -s http://127.0.0.1:9222/json/version > /dev/null 2>&1; then
    echo "Chrome debugging interface is ready"
    break
  fi
  sleep 1
done

# Use socat to forward port 9222 to 0.0.0.0
socat TCP-LISTEN:9223,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:9222 &
SOCAT_PID=$!

echo "Port forwarding: 0.0.0.0:9223 -> 127.0.0.1:9222"

# Wait for the application process
wait $APP_PID
