import logging
from os import path, remove

class Log:
    """
    Для конфигурации логгера.

    logger_format:
        устанавливает параметр формата лога, если уровень логирования указан DEBUG/ERROR/CRITICAL

    logger_file_handler:
        устанавливает параметры для записи в файл

    logger_stream_handler:
        устанавливает параметры для вывода в stdout

    logger:
        устанавливает параметры уровня логирования
    """

    def __init__(self, logging_level = "info", logging_file_name = None, **kwargs):
        self.logging = logging.getLogger()
        self.logging_level = logging_level
        self.logging_file_name = logging_file_name
        self.logging_file_format = logging.Formatter('[%(asctime)s] %(levelname)s - Sentry Rate Limiting: %(message)s')
        super().__init__(**kwargs)

    def logger_format(self):
        if self.logging_level.upper() in ["DEBUG", "ERROR", "CRITICAL"]:
            self.logging_file_format = logging.Formatter('[%(asctime)s] [%(levelname)s] (%(filename)s).%(funcName)s(%(lineno)d) - Sentry Rate Limiting: %(message)s')

    def logger_file_handler(self):
        if self.logging_file_name:
            self.file_handler = logging.FileHandler(self.logging_file_name)
            self.file_handler.setFormatter(self.logging_file_format)
            self.logging.addHandler(self.file_handler)

    def logger_stream_handler(self):
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.logging_file_format)
        self.logging.addHandler(self.stream_handler)

    def logger(self):
        self.logging.setLevel(self.logging_level.upper())
