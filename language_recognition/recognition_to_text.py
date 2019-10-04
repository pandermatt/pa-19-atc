"""
Based on code take from Bachelors Thesis by Leandro Kuster and Emanuele Mazzotta

Original authors: Leandro Kuster and Emanuele Mazzotta
Modified by: Pascal Andermatt and Jennifer Schürch
"""

import json

import requests

from config import config
from util.logger import log


def analyse_text(text):
    data = _send_request(text)

    intent = data.get('topScoringIntent', {}).get('intent')
    entities = {entity.get('type'): entity.get('entity') for entity in data.get('entities', [])}

    return {'text': text, 'intent': intent, 'entities': entities}


def _send_request(text):
    try:
        response = requests.get(
            url="https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/" + config.microsoft_luis_app_key(),
            params={
                "staging": "true",
                "verbose": "true",
                "timezoneOffset": "-420",
                "subscription-key": config.microsoft_luis_subscription_key(),
                "q": text,
            },
        )

        log.debug(f'Response HTTP Status Code: {response.status_code}')
        log.debug(f'Response HTTP Response Body: {response.content}')

        if response.status_code != 200:
            log.warning(f'HTTP Request NOK ({response.status_code}), Body: {response.content}')

        return json.loads(response.content)
    except requests.exceptions.RequestException:
        log.warning('HTTP Request failed')


if __name__ == '__main__':
    print(analyse_text('bonjour topswiss 4578 climb to flight level 310'))
