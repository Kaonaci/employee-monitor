from abc import ABC, abstractmethod


class Saver(ABC):
    @abstractmethod
    async def save(
        self,
        data: bytes,
        filename_with_ext: str,
    ) -> str:
        """Async save file to folder"""
