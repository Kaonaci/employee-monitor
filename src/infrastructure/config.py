import math
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AppConfig:
    screen_dir: Path
    camera_dir: Path
    interval: float


class Config:
    def __init__(self, config_path: Path):
        self._config_path = Path(config_path)

    def load(self) -> AppConfig:
        if not self._config_path.is_file():
            raise FileNotFoundError(
                f"Configuration file '{self._config_path}' does not exist."
            )

        with self._config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        if not isinstance(data, dict):
            raise TypeError("Configuration must contain a YAML mapping.")

        screen_dir = self._get_path(data, "screen_dir", "./screenshots")
        camera_dir = self._get_path(data, "camera_dir", "./webcam_snapshots")
        interval = self._get_interval(data)

        return AppConfig(
            screen_dir=screen_dir,
            camera_dir=camera_dir,
            interval=interval,
        )

    @staticmethod
    def _get_path(data: dict, key: str, default: str) -> Path:
        value = data.get(key, default)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid path configuration: '{key}'.")

        return Path(value).expanduser()

    @staticmethod
    def _get_interval(data: dict) -> float:
        try:
            value = data.get("interval_seconds", 180)

            if isinstance(value, bool):
                raise TypeError

            interval = float(value)

            if not math.isfinite(interval) or interval <= 0:
                raise ValueError

            return interval

        except (TypeError, ValueError):
            raise ValueError(
                "Configuration 'interval_seconds' must be a positive number."
            ) from None