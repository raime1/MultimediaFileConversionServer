FROM python:3.8-alpine


WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r "./requirements.txt"

COPY . .

EXPOSE 5050

CMD [ "python3", "server.py" ]
