FROM python:3-alpine

ENV API_KEY=
ENV CONTROL_SERVER_PORT=8000
ENV RESTART_TIME=
ENV TZ=Etc/UTC

RUN apk add --no-cache tzdata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 4040

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./gluebot.py" ]

