import json

import requests

from util.config import config
from util.logger import log

REGION = 'westeurope'
MODE = 'interactive'
LANG = 'en-US'
FORMAT = 'detailed'


def speech_to_text(audio_file_path):
    api_url = 'https://{0}.stt.speech.microsoft.com/speech/recognition/' \
              '{1}/cognitiveservices/v1?language={2}&format={3}'.format(REGION, MODE, LANG, FORMAT)
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
    transcript = data.get('NBest')[0].get('Display')
    if transcript == '' or data.get('RecognitionStatus') != 'Success':
        log.warning(f'{audio_file_path} has an empty transcript')
        return
    log.info("Transcript: %s" % transcript)
    return transcript
