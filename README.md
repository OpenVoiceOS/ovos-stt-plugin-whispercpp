## Description

This is an OpenVoiceOS speech-to-text (STT) plugin for [whisper.cpp](https://github.com/ggerganov/whisper.cpp), a C/C++ port of [OpenAI's Whisper](https://github.com/openai/whisper) automatic speech recognition model.

whisper.cpp runs on the CPU and has these traits:

- Plain C/C++ implementation with no dependencies
- Native support for Apple silicon, optimized with Arm Neon and the Accelerate framework
- AVX intrinsics support for x86 processors
- Mixed F16 / F32 precision
- Low memory use through Flash Attention and Flash Forward
- No memory allocation at runtime

## Install

```bash
pip install ovos-stt-plugin-whispercpp
```

## Configuration

The available models are `tiny.en`, `tiny`, `base.en`, `base`, `small.en`, `small`, `medium.en`, `medium`, and `large`.

```json
  "stt": {
    "module": "ovos-stt-plugin-whispercpp",
    "ovos-stt-plugin-whispercpp": {
        "model": "tiny"
    }
  }
```

## Models

The plugin downloads models automatically to `~/.local/share/pywhispercpp/models/{model_name}` on load.

This table shows the disk space and memory each model uses.

| Model  | Disk   | Memory  |
| ---    | ---    | ---     |
| tiny   |  75 MB | ~280 MB |
| base   | 142 MB | ~430 MB |
| small  | 466 MB | ~1.0 GB |
| medium | 1.5 GB | ~2.6 GB |
| large  | 2.9 GB | ~4.7 GB |

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager), which loads and manages OVOS plugins, including this one
- [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp), the inference engine this plugin wraps
- [openai/whisper](https://github.com/openai/whisper), the original Whisper model

## License

Apache-2.0
