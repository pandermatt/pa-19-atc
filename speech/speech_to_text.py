"""
Author: Pascal Andermatt and Jennifer Schürch
"""

import json

import requests
import time

from config import config
from util.logger import log


def speech_to_text(audio_file_path):
    data = None
    cnt = 0
    # if data is None HTTP Request failed,
    # The cause is probably because there is a limit of how many Request can be sent,
    # but since it looks random we'll just try again when it happens...
    while data is None and cnt < 5:
        data = _send_request(audio_file_path)
        cnt += 1
        if data is None:
            log.warning(f'try number {cnt} failed for {audio_file_path}')
            time.sleep(0.5)

    if data is None:
        log.warning(f'{audio_file_path} had an HTTP Request failure')
        return
    if data.get('RecognitionStatus') != 'Success':
        logwarning = f'{audio_file_path} has an empty transcript'
        if data.get('RecognitionStatus') is not None:
            logwarning += ', RecognitionStatus = ' + data.get('RecognitionStatus')
        log.warning(logwarning)
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
            log.error(f'HTTP Request NOK ({response.status_code}), Body: {response.content}')
        return json.loads(response.content)
    except requests.exceptions.RequestException:
        log.error('HTTP Request failed')
