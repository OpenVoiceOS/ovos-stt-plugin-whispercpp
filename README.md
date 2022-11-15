## Description

Mycroft STT plugin for [whispercpp](https://github.com/ggerganov/whisper.cpp)

High-performance inference of [OpenAI's Whisper](https://github.com/openai/whisper) automatic speech recognition (ASR) model:

- Plain C/C++ implementation without dependencies
- Apple silicon first-class citizen - optimized via Arm Neon and Accelerate framework
- AVX intrinsics support for x86 architectures
- Mixed F16 / F32 precision
- Low memory usage (Flash Attention + Flash Forward)
- Zero memory allocations at runtime
- Runs on the CPU


## Install

`pip install ovos-stt-plugin-whispercpp`

### WhisperCPP

First let's build whisper.cpp from source and move the shared library to the plugin expected default path

```bash
# build shared libwhisper.so
git clone https://github.com/ggerganov/whisper.cpp /tmp/whispercpp
cd /tmp/whispercpp
# last commit before a breaking change
git checkout d6b84b2a23220dd8b8792872a3ab6802cd24b424
gcc -O3 -std=c11   -pthread -mavx -mavx2 -mfma -mf16c -fPIC -c ggml.c
g++ -O3 -std=c++11 -pthread --shared -fPIC -static-libstdc++ whisper.cpp ggml.o -o libwhisper.so
cp libwhisper.so ~/.local/bin/libwhisper.so
```


## Configuration

You need to download and compile whispercpp from source as described in previous step

provide the path to the executable in the config if not using the default location

available models are `"tiny.en", "tiny", "base.en", "base", "small.en", "small", "medium.en", "medium", "large"`

```json
  "stt": {
    "module": "ovos-stt-plugin-whispercpp",
    "ovos-stt-plugin-whispercpp": {
        "lib": "~/.local/bin/libwhisper.so",
        "model": "tiny"
    }
  }
 
```

## Models

Models will be autodownloaded to `/home/user/.local/share/whispercpp/{model_name}` when plugin is loaded


Memory usage

| Model  | Disk   | Mem     |
| ---    | ---    | ---     |
| tiny   |  75 MB | ~280 MB |
| base   | 142 MB | ~430 MB |
| small  | 466 MB | ~1.0 GB |
| medium | 1.5 GB | ~2.6 GB |
| large  | 2.9 GB | ~4.7 GB |


## Docker

This plugin can be used together with [ovos-stt-http-server](https://github.com/OpenVoiceOS/ovos-stt-http-server) 

```bash
docker run -p 8080:8080 ghcr.io/openvoiceos/whisper-stt-http-server:master
```