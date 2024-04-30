import os
import json


class OSHandler:

    @staticmethod
    def check_path(*path) -> bool:
        """

        :param path:
        :return:
        """
        return os.path.exists(os.path.join(*path))

    @staticmethod
    def make_dir(*path) -> None:
        """

        :param path:
        :return:
        """
        os.makedirs(os.path.join(*path))

    @staticmethod
    def write_to_file(content: str, *path) -> None:
        """

        :param path:
        :param content:
        :return:
        """
        with open(os.path.join(*path), 'w') as f:
            f.write(content)

    @staticmethod
    def write_to_json(content: dict, *path) -> None:
        """

        :param path:
        :param content:
        :return:
        """
        with open(os.path.join(*path), 'w') as json_file:
            json.dump(content, json_file, indent=4)

    @staticmethod
    def read_from_file(*path) -> str:
        """

        :param path:
        :return:
        """
        with open(os.path.join(*path), 'r') as f:
            return f.read()

    @staticmethod
    def read_from_json(*path) -> dict:
        """

        :param path:
        :return:
        """
        with open(os.path.join(*path), 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def add_to_file(content: str, *path) -> None:
        """

        :param path:
        :param content:
        :return:
        """
        with open(os.path.join(*path), 'a') as f:
            f.write(content)


    @staticmethod
    def get_project_root(_file):
        """
        CAREFUL: This method works only from within custom subpackage

        :param _file:
        :return:
        """
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_file))))

    @staticmethod
    def get_file_list(*path) -> list[str]:
        return [f for f in os.listdir(os.path.join(*path)) if os.path.isfile(os.path.join(*path, f))]
