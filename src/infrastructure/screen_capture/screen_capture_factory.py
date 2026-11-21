import os
import sys

from ...domain.screen_capture import ScreenCapture


class ScreenCaptureFactory:
    def _create_grim_capture(self) -> ScreenCapture:
        from .grim_screen_capture import GrimScreenCaprute
        return GrimScreenCaprute()

    def _create_windows_capture(self) -> ScreenCapture:
        from .windows_screen_capture import WindowsScreenCapture
        return WindowsScreenCapture()

    def __call__(self) -> ScreenCapture:
        if sys.platform == "win32":
            return self._create_windows_capture()
        
        if sys.platform == "linux":
            is_wayland = (
                os.environ.get("WAYLAND_DISPLAY") is not None
                or os.environ.get("XDG_SESSION_TYPE") == "wayland"
            )

            if is_wayland:
                return self._create_grim_capture()
                
            raise RuntimeError("Only Wayland is now supported on Linux.")

        raise RuntimeError(f"Unsupported platform: {sys.platform}")
