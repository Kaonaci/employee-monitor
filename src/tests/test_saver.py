import asyncio
from pathlib import Path

from ..infrastructure.saver.local_saver import LocalSaver


async def main() -> None:
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)

    saver = LocalSaver(output_dir)

    data = b"Hello, World!"
    filename = "test.txt"

    saved_path = await saver.save(data, filename)

    file_path = Path(saved_path)

    print(f"File saved: {file_path.resolve()}")
    print(f"File exists: {file_path.exists()}")
    print(f"Content matches: {file_path.read_bytes() == data}")
    print(f"File size: {file_path.stat().st_size} bytes")


if __name__ == "__main__":
    asyncio.run(main())