import datetime
from oshandler import OSHandler


class Logger:
    log_path: str = "logs"

    @classmethod
    def log(cls, source, content, to_logs=False) -> None:
        """

        :param source:
        :param content:
        :param to_logs:
        :return:
        """
        print(datetime.datetime, content)
        if to_logs:
            if not OSHandler.check_path(cls.log_path, source):
                OSHandler.write_to_file(content, cls.log_path, source)
            else:
                OSHandler.add_to_file(content, cls.log_path, source)

    @classmethod
    def flush_logs(cls) -> None:
        """

        :return:
        """
        pass
