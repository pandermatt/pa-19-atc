from os import environ
from os.path import dirname, abspath, join

import yaml

from logger import log

APPLICATION_CONFIG_PATH = join(dirname(abspath(__file__)), 'application.yml')


class Config:
    _config_file = None

    def data_dir(self):
        return abspath(join(dirname(abspath(__file__)), 'data'))

    def clean_data_dir(self):
        return join(self.data_dir(), 'clean')

    def clean_data_audio_dir(self):
        return join(self.clean_data_dir(), 'audio')

    def provider_accuracy_dir(self):
        return join(self.data_dir(), 'microsoft_custom_speech')

    def microsoft_speech_subscription_key(self):
        return self._get_var('MICROSOFT_SPEECH_SUBSCRIPTION_KEY')

    def microsoft_luis_app_key(self):
        return self._get_var('MICROSOFT_LUIS_APP_KEY')

    def microsoft_luis_subscription_key(self):
        return self._get_var('MICROSOFT_LUIS_SUBSCRIPTION_KEY')

    def _get_var(self, var):
        if not self._config_file:
            try:
                with open(APPLICATION_CONFIG_PATH, 'r') as stream:
                    self._config_file = yaml.safe_load(stream)
                    log.info("Config Loaded")
            except FileNotFoundError:
                log.info("Config not found, using ENV Var")
                return environ.get(var)
        return environ.get(var) or self._config_file[var]


config = Config()
