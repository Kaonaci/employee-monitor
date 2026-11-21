import asyncio

from ...domain.screen_capture import ScreenCapture


class GrimScreenCaprute(ScreenCapture):
    async def capture_screen(
        self,
        display_id: str | None = None,
    ) -> bytes:
        command = ["grim"]

        if display_id is not None:
            command.extend(["-o", display_id])

        command.extend(["-t", "jpeg", "-"])

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_message = stderr.decode().strip()
            raise RuntimeError(
                f"Failed to capture screen using 'grim': {error_message}"
            )

        return stdout