import asyncio

import cv2

from ...domain.camera_capture import CameraCapture


class OpenCVCameraCapture(CameraCapture):
    def __init__(
        self,
        camera_index: int = 0,
        image_format: str = ".jpg",
        buffer_flush_frames: int = 3,
    ):
        self._camera_index = camera_index
        self._image_format = (
            image_format
            if image_format.startswith(".")
            else f".{image_format}"
        )
        self._buffer_flush_frames = buffer_flush_frames
        self._cap: cv2.VideoCapture | None = None

    async def start(self) -> None:
        self._cap = await asyncio.to_thread(
            cv2.VideoCapture,
            self._camera_index,
        )

        if not await asyncio.to_thread(self._cap.isOpened):
            await asyncio.to_thread(self._cap.release)
            self._cap = None
            raise RuntimeError(
                f"Failed to connect to camera with index {self._camera_index}"
            )

        await asyncio.to_thread(
            self._cap.set,
            cv2.CAP_PROP_BUFFERSIZE,
            1,
        )

    async def stop(self) -> None:
        if self._cap is not None:
            await asyncio.to_thread(self._cap.release)
            self._cap = None

    async def capture_frame(self) -> bytes:
        if self._cap is None:
            raise RuntimeError("Camera is not running. Call start() first.")

        for _ in range(self._buffer_flush_frames):
            await asyncio.to_thread(self._cap.grab)

        ret, frame = await asyncio.to_thread(self._cap.retrieve)

        if not ret or frame is None:
            raise RuntimeError("Failed to read a frame from the camera.")

        success, encoded_image = await asyncio.to_thread(
            cv2.imencode,
            self._image_format,
            frame,
        )

        if not success:
            raise RuntimeError("Failed to encode the camera image.")

        return encoded_image.tobytes()