import os
import json
from typing import List, Dict, Any


class OSHandler:
    @staticmethod
    def check_path(*path: str) -> bool:
        return os.path.exists(os.path.join(*path))

    @staticmethod
    def make_dir(*path: str) -> None:
        os.makedirs(os.path.join(*path))

    @staticmethod
    def write_to_file(content: str, *path: str) -> None:
        with open(os.path.join(*path), 'w') as f:
            f.write(content)

    @staticmethod
    def write_to_json(content: Any, *path: str) -> None:
        with open(os.path.join(*path), 'w') as json_file:
            json.dump(content, json_file, indent=4)

    @staticmethod
    def read_from_file(*path: str) -> str:
        with open(os.path.join(*path)) as f:
            return f.read()

    @staticmethod
    def read_from_json(*path: str) -> Dict[str, Any]:
        with open(os.path.join(*path), 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def add_to_file(content: str, *path: str) -> None:
        with open(os.path.join(*path), 'a') as f:
            f.write(content)

    @staticmethod
    def get_project_root() -> str:
        # CAREFUL: Hardcoded for now
        return os.path.join("/", "Users", "arseniikvachan", "PycharmProjects", "SR-LLM")

    @staticmethod
    def get_file_list(*path: str) -> List[str]:
        return [f for f in os.listdir(os.path.join(*path)) if os.path.isfile(os.path.join(*path, f))]

    @staticmethod
    def remove_dir(*path: str) -> None:
        os.rmdir(os.path.join(*path))
