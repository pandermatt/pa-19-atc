import json

import requests

from config import config
from logger import log


def transcribe_microsoft_custom_speech(audio_file_path):
    api_url = 'https://westeurope.stt.speech.microsoft.com/speech/recognition' \
              '/conversation/cognitiveservices/v1?language=en-CA'
    headers = {
        'Ocp-Apim-Subscription-Key': config.microsoft_speech_subscription_key(),
        'Content-Type': 'audio/wav; codecs=audio/pcm;'
    }

    response = requests.post(
        api_url,
        data=open(audio_file_path, 'rb'),
        headers=headers
    )

    if not response.ok:
        log.warning(f'Response code {response.status_code} for {audio_file_path}')
        return

    data = json.loads(response.content)
    transcript = data.get('DisplayText')
    if transcript == '':
        log.warning(f'{audio_file_path} has an empty transcript')
        return
    log.info("Transcript: %s" % transcript)
    return transcript
