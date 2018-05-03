#!/usr/bin/env python3
#coding: utf-8

# all UD 1.4 langs

short2long = {
    "ar": "ara",
    "bg": "bul",
    "ca": "cat",
    "cop": "cop",  # no W2C, no Opus
    "cs": "ces",
    "cu": "chu",  # no W2C, no Opus
    "da": "dan",
    "de": "deu",
    "el": "ell",
    "en": "eng",
    "es": "spa",
    "et": "est",
    "eu": "eus",
    "fa": "fas",
    "fi": "fin",
    "fr": "fra",
    "ga": "gle",  # in Opus: leccos ale ne OpenSubtitles
    "gl": "glg",
    "got": "got",  # no W2C, no Opus
    "grc": "grc",  # no W2C, in Opus: Ubuntu
    "he": "heb",
    "hi": "hin",
    "hr": "hrv",
    "hu": "hun",
    "id": "ind",
    "it": "ita",
    "ja": "jpn",  # no Delta
    "kk": "kaz",
    "la": "lat",  # in Opus: Ubuntu Gnome Tatoeba
    "lv": "lav",
    "nl": "nld",
    "no": "nor",
    "pl": "pol",
    "pt": "por",
    "ro": "ron",
    "ru": "rus",
    "sa": "san",  # no W2C, in Opus: Ubuntu
    "sk": "slk",
    "sl": "slv",
    "sv": "swe",
    "swl": "swl",  # no W2C, no Opus
    "ta": "tam",
    "tr": "tur",
    "ug": "uig",  # no W2C, in Opus: Ubuntu Gnome Tanzil
    "uk": "ukr",
    "vi": "vie",
    "zh": "zho",  # no Delta
}

long2short = dict()

for s, l in short2long.items():
    long2short[l] = s

import sys
iso_in = sys.argv[1]
if len(iso_in) == 3:
    print(long2short[iso_in])
else:
    print(short2long[iso_in])


