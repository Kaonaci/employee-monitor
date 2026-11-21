import asyncio
from pathlib import Path

from ..infrastructure.screen_capture.screen_capture_factory import ScreenCaptureFactory


async def main() -> None:
    screen_capture = ScreenCaptureFactory()()

    image_data = await screen_capture.capture_screen()

    output_path = Path("test_screen.jpg")
    output_path.write_bytes(image_data)

    print(f"Screen captured: {len(image_data)} bytes")
    print(f"Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())