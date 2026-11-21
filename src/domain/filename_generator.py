from abc import ABC, abstractmethod


class FilenameGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        """Get name for file"""
