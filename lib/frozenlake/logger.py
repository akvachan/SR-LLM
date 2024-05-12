import os
from oshandler import OSHandler

from logger import Logger


class ChatLogger(Logger):
    level = "info"
    format = "{asctime} : {role} : {content}"

    def put(self, extra, message="") -> None:
        self.logger.info(message, extra=extra)

    def flush(self) -> None:
        OSHandler.remove_file(os.path.join(self.location, self.name))
