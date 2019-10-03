"""
Based on code take from Bachelors Thesis by Leandro Kuster and Emanuele Mazzotta

Original authors: Leandro Kuster and Emanuele Mazzotta
Modified by: Pascal Andermatt and Jennifer Schürch
"""

import json

import requests

from config import config
from util.logger import log

REGION = 'westus'


def analyse_text(text):
    api_url = 'https://{0}.api.cognitive.microsoft.com/luis/v2.0/apps/{1}' \
              '?staging=true&verbose=true&timezoneOffset=-420' \
              '&subscription-key={2}' \
              '&q={3}'.format(REGION,
                              config.microsoft_luis_app_key(),
                              config.microsoft_luis_subscription_key(),
                              text)

    response = requests.get(api_url)
    if not response.ok:
        log.warning(f'Response code {response.status_code} for text {text}')
        return

    data = json.loads(response.content)
    intent = data.get('topScoringIntent', {}).get('intent')
    entities = {
        entity.get('type'): entity.get('entity')
        for entity
        in data.get('entities', [])
    }

    return {'text': text, 'intent': intent, 'entities': entities}


if __name__ == '__main__':
    print(analyse_text('bonjour topswiss 4578 climb to flight level 310'))
