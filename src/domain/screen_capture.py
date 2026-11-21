from abc import ABC, abstractmethod


class ScreenCapture(ABC):
    @abstractmethod
    async def capture_screen(self, display_id: str | None = None) -> bytes:
        """Capture current screen frame"""
