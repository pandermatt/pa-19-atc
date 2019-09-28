from os import environ
from os.path import dirname, abspath, join

ROOT_DIR = dirname(abspath(__file__))


class Config:

    @staticmethod
    def root_dir():
        return ROOT_DIR

    @staticmethod
    def data_dir():
        return abspath(join(Config.root_dir(), '.', 'data'))

    @staticmethod
    def original_data_dir():
        return join(Config.data_dir(), 'original')

    @staticmethod
    def original_data_text_dir():
        return join(Config.original_data_dir(), 'text')

    @staticmethod
    def original_data_audio_dir():
        return join(Config.original_data_dir(), 'audio')

    @staticmethod
    def clean_data_dir():
        return join(Config.data_dir(), 'clean')

    @staticmethod
    def clean_data_text_dir():
        return join(Config.clean_data_dir(), 'text')

    @staticmethod
    def clean_data_audio_dir():
        return join(Config.clean_data_dir(), 'audio')

    @staticmethod
    def test_data_dir():
        return join(Config.data_dir(), 'test')

    @staticmethod
    def test_data_text_dir():
        return join(Config.test_data_dir(), 'text')

    @staticmethod
    def test_data_audio_dir():
        return join(Config.test_data_dir(), 'audio')

    @staticmethod
    def train_data_dir():
        return join(Config.data_dir(), 'train')

    @staticmethod
    def train_data_text_dir():
        return join(Config.train_data_dir(), 'text')

    @staticmethod
    def train_data_audio_dir():
        return join(Config.train_data_dir(), 'audio')

    @staticmethod
    def accuracy_dir():
        return join(Config.data_dir(), 'accuracy')

    @staticmethod
    def text_analysis_dir():
        return join(Config.data_dir(), 'text_analysis')

    @staticmethod
    def atc_flight_level_example():
        return join(Config.text_analysis_dir(), 'atc_examples_flight_level.txt')

    @staticmethod
    def atc_flight_level_analysis_hypothesis():
        return join(Config.text_analysis_dir(), 'atc_flight_level_analysis_hypothesis.txt')

    @staticmethod
    def atc_flight_level_analysis_reference():
        return join(Config.text_analysis_dir(), 'atc_flight_level_analysis_reference.txt')

    @staticmethod
    def atc_flight_level_noteworthy_original():
        return join(Config.text_analysis_dir(), 'noteworthy_transmission_original.txt')

    @staticmethod
    def atc_flight_level_noteworthy_generated():
        return join(Config.text_analysis_dir(), 'noteworthy_transmission_generated.txt')

    @staticmethod
    def provider_accuracy_dir():
        return join(Config.accuracy_dir(), Config.provider())

    @staticmethod
    def provider_accuracy_file():
        return join(Config.accuracy_dir(), f'{Config.provider()}_accuracy.txt')

    @staticmethod
    def aws_s3_bucket():
        return _str('AWS_S3_BUCKET', default='bachelor-rege-01')

    @staticmethod
    def training_testing_split_ratio():
        return _float('TRAINING_TESTING_SPLIT_RATIO', default=0.8)

    @staticmethod
    def audio_speeds():
        return _list('AUDIO_SPEEDS', default='1.1')

    @staticmethod
    def provider():
        return 'microsoft_custom_speech'

    @staticmethod
    def enable_save_plot_to_file():
        return _bool('ENABLE_SAVE_PLOT_TO_FILE', default=True)

    @staticmethod
    def microsoft_speech_subscription_key():
        return _str('MICROSOFT_SPEECH_SUBSCRIPTION_KEY')

    @staticmethod
    def microsoft_luis_app_key():
        return _str('MICROSOFT_LUIS_APP_KEY')

    @staticmethod
    def microsoft_luis_subscription_key():
        return _str('MICROSOFT_LUIS_SUBSCRIPTION_KEY')

    @staticmethod
    def aws_access_key_id():
        return _str('AWS_ACCESS_KEY_ID')

    @staticmethod
    def aws_secret_access_key():
        return _str('AWS_SECRET_ACCESS_KEY')

    @staticmethod
    def language():
        return _str('LANG', default='de')


def _str(var, **kwargs):
    return str(_load(var, **kwargs))


def _int(var, **kwargs):
    return int(_load(var, **kwargs))


def _float(var, **kwargs):
    return float(_load(var, **kwargs))


def _list(var, **kwargs):
    return [float(speed) for speed in _load(var, **kwargs).split(',')]


def _bool(var, **kwargs):
    return bool(_str2bool(_load(var, **kwargs)))


def _str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


def _load(var, **kwargs):
    variable = _env().get(var) or kwargs.get('default')
    if not variable:
        print(f'Please set the environment variable \'{var}\'')
        # exit(1)
    return variable


def _env():
    if not hasattr(Config, '_ENV'):
        Config._ENV = {k: v for k, v in zip(environ.keys(), environ.values())}
    return Config._ENV
