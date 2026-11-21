from ..infrastructure.filename_generator.time_based_filename_format import (
    TimeBasedFilenameFormat,
)


def main() -> None:
    generator = TimeBasedFilenameFormat(
        prefix="cap",
        extension="jpg",
        time_format="%Y-%m-%d_%H-%M-%S",
    )

    filename = generator.generate()

    print(f"Generated filename: {filename}")


if __name__ == "__main__":
    main()