# gluebot

A basic container that auto-restarts gluetun at a specified time or if your speedtest is below a certain download speed, upload speed, or ping time.

![screenshot](gluebot-git-logo.png)

This is a personal container I built for my own use. I was encouraged to make it public. It comes with no support or planned future releases.

There are three modes this container can operate in.

* Timed daily restart of gluetun.
* Restart based on speedtest-tracker container (lscr.io/linuxserver/speedtest-tracker) results.
* Both timed daily restart and speedtest-tracker results.

Requirements:

* Timed restart: An existing gluetun docker compose file. As of the current gluetun release, the API is open and doesn't require authentication. Future gluetun releases will require the config.toml file to be defined. Gluebot supports both.
* Speedtest restart: Requires a functioning lscr.io/linuxserver/speedtest-tracker container inside your gluetun network. And the gluebot webhook url and thresholds defined in speedtest-tracker.

Basic timed restart without API auth:
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - RESTART_TIME=19:10            # optional, but required for timed restarts.
      - TZ=Europe/London              # optional. defaults to UTC.
    network_mode: "service:gluetun"
    restart: unless-stopped
```


Timed restart with API auth:
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y        # optional, but required for secured gluetun API.
      - RESTART_TIME=19:10            # optional, but required for timed restarts.
      - TZ=Europe/London              # optional. defaults to UTC.
    network_mode: "service:gluetun"
    restart: unless-stopped
```


Timed restart with API auth and speedtest (webhook and threshholds must be defined in speedtest container):
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y        # optional, but required for secured gluetun API.
      - CONTROL_SERVER_PORT=8000      # optional. defaults to 8000.
      - RESTART_TIME=19:10            # optional, but required for timed restarts.
      - TZ=${TZ}                      # optional. defaults to UTC.
    network_mode: "service:gluetun"
    restart: unless-stopped
```
