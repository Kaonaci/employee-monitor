import asyncio
from pathlib import Path

from .infrastructure.camera_capture.opencv_camera_capture import OpenCVCameraCapture
from .infrastructure.config import Config
from .infrastructure.filename_generator.time_based_filename_format import (
    TimeBasedFilenameFormat,
)
from .infrastructure.saver.local_saver import LocalSaver
from .infrastructure.screen_capture.screen_capture_factory import ScreenCaptureFactory


async def main():
    # Read configuration from environment variables
    config = Config(Path("config.yaml")).load()

    screen_dir = config.screen_dir
    camera_dir = config.camera_dir
    interval = config.interval

    screen_dir.mkdir(parents=True, exist_ok=True)
    camera_dir.mkdir(parents=True, exist_ok=True)

    # Ensure target directories exist
    screen_dir.mkdir(parents=True, exist_ok=True)
    camera_dir.mkdir(parents=True, exist_ok=True)

    # Instantiate filename formatters with different prefixes
    screen_filename_generator = TimeBasedFilenameFormat(
        prefix="screen",
        extension="jpg",
    )
    camera_filename_generator = TimeBasedFilenameFormat(
        prefix="camera",
        extension="jpg",
    )

    # Instantiate savers for screen and camera folders
    screen_saver = LocalSaver(folder_path=screen_dir)
    camera_saver = LocalSaver(folder_path=camera_dir)

    # Initialize capture devices
    camera = OpenCVCameraCapture()
    screen = ScreenCaptureFactory()()

    # Start the camera and notify start
    await camera.start()
    print("Capture service started. Press Ctrl+C to stop.")

    try:
        while True:
            # Capture screen frame and webcam frame concurrently
            screen_data, camera_data = await asyncio.gather(
                screen.capture_screen(),
                camera.capture_frame()
            )

            # Generate unique filenames
            screen_filename = screen_filename_generator.generate()
            camera_filename = camera_filename_generator.generate()

            # Save files to disk concurrently without console prints inside the loop
            await asyncio.gather(
                screen_saver.save(screen_data, screen_filename),
                camera_saver.save(camera_data, camera_filename)
            )

            # Wait for the next interval
            await asyncio.sleep(interval)

    except asyncio.CancelledError:
        pass
    finally:
        # Properly release camera resources on exit
        await camera.stop()
        print("Capture service stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")