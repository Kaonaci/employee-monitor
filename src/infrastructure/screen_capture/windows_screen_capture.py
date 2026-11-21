import asyncio
from io import BytesIO

import mss
from PIL import Image

from ...domain.screen_capture import ScreenCapture


class WindowsScreenCapture(ScreenCapture):
    async def capture_screen(
        self,
        display_id: str | None = None,
    ) -> bytes:
        return await asyncio.to_thread(self._capture_screen, display_id)

    @staticmethod
    def _capture_screen(display_id: str | None) -> bytes:
        with mss.mss() as sct:
            monitor_index = int(display_id) if display_id is not None else 0

            if monitor_index < 0 or monitor_index >= len(sct.monitors):
                raise ValueError(f"Invalid display_id: {display_id}")

            screenshot = sct.grab(sct.monitors[monitor_index])

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb,
            )

            buffer = BytesIO()
            image.save(buffer, format="JPEG")

            return buffer.getvalue()