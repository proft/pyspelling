#!/usr/bin/env python

"""
pyspelling

Spellchecking for Ukrainian, Russian and English languages.
Used: Python 3, Yandex spellservice.

by proft @ http://proft.me
"""

import os
import requests
from subprocess import Popen, PIPE

ROOT = os.path.abspath(os.path.dirname(__file__))
ICON_OK = os.path.join(ROOT, 'ok.png')
ICON_ERROR = os.path.join(ROOT, 'error.png')
LANG_TRANS = {'ua': 'uk', 'us': 'en', 'ru': 'ru'}


def get_layout():
    """ Get current keyboard layout """

    pipe = Popen("setxkbmap -print | grep xkb_symbols | awk -F'+' '{print $2}'", stdout=PIPE, shell=True)
    layout = pipe.communicate()[0].strip().decode("utf-8")
    return str(layout)


def set_clipboard(text):
    """ Set system clipboard to text """

    xsel_proc = Popen(['xsel', '-bi'], stdin=PIPE)
    xsel_proc.communicate(bytes(text, 'utf-8'))


def get_clipboard():
    """ Get text from system clipboard """

    return os.popen('xsel').read()

if __name__ == '__main__':
    word = get_clipboard()
    params = {'text': get_clipboard(), 'lang': LANG_TRANS[get_layout()]}
    r = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params=params)

    if r.status_code == 200:
        if len(r.json()) > 0:
            out = r.json()[0]
            variants = [v for v in out['s']]
            set_clipboard(variants[0])
            os.system('notify-send -i %(icon)s "%(caption)s" "%(text)s"' % {
                'icon': ICON_ERROR,
                'caption': word,
                'text': '\n'.join(variants)
            })
        else:
            os.system('notify-send -i %(icon)s "%(text)s"' % {
                'icon': ICON_OK,
                'text': word
            })
