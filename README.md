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

First let's install whisper.cpp from source and move the binary to the plugin expected default path

```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make
cp main ~/.local/bin/whispercpp
```

Models will be autodownloaded to `/home/user/.local/share/whispercpp/{model_name}` when plugin is loaded

## Configuration

You need to download and compile whispercpp from source as described in previous step

provide the path to the executable in the config if not using the default location

available models are `"tiny.en", "tiny", "base.en", "base", "small.en", "small", "medium.en", "medium", "large"`

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