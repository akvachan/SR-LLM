from abc import ABC
import jsonpickle
import os

from oshandler import OSHandler


class Intel(ABC):
    def serialize(self, location: str, name: str) -> None:
        if not os.path.exists(location):
            OSHandler.make_dir(location)
        json_str = jsonpickle.encode(self)
        OSHandler.write_to_json(json_str, os.path.join(location, f"{name}.json"))

    @staticmethod
    def deserialize(json_path: str) -> 'Intel':
        json_str = OSHandler.read_from_json(json_path)
        return jsonpickle.decode(json_str)
