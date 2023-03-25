## Description

OpenVoiceOS STT plugin for [whispercpp](https://github.com/ggerganov/whisper.cpp)

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

available models are `"tiny.en", "tiny", "base.en", "base", "small.en", "small", "medium.en", "medium", "large"`

```json
  "stt": {
    "module": "ovos-stt-plugin-whispercpp",
    "ovos-stt-plugin-whispercpp": {
        "model": "tiny"
    }
  }
 
```

## Models

Models will be autodownloaded to `~/.local/share/pywhispercpp/models/{model_name}` when plugin is loaded


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
