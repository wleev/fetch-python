from alpine:3.17

RUN apk update && apk add python3 py3-pip

WORKDIR /usr/local/src

COPY fetch.py .
COPY requirements.txt .
COPY fetch-py /usr/local/bin
RUN chmod +x /usr/local/bin/fetch-py

RUN pip3 install -r requirements.txt
WORKDIR /
