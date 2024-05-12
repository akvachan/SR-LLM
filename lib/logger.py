from abc import abstractmethod
import logging
import os

from oshandler import OSHandler


class Logger(logging.getLoggerClass()):
    def __init__(self, location, name):
        if not os.path.exists(location):
            OSHandler.make_dir(location)

        self.name = name
        self.logger = logging.getLogger(self.name)
        self.location = location
        self.logger.setLevel(self.to_log_level(self.level))
        self.file_handler = logging.FileHandler(os.path.join(location, self.name + ".log"))
        self.formatter = logging.Formatter(self.format, style="{")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)



    @property
    def level(self) -> str:
        ...

    @property
    def format(self) -> str:
        ...

    @staticmethod
    def to_log_level(log_level: str):
        if log_level == "info":
            level = logging.INFO
        elif log_level == "warning":
            level = logging.WARNING
        elif log_level == "error":
            level = logging.ERROR
        return level

    @abstractmethod
    def flush(self) -> None:
        ...

    @abstractmethod
    def put(self, message, extra) -> None:
        ...


