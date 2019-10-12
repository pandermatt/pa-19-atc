import glob
import os

import librosa
import numpy as np
from pydub import AudioSegment
from pydub.effects import speedup
from pydub.utils import which

from config import config
from util.logger import log


def convert_audio_files():
    if not which("ffmpeg"):
        log.warning("Couldn't find ffmpeg")

    for original_audio_file_path in glob.glob(os.path.join(config.clean_data_audio_dir(), '*.wav')):
        for speed in [0.9, 1.1, 1.3]:
            _convert_audio(original_audio_file_path, speed)

        for speed in [1.1]:
            _convert_audio_with_normalisation(original_audio_file_path, speed)

        _convert_audio_with_noise_injection(original_audio_file_path, 0.01)


def _convert_audio(audio_file_path, speed):
    file_name = os.path.basename(audio_file_path)
    output_path = os.path.join(config.clean_data_custom_audio_dir(prefix=str(speed)), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{speed}')
        return

    log.info(f'Convert {file_name} with {speed}')
    sound = AudioSegment.from_file(audio_file_path, format="wav")
    sound = speedup(sound, playback_speed=speed)

    # 44.1k - standard audio CD
    sound = sound.set_frame_rate(44100)
    sound.export(output_path, format="wav")


def _convert_audio_with_normalisation(audio_file_path, speed):
    file_name = os.path.basename(audio_file_path)
    output_path = os.path.join(config.clean_data_custom_audio_dir(prefix=str(speed) + '-normal'), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{speed}-normalisation')
        return

    log.info(f'Convert {file_name} with 1.1 normalisation')
    os.system(f'ffmpeg -i {audio_file_path}  -filter:a "atempo={speed}" {output_path}')


def _convert_audio_with_noise_injection(audio_file_path, noise_factor):
    file_name = os.path.basename(audio_file_path)
    output_path = os.path.join(config.clean_data_custom_audio_dir(prefix=str(noise_factor) + '-noise'), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{noise_factor}-noise')
        return

    log.info(f'Convert {file_name} with noise injection')
    data, sr = librosa.load(audio_file_path)

    noise = np.random.randn(len(data))
    augmented_data = data + noise_factor * noise
    augmented_data = augmented_data.astype(type(data[0]))

    librosa.output.write_wav(output_path, augmented_data, sr)


if __name__ == '__main__':
    convert_audio_files()
