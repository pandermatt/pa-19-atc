import json

import requests

from config import config


def transcribe_microsoft_custom_speech(audio_file_path):
    api_url = 'https://westeurope.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-CA'
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
        print(response)
        print(f'Response code {response.status_code} for {audio_file_path}')
        return

    data = json.loads(response.content)
    transcript = data.get('DisplayText', '')
    if transcript == '':
        print(f'Failed for {audio_file_path}')
        return
    print(transcript)
    return transcript
