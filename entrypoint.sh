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

# Start the application in the background
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

# Start nginx reverse proxy to forward CDP with Host header rewrite
cat > /tmp/nginx-cdp.conf << 'EOF'
daemon off;
worker_processes 1;
pid /tmp/nginx.pid;
error_log /tmp/nginx-error.log;
events { worker_connections 1024; }
http {
    access_log /tmp/nginx-access.log;
    client_body_temp_path /tmp/nginx-client-body;
    proxy_temp_path /tmp/nginx-proxy;
    fastcgi_temp_path /tmp/nginx-fastcgi;
    uwsgi_temp_path /tmp/nginx-uwsgi;
    scgi_temp_path /tmp/nginx-scgi;
    server {
        listen 9223;
        location / {
            proxy_pass http://127.0.0.1:9222;
            proxy_http_version 1.1;
            proxy_set_header Host localhost:9222;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
        }
    }
}
EOF
nginx -c /tmp/nginx-cdp.conf &
NGINX_PID=$!
echo "nginx reverse proxy forwarding CDP port 9222 to 9223 with Host header rewrite"

# Wait for the application process
wait $APP_PID
