import glob
import os.path

from pydub import AudioSegment
from pydub.utils import which

from config import config
from util.logger import log


def _change_pitch_and_speed(sound, octaves=0.5):
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})


def convert_audio():
    if not which("ffmpeg"):
        log.warning("Couldn't find ffmpeg")

    for audio_file_path in glob.glob(os.path.join(config.clean_data_audio_dir(), '*.wav')):
        file_name = os.path.basename(audio_file_path)
        output_path = os.path.join(config.clean_data_custom_audio_dir(), file_name)
        log.info(f'Convert {file_name}')
        sound = AudioSegment.from_file(audio_file_path, format="wav")
        sound = _change_pitch_and_speed(sound)

        # 44.1k - standard audio CD
        sound = sound.set_frame_rate(44100)
        sound.export(output_path, format="wav")


if __name__ == '__main__':
    convert_audio()
