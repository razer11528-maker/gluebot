# gluebot

A basic container that auto-restarts gluetun at a specified time or if your speedtest is below a certain download speed, upload speed, or ping time.

![screenshot](gluebot-git-logo.png)

This is a personal container I built for my own use. I was encouraged to make it public. It comes with no support or planned future releases unless I get bored.

## Installation

### See below for compose examples

```
docker pull ghcr.io/razer11528-maker/gluebot:latest
```

### Or build it yourself after reviewing the code

```bash
git clone https://github.com/razer11528-maker/gluebot.git
cd gluebot
docker build -t gluebot .
```
```
gluebot:
   container_name: gluebot
   image: gluebot
```

## Three modes of operation:

* Timed daily restart of gluetun via setting a 24hr time env variable, like 19:10 for 7:10pm.
* Restart based on speedtest-tracker container (lscr.io/linuxserver/speedtest-tracker) results. Gluebot listens on port 4040. *ANY* post to this port will trigger a restart.
* Both timed daily restart and speedtest-tracker results.

## Requirements:

* Timed restart: An existing gluetun docker compose file. As of the current gluetun release, the API is open and doesn't require authentication. Future gluetun releases will require the config.toml file to be defined. Gluebot supports both.
* Speedtest restart: Requires a functioning lscr.io/linuxserver/speedtest-tracker container inside your gluetun network. And the gluebot webhook url and thresholds defined in speedtest-tracker.

## Config Examples

### Environment options:

```
API_KEY=                # optional, but required for secured gluetun API.
CONTROL_SERVER_PORT=    # optional. defaults to 8000.
RESTART_TIME=           # optional, but required for timed restarts.
TZ=                     # optional. defaults to UTC.
```

### Basic timed restart without API auth:
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - RESTART_TIME=19:10
      - TZ=Europe/London
    network_mode: "service:gluetun"
    restart: unless-stopped
```


### Timed restart with API auth, and gluetun api on port 9090:
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y
      - RESTART_TIME=19:10
      - TZ=Europe/London
      - CONTROL_SERVER_PORT=9090
    network_mode: "service:gluetun"
    restart: unless-stopped
```


### Timed and speedtest restart with API auth (webhook and threshholds must be defined in speedtest container):
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y
      - RESTART_TIME=19:10
      - TZ=Europe/London
    network_mode: "service:gluetun"
    restart: unless-stopped
```

### Only speedtest restart with API auth (webhook and threshholds must be defined in speedtest container):
```
  gluebot:
    container_name: gluebot
    image: ghcr.io/razer11528-maker/gluebot:latest
    environment:
      - API_KEY=SUperS3cretK3y
      - TZ=Europe/London
    network_mode: "service:gluetun"
    restart: unless-stopped
```

### Speedtest-tracker settings

![screenshot](speedtest-tracker-webhook.png)
![screenshot](speedtest-tracker-thresholds.png)

### Example config.toml file in [GLUTEN_CONFIG_DIR]/auth/config.toml:

```
[[roles]]
name = "homepage"
routes = ["GET /v1/publicip/ip"]
auth = "apikey"
apikey = "H0meP4geK3y"

[[roles]]
name = "gluebot"
routes = ["PUT /v1/openvpn/status"]
auth = "apikey"
apikey = "SUperS3cretK3y"
```

> [!CAUTION]
> This container was never designed to be secure. It always listens on 4040 (inside the gluetun network)
> and will perform a gluetun restart on _ANY_ post to it. This container stores gluetun's api key in env,
> this container completely destroys gluetun's hard work at using api keys for security by leaving port 4040
> wide open. This container will not be kept current.
>
> If you read this far, here's a bonus. An http get to port 4040 will display the logs. You might find it useful
> in an iframe on dashboards or if you prefer browsers. Add port 4040:4040 to gluetuns service config and access it
> on your lan. Which is amazingly insecure, as anyone on the lan that posts to port 4040 will restart gluetun.

