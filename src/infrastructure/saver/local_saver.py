import asyncio
from pathlib import Path

from ...domain.saver import Saver


class LocalSaver(Saver):
    def __init__(self, folder_path: Path):
        self._folder = Path(folder_path)

        if not self._folder.exists() or not self._folder.is_dir():
            raise FileNotFoundError(
                f"Folder '{self._folder}' does not exist or is not a directory."
            )

    async def save(
        self,
        data: bytes,
        filename_with_ext: str,
    ) -> str:
        file_path = self._folder / filename_with_ext

        await asyncio.to_thread(file_path.write_bytes, data)

        return str(file_path)