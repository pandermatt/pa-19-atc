import csv
import glob
import os
import random

import librosa
import numpy as np
from pydub import AudioSegment
from pydub.utils import which

from config import config
from util.logger import log

#AUDIO_DIR = config.train_data_audio_dir
AUDIO_DIR = config.test_data_audio_dir


def convert_audio_files():
    if not which("ffmpeg"):
        log.warning("Couldn't find ffmpeg")

    error_files = []

    for original_audio_file_path in glob.glob(os.path.join(AUDIO_DIR(), '*.wav')):
        try:
            for speed in []:
                _convert_audio(original_audio_file_path, speed)

            for speed in []:
                _convert_audio_with_normalisation(original_audio_file_path, speed)

            _convert_audio_with_noise_injection(original_audio_file_path, 0.01)
            _convert_audio_with_noise_injection(original_audio_file_path, 0.03)
            _convert_audio_with_noise_injection(original_audio_file_path, 0.05)
            _convert_audio_with_noise_injection(original_audio_file_path, 0.07)
            _convert_audio_with_noise_injection(original_audio_file_path, 0.09)
            _convert_audio_with_noise_injection(original_audio_file_path, 0.1)

            #_convert_audio_with_random_speed(original_audio_file_path, random.choice(np.arange(0.7, 1.3, 0.1)))
        except:
            error_files.append(original_audio_file_path)
            log.warning(f'Could not convert {original_audio_file_path}')

    if len(error_files) != 0:
        log.warning(f'Could not convert {error_files}')


def _convert_audio(audio_file_path, speed):
    suffix = f'_speed-{speed}'
    file_name = _add_suffix(audio_file_path, suffix)
    output_path = os.path.join(AUDIO_DIR(suffix), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{speed}')
        return

    log.info(f'Convert {file_name} with {speed}')
    sound = AudioSegment.from_file(audio_file_path, format="wav")
    sound = _change_pitch_and_speed(sound, speed)

    sound = sound.set_frame_rate(16000)
    sound.export(output_path, format="wav")


def _convert_audio_with_random_speed(audio_file_path, speed):
    suffix = f'_random-speed'
    file_name = _add_suffix(audio_file_path, suffix)
    output_path = os.path.join(AUDIO_DIR(suffix), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-random-speed')
        return

    log.info(f'Convert {file_name} with random {speed}')
    sound = AudioSegment.from_file(audio_file_path, format="wav")
    sound = _change_pitch_and_speed(sound, speed)

    sound = sound.set_frame_rate(16000)
    sound.export(output_path, format="wav")

    file = os.path.join(AUDIO_DIR(suffix), 'result_random.csv')
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([speed, file_name])


def _change_pitch_and_speed(sound, speed):
    new_sample_rate = int(sound.frame_rate * speed)
    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})


def _convert_audio_with_normalisation(audio_file_path, speed):
    suffix = f'_speed-{speed}-normal'
    file_name = _add_suffix(audio_file_path, suffix)
    output_path = os.path.join(AUDIO_DIR(suffix), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{speed}-normalisation')
        return

    log.info(f'Convert {file_name} with 1.1 normalisation')
    os.system(f'ffmpeg -i {audio_file_path}  -filter:a "atempo={speed}" {output_path}')


def _convert_audio_with_noise_injection(audio_file_path, noise_factor):
    suffix = f'_noise-{noise_factor}'
    file_name = _add_suffix(audio_file_path, suffix)
    output_path = os.path.join(AUDIO_DIR(suffix), file_name)

    if os.path.exists(output_path):
        log.info(f'already exists... skipping:\t {file_name}-{noise_factor}-noise')
        return

    log.info(f'Convert {file_name} with noise injection')
    data, sr = librosa.load(audio_file_path)

    noise = np.random.randn(len(data))
    augmented_data = data + noise_factor * noise
    augmented_data = augmented_data.astype(type(data[0]))

    librosa.output.write_wav(output_path, augmented_data, sr)


def _add_suffix(audio_file_path, suffix):
    filename = os.path.basename(audio_file_path)
    return "{0}{2}.{1}".format(*filename.rsplit('.', 1) + [suffix])


if __name__ == '__main__':
    convert_audio_files()
