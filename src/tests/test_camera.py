import asyncio
from pathlib import Path

from ..infrastructure.camera_capture.opencv_camera_capture import OpenCVCameraCapture


async def main() -> None:
    camera = OpenCVCameraCapture(camera_index=0)

    try:
        await camera.start()
        print("Camera connected")

        image = await camera.capture_frame()

        output = Path("test_capture.jpg")
        output.write_bytes(image)

        print(f"Frame captured: {len(image)} bytes")
        print(f"Saved to: {output.resolve()}")

    finally:
        await camera.stop()
        print("Camera disconnected")


if __name__ == "__main__":
    asyncio.run(main())