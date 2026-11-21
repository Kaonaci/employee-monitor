from datetime import datetime

from ...domain.filename_generator import FilenameGenerator


class TimeBasedFilenameFormat(FilenameGenerator):
    def __init__(
        self,
        prefix: str,
        extension: str,
        time_format: str = "%Y-%m-%d_%H-%M-%S",
    ):
        self._prefix = prefix
        self._extension = extension.lstrip(".")
        self._time_format = time_format
        self._index = 0

    def generate(self) -> str:
        timestamp = datetime.now().strftime(self._time_format)

        filename = (
            f"{self._prefix}_{timestamp}_{self._index}.{self._extension}"
        )

        self._index += 1

        return filename