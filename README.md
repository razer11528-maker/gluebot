# gluebot

A basic container that auto-restarts gluetun at a specified time, or if your speedtest is below a certain download speed , upload speed, or ping time.

![screenshot](gluebot-git-logo.png)


Define the container in your existing gluetun compose file:
```
  gluetun-restart:
    container_name: gluetun-restart
    image: ghcr.io/sboger/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y        # optional.
      - CONTROL_SERVER_PORT=8000      # optional. defaults to 8000.
      - RESTART_TIME=19:10            # optional.
      - TZ=${TZ}                      # optional. defaults to UTC.
    network_mode: "service:gluetun"
    restart: unless-stopped
```
