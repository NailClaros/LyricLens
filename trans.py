import requests
import json
import os
import html


nkey = os.getenv('key_n')
hkey = os.getenv('key_h')

def detect(text):
    url = "https://google-translate-api8.p.rapidapi.com/google-translate/detect/"

    querystring = {"text":f"{text}"}

    payload = {
        "key1": "value",
        "key2": "value"
    }
    headers = {
        "x-rapidapi-key": str(hkey),
        "x-rapidapi-host": "google-translate-api8.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.json())
    ax = json.loads(response.text)
    if ax['result'] != None:
        code = ax['result']['code']
        language = ax['result']['language']
        return code, language

    return "MUL", "Made up Language/gibberish"


def translate(text: str, lang: str, og_lang:str) -> str:
    CHUNK_SIZE = 1000
    translated_parts = []

    code = ""
    for k, v in languages_dict.items():
        if og_lang.lower() == v.lower():
            code = k

    for start in range(0, len(text), CHUNK_SIZE):
        chunk = text[start : start + CHUNK_SIZE]
        try:
            url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
            payload = {
                "q": str(chunk),
                "source": code,
                "target": str(lang),
                "format": "text"
            }
            headers = {
                "x-rapidapi-key": nkey,
                "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            data = json.loads(response.text)
            # Safe extraction with fallbacks
            translated_text = data['data']['translations']['translatedText'][0]

            if translated_text is None:
                # Try alternative path if API changed or unexpected
                # Dump entire response for debugging (could log instead)
                print("Unexpected translation response shape:", data)
                translated_text = chunk  # fallback to original
            translated_text = html.unescape(translated_text)
            translated_parts.append(str(translated_text))

        except requests.RequestException as e:
            print(f"[Warning] Translation API error for chunk starting at {start}: {e}")
            translated_parts.append(chunk)  # fallback to original chunk

    return "".join(translated_parts)
###Title
###Coverart
###natural lang
###html translation -- time to kill

languages_dict = {
    "en": "English",
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "as": "Assamese",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "yue": "Cantonese",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "chr": "Cherokee",
    "ny": "Chichewa",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "dz": "Dzongkha",
    "eo": "Esperanto",
    "et": "Estonian",
    "fil": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gn": "Guarani",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ckb": "Kurdish (Sorani)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia (Oriya)",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "rm": "Romansh",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "ser": "Serrano",
    "st": "Sesotho",
    "sn": "Shona",
    "scn": "Sicilian",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ber": "Tamazight",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "bo": "Tibetan",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "wo": "Wolof",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}