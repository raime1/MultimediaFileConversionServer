FROM alpine:3.10


WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

RUN pip3 --no-cache-dir install -r "./requirements.txt"

RUN apk add ffmpeg

COPY . .

EXPOSE 5050

CMD [ "python3", "-u" ,"server.py" ]
