FROM debian:buster-slim

RUN apt-get update && \
  apt-get install -y git python3 python3-dev python3-pip curl build-essential
RUN apt-get install -y swig portaudio19-dev libpulse-dev

RUN pip3 install ovos-stt-http-server
RUN pip3 install git+https://github.com/abdeladim-s/pywhispercpp

COPY . /tmp/ovos-stt-plugin-whispercpp
RUN pip3 install /tmp/ovos-stt-plugin-whispercpp

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-whispercpp
