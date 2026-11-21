from abc import ABC, abstractmethod


class CameraCapture(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Async start or connect to camera"""

    @abstractmethod
    async def stop(self) -> None:
        """Async stop or disconnect from camera"""

    @abstractmethod
    async def capture_frame(self) -> bytes:
        """Capture current camera frame"""
