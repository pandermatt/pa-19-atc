"""
Author: Pascal Andermatt and Jennifer Schürch
"""

import json

import requests

from config import config
from util.logger import log


def speech_to_text(audio_file_path):
    data = _send_request(audio_file_path)

    if data.get('RecognitionStatus') != 'Success':
        log.warning(f'{audio_file_path} has an empty transcript')
        return

    transcript = data.get('NBest')[0].get('Display')
    log.info("Transcript: %s" % transcript)
    return transcript


def _send_request(audio_file_path):
    try:
        response = requests.post(
            url="https://westeurope.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1",
            params={
                "format": "detailed",
                "cid": config.microsoft_speech_endpoint_id(),
            },
            headers={
                "Ocp-Apim-Subscription-Key": config.microsoft_speech_subscription_key(),
                "Content-Type": "audio/wav; codecs=audio/pcm;",
            },
            data=open(audio_file_path, 'rb'),
        )

        log.debug(f'Response HTTP Status Code: {response.status_code}')
        log.debug(f'Response HTTP Response Body: {response.content}')

        if response.status_code != 200:
            log.warning(f'HTTP Request NOK ({response.status_code}), Body: {response.content}')

        return json.loads(response.content)
    except requests.exceptions.RequestException:
        log.warning('HTTP Request failed')
