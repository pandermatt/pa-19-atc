"""
Author: Pascal Andermatt and Jennifer Schürch
"""

import os
from os.path import dirname, abspath, join, exists

import yaml

from util.logger import log


def _get_or_create(dir_path):
    if not exists(dir_path):
        os.makedirs(dir_path)
        log.info("Creating: " + dir_path)
    return dir_path


class Config:
    _root_dir = dirname(abspath(__file__))
    _application_config_path = join(_root_dir, 'application.yml')
    _config_file = None

    #############
    # DIRECTORY #
    #############
    def data_dir(self):
        return abspath(join(self._root_dir, 'data'))

    def clean_data_dir(self):
        return _get_or_create(join(self.data_dir(), 'clean'))

    def clean_data_audio_dir(self):
        return _get_or_create(join(self.clean_data_dir(), 'audio'))

    def clean_data_text_dir(self):
        return _get_or_create(join(self.clean_data_dir(), 'text'))

    def clean_data_custom_audio_dir(self, suffix=''):
        return _get_or_create(join(self.clean_data_audio_dir(), 'custom' + suffix))

    def clean_data_cleaned_text_dir(self):
        return _get_or_create(join(self.clean_data_dir(), 'cleaned_text'))

    def train_data_dir(self):
        return _get_or_create(join(self.data_dir(), 'train_data_augmented'))

    def train_data_audio_dir(self, suffix=''):
        return _get_or_create(join(self.train_data_dir(), 'audio_files_simple' + suffix))

    def test_data_dir(self):
        return _get_or_create(join(self.data_dir(), 'test'))

    def test_data_text_dir(self):
        return _get_or_create(join(self.test_data_dir(), 'text'))

    def test_data_cleaned_text_dir(self):
        return _get_or_create(join(self.test_data_dir(), 'cleaned_text'))

    def test_data_audio_dir(self):
        return _get_or_create(join(self.test_data_dir(), 'audio'))

    def accuracy_dir(self):
        return _get_or_create(join(self.data_dir(), 'accuracy'))

    def provider_accuracy_dir(self, prefix=''):
        return _get_or_create(join(self.data_dir(), prefix + 'microsoft_custom_speech'))

    def provider_accuracy_dir_nocreate(self, prefix=''):
        return join(self.data_dir(), prefix + 'microsoft_custom_speech')

    def provider_accuracy_file(self, prefix=''):
        return _get_or_create(join(self.accuracy_dir(), f'{self.provider(prefix)}_accuracy.txt'))

    def provider_accuracy_file_nocreate(self, prefix=''):
        return join(self.accuracy_dir(), f'{self.provider(prefix)}_accuracy.txt')

    def provider_accuracy_average_file(self, prefix=''):
        return join(self.accuracy_dir(), f'{self.provider(prefix)}_average.txt')

    def keyword_dir(self):
        return _get_or_create(join(self.data_dir(), 'keyword'))

    def original_keyword_dir(self):
        return _get_or_create(join(self.keyword_dir(), 'original'))

    def compare_keyword_dir(self):
        return _get_or_create(join(self.keyword_dir(), 'compare'))

    def audio_keyword_dir(self):
        return _get_or_create(join(self.keyword_dir(), 'audio'))

    def provider(self, prefix=''):
        return prefix+'microsoft_custom_speech'

    #############
    # KEYS      #
    #############
    def microsoft_speech_subscription_key(self):
        return self._get_var('MICROSOFT_SPEECH_SUBSCRIPTION_KEY')

    def microsoft_speech_endpoint_id(self):
        return self._get_var('MICROSOFT_SPEECH_ENDPOINT_ID')

    def microsoft_luis_app_key(self):
        return self._get_var('MICROSOFT_LUIS_APP_KEY')

    def microsoft_luis_subscription_key(self):
        return self._get_var('MICROSOFT_LUIS_SUBSCRIPTION_KEY')

    def _get_var(self, var):
        if not self._config_file:
            try:
                with open(self._application_config_path, 'r') as stream:
                    self._config_file = yaml.safe_load(stream)
                    log.info("Config Loaded")
            except FileNotFoundError:
                log.info("Config not found, using ENV Var")
                return os.environ.get(var)
        try:
            return os.environ.get(var) or self._config_file[var]
        except KeyError:
            log.exit('Can not find ENV var: %s' % var)


config = Config()
