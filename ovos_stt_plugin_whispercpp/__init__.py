# this is needed to read the WAV file properly
import numpy
from ovos_plugin_manager.templates.stt import STT
from pywhispercpp.model import Model as WhisperEngine
from speech_recognition import AudioData


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
                                    log_level=self.config.get("log_level", "WARNING"),
                                    language="auto",
                                    print_realtime=False,
                                    print_progress=False,
                                    print_timestamps=False,
                                    single_segment=True)
        #  print(self.engine.get_params())  # TODO expose more of these above

    def audiodata2array(self, audio_data):
        assert isinstance(audio_data, AudioData)
        # Convert buffer to float32 using NumPy
        audio_as_np_int16 = numpy.frombuffer(audio_data.get_wav_data(), dtype=numpy.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

        # Normalise float32 array so that values are between -1.0 and +1.0
        max_int16 = 2 ** 15
        data = audio_as_np_float32 / max_int16
        return data

    def execute(self, audio, language=None):
        lang = language or self.lang
        lang = lang.lower().split("-")[0]
        if lang not in self.available_languages:
            lang = "auto"  # TODO - raise error instead ?
        return self.engine.transcribe(self.audiodata2array(audio), language=lang)[0].text

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
    from speech_recognition import Recognizer, AudioFile

    jfk = "/home/user/whisper.cpp/samples/jfk.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    a = b.execute(audio, language="en")
    print(a)
