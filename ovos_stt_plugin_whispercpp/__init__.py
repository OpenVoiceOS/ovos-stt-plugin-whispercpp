from ovos_plugin_manager.templates.stt import STT
from pywhispercpp.model import Model as WhisperEngine
from ovos_plugin_manager.utils.audio import AudioData, AudioFile
from typing import Optional


class WhispercppSTT(STT):
    MODELS = ("tiny.en", "tiny", "base.en", "base", "small.en", "small", "medium.en", "medium", "large")
    LANGUAGES = {
        "en": "english",
        "zh": "chinese",
        "de": "german",
        "es": "spanish",
        "ru": "russian",
        "ko": "korean",
        "fr": "french",
        "ja": "japanese",
        "pt": "portuguese",
        "tr": "turkish",
        "pl": "polish",
        "ca": "catalan",
        "nl": "dutch",
        "ar": "arabic",
        "sv": "swedish",
        "it": "italian",
        "id": "indonesian",
        "hi": "hindi",
        "fi": "finnish",
        "vi": "vietnamese",
        "iw": "hebrew",
        "uk": "ukrainian",
        "el": "greek",
        "ms": "malay",
        "cs": "czech",
        "ro": "romanian",
        "da": "danish",
        "hu": "hungarian",
        "ta": "tamil",
        "no": "norwegian",
        "th": "thai",
        "ur": "urdu",
        "hr": "croatian",
        "bg": "bulgarian",
        "lt": "lithuanian",
        "la": "latin",
        "mi": "maori",
        "ml": "malayalam",
        "cy": "welsh",
        "sk": "slovak",
        "te": "telugu",
        "fa": "persian",
        "lv": "latvian",
        "bn": "bengali",
        "sr": "serbian",
        "az": "azerbaijani",
        "sl": "slovenian",
        "kn": "kannada",
        "et": "estonian",
        "mk": "macedonian",
        "br": "breton",
        "eu": "basque",
        "is": "icelandic",
        "hy": "armenian",
        "ne": "nepali",
        "mn": "mongolian",
        "bs": "bosnian",
        "kk": "kazakh",
        "sq": "albanian",
        "sw": "swahili",
        "gl": "galician",
        "mr": "marathi",
        "pa": "punjabi",
        "si": "sinhala",
        "km": "khmer",
        "sn": "shona",
        "yo": "yoruba",
        "so": "somali",
        "af": "afrikaans",
        "oc": "occitan",
        "ka": "georgian",
        "be": "belarusian",
        "tg": "tajik",
        "sd": "sindhi",
        "gu": "gujarati",
        "am": "amharic",
        "yi": "yiddish",
        "lo": "lao",
        "uz": "uzbek",
        "fo": "faroese",
        "ht": "haitian creole",
        "ps": "pashto",
        "tk": "turkmen",
        "nn": "nynorsk",
        "mt": "maltese",
        "sa": "sanskrit",
        "lb": "luxembourgish",
        "my": "myanmar",
        "bo": "tibetan",
        "tl": "tagalog",
        "mg": "malagasy",
        "as": "assamese",
        "tt": "tatar",
        "haw": "hawaiian",
        "ln": "lingala",
        "ha": "hausa",
        "ba": "bashkir",
        "jw": "javanese",
        "su": "sundanese",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self.config.get("model")
        if not model:
            model = "base"
        assert model in self.MODELS  # TODO - better error handling

        self.engine = WhisperEngine(model,
                                    language="auto",
                                    print_realtime=False,
                                    print_progress=False,
                                    print_timestamps=False,
                                    single_segment=True)
        #  print(self.engine.get_params())  # TODO expose more of these above

    def execute(self, audio: AudioData, language: Optional[str]=None):
        lang = language or self.lang
        lang = lang.lower().split("-")[0]
        if lang not in self.available_languages:
            lang = "auto"  # TODO - raise error instead ?
        return self.engine.transcribe(audio.get_np_float32(), language=lang)[0].text

    @property
    def available_languages(self) -> set:
        return set(self.engine.available_languages())


WhispercppSTTConfig = {
    lang: [{"model": "tiny",
            "lang": lang,
            "meta": {
                "priority": 50,
                "display_name": f"WhisperCPP (Tiny)",
                "offline": True}
            },
           {"model": "base",
            "lang": lang,
            "meta": {
                "priority": 55,
                "display_name": f"WhisperCPP (Base)",
                "offline": True}
            },
           {"model": "small",
            "lang": lang,
            "meta": {
                "priority": 60,
                "display_name": f"WhisperCPP (Small)",
                "offline": True}
            }
           ]
    for lang, lang_name in WhispercppSTT.LANGUAGES.items()
}

if __name__ == "__main__":
    b = WhispercppSTT()

    jfk = "/home/miro/PycharmProjects/ovos-stt-plugin-vosk/jfk.wav"
    with AudioFile(jfk) as source:
        audio = source.read()

    a = b.execute(audio, language="en")
    print(a)
