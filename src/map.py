from abc import ABC, abstractmethod


class Map(ABC):
    pass


class MapGenerator(ABC):
    """
    Abstract map generation class.
    Implement this class for custom map generation logic.
    MapGenerator methods are responsible for generating custom maps and saving them on disk.

    Attributes
    ----------
    maps_dir: str
        Name of directory where generated maps are stored, usually just "maps".
    map_name: str
        Name of your custom map, usually in PascalCase and with version number, e.g.: "MyMap-v2".

    Methods
    -------
    generate_batch(*args) -> None
        Generates a batch (multiple) maps and saves them on disk.
    generate_single(*args) -> None
        Generates a single map and (potentially) saves it on disk.
    """

    @property
    def maps_dir(self) -> str:
        pass

    @property
    def map_name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def generate_batch(cls, *args) -> None:
        pass

    @classmethod
    @abstractmethod
    def generate_single(cls, *args) -> None:
        pass


class MapManipulator(ABC):
    """
    Abstract map manipulation and altering class.
    Implement this class in case you need to manipulate or alter your map.
    """
    pass


class MapSolver(ABC):
    """
    Abstract class for solving your map, e.g., finding optimal paths.
    Implement this class in case you want to generate solutions to your map.

    Attributes
    ----------
    maps_dir: str
        Name of directory where generated maps are stored, usually just "maps".

    Methods
    -------
    solve_batch(*args) -> None
        Solves a batch (multiple) maps and saves solutions on disk.
    solve_single(*args) -> None
        Solves a single map and saves its solution on disk.
    """

    @property
    def maps_dir(self) -> str:
        pass

    @property
    def map_name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def solve_batch(cls, *args) -> None:
        pass

    @classmethod
    @abstractmethod
    def solve_single(cls, *args) -> None:
        pass
