FROM ubuntu
RUN apt-get update && \
  apt-get install -y git python3 python3-dev python3-pip curl build-essential
RUN apt-get install -y swig portaudio19-dev libpulse-dev

RUN apt-get install -y \
    git \
    build-essential \
    cmake \
    ninja-build

RUN pip3 install ovos-stt-http-server
RUN pip3 install git+https://github.com/abdeladim-s/pywhispercpp.git

COPY . /tmp/ovos-stt-plugin-whispercpp
RUN pip3 install /tmp/ovos-stt-plugin-whispercpp
RUN pip3 install flask git+https://github.com/MycroftAI/mycroft-messagebus-client.git

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-whispercpp
