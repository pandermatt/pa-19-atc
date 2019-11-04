"""
Author: Leandro Kuster and Emanuele Mazzotta
"""

import re

from text2digits.text2digits import Text2Digits

REPLACE_MAP = {
    'alfa': 'A',
    'alpha': 'A',
    'bravo': 'B',
    'charlie': 'C',
    'delta': 'D',
    'echo': 'E',
    'foxtrot': 'F',
    'fox': 'F',
    'golf': 'G',
    'hotel': 'H',
    'india': 'I',
    'juliett': 'J',
    'kilo': 'K',
    'lima': 'L',
    'mike': 'M',
    'november': 'N',
    'oscar': 'O',
    'papa': 'P',
    'quebec': 'Q',
    'romeo': 'R',
    'sierra': 'S',
    'tango': 'T',
    'uniform': 'U',
    'victor': 'V',
    'whiskey': 'W',
    'x-ray': 'X',
    'xray': 'X',
    'yankee': 'Y',
    'zulu': 'Z',
    'okay': 'ok',
    'goodbye': 'good bye',
    'freiburg': 'fribourg',
    'airfrans': 'air france',
    'st': 'saint',
    'ah': '',
    'yeah': '',
    'oh': '',
}


def clean_up_text(text):
    t2n = Text2Digits()
    text = t2n.convert(text)

    text = text.lower()

    # Remove non alphanumeric-or-space characters
    text = re.sub(r'[^\w\s]+', '', text)

    for k, v in REPLACE_MAP.items():
        text = re.sub(f'\\b{k}\\b', v, text)

    # Convert double x => x x
    text = re.sub(r'(double)(\s)(\d)', r'\3 \3', text)

    # Convert triple x => x x x
    text = re.sub(r'(triple)(\s)(\d)', r'\3 \3 \3', text)

    # Convert 6 6 0 => 660
    text = re.sub(r'(?<=\d)\s(?=\d)', '', text)

    # Add extra space for "word l" => "word  l" (l = single letter)
    text = re.sub(r'(\w{2,})(\s)(\w\W)', r'\1\2\2\3', text)
    # Convert k l m => klm
    text = re.sub(r'(?<=\w)\s(?=\w\s|\w$)', '', text)

    # Multiple spaces to one
    text = re.sub(r'\s+', ' ', text)

    # DLH 345 AB => DLH345AB
    text = re.sub(r'^([A-Z]+)(\s+)(\d+)', r'\1\3', text)
    text = re.sub(r'(?<=\d)(\s+)([A-Z]+)', r'\2', text)

    text = text.replace(' decimal ', '.')
    text = text.replace(' comma ', '.')

    return text.strip()


if __name__ == '__main__':
    print(clean_up_text('bonjour topswiss four five decimal seven eight climb to flight level three one zero'))
