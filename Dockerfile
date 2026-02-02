FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox \
    libgtk-3-0 libwebkit2gtk-4.1-0 \
    libx11-6 libx11-xcb1 libxcb1 \
    libxrandr2 libxinerama1 libxcomposite1 libxcursor1 libxi6 \
    libxdamage1 libxext6 libxfixes3 libxkbcommon0 \
    libglib2.0-0 libgdk-pixbuf-2.0-0 libpango-1.0-0 libatk1.0-0 libcairo2 \
    libayatana-appindicator3-1 \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-arphic-uming \
    fonts-arphic-ukai \
    fonts-roboto \
    fonts-dejavu \
    fonts-liberation \
    fonts-ubuntu \
    fonts-cantarell \
    curl wget xauth util-linux \
    libnotify-bin xdg-utils \
    dbus-x11 at-spi2-core \
    libnss3 libgbm1 libasound2t64 libdrm2 \
    libatk-bridge2.0-0 libatspi2.0-0 \
    libc6 libcups2 libcurl4 libdbus-1-3 libexpat1 libnspr4 \
    libgtk-4-1 libu2f-udev libvulkan1 \
    unzip openssh-client openjdk-21-jre-headless \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*
 
#RUN curl -L -f -o /tmp/mlxdeb.deb "https://mlxdists.s3.eu-west-3.amazonaws.com/mlx/latest/multiloginx-amd64.deb"
COPY ./desktop-multiloginx-ubuntu-24.04-amd64.deb /tmp/mlxdeb.deb
# Create non-root user
RUN useradd -m -s /bin/bash appuser && \
    mkdir -p /home/appuser/.config && \
    chown -R appuser:appuser /home/appuser
WORKDIR /home/appuser
RUN dpkg-deb -x /tmp/mlxdeb.deb mlx  && dpkg-deb --control /tmp/mlxdeb.deb  &&  dpkg -i /tmp/mlxdeb.deb && rm /tmp/mlxdeb.deb



# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /home/appuser/
# COPY ./your-wails-app /app/your-wails-app
# RUN chmod +x /app/your-wails-app

ENV DISPLAY=:99
EXPOSE 5900

ENTRYPOINT ["/entrypoint.sh"]
USER appuser
CMD ["mlxapp"]
