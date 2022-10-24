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

## Configuration

You need to download and compile whispercpp from source, provide the path to the executable in the config

follow instructions here https://github.com/ggerganov/whisper.cpp

```json
  "stt": {
    "module": "ovos-stt-plugin-whispercpp",
    "ovos-stt-plugin-whispercpp": {
        "bin": "/home/user/.local/bin/whispercpp",
        "model": "tiny"
    }
  }
 
```

## Docker

This plugin can be used together with [ovos-stt-http-server](https://github.com/OpenVoiceOS/ovos-stt-http-server) 

```bash
docker run -p 8080:8080 ghcr.io/openvoiceos/whisper-stt-http-server:master
```