from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import tomlkit

if TYPE_CHECKING:
    from ..pins.input_pin import InputPin
    from ..pins.output_pin import OutputPin
    from ..pins.virtual_pin import VirtualPin

    class Project(TypedDict):
        name: str

    class Config(TypedDict):
        Project: Project
        InputPins: list[InputPin]
        OutputPins: list[OutputPin]
        VirtualPins: list[VirtualPin]


class ConfigParser:
    config_file_path: Path

    def __init__(self, config_file_path: str | Path):
        self.config_file_path = Path(config_file_path)

    def load_config(self):
        with open(self.config_file_path, "rb") as f:
            config = tomlkit.load(f)
            return config.unwrap()

    def save_config(self, config: Config, with_timestamp: bool = False):
        config_file_path = self.config_file_path

        if with_timestamp:
            timstamp = datetime.now().strftime("%Y%m%d-%H%M")

            config_file_path = Path(
                self.config_file_path.parent, f"{timstamp}_{self.config_file_path.stem}{self.config_file_path.suffix}"
            )
        with open(config_file_path, "w") as f:
            # convert config to tomlkit document
            tomlkit.dump(config, f)  # type: ignore


if __name__ == "__main__":
    from pathlib import Path

    # git this file dir
    this_dir = Path(__file__).parent
    parser = ConfigParser(this_dir / "./test_config.toml")
    config = parser.load_config()
    print(config)
