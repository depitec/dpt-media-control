from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, TypedDict

import tomlkit

if TYPE_CHECKING:
    from PinManager.Pins.InputPin import InputPin
    from PinManager.Pins.OutputPin import OutputPin
    from PinManager.Pins.VirtualPin import VirtualPin

    class Project(TypedDict):
        name: str

    class Config(TypedDict):
        Project: Project
        InputPins: list[InputPin]
        OutputPins: list[OutputPin]
        VirtualPins: list[VirtualPin]


class ConfigParser:
    config_file_path: Path
    _config: tomlkit.TOMLDocument

    def __init__(self, config_file_path: str | Path, project: Project):
        self.config_file_path = Path(config_file_path)

        inital_toml_doc = tomlkit.document()
        project_object = tomlkit.table()

        for key, value in project.items():
            project_object.add(key, value)

        inital_toml_doc.add("Project", project_object)

        self._config = inital_toml_doc

    @property
    def config(self):
        return self._config.unwrap()

    def set_config(self, config: Config):
        self._config = self._dict_to_toml_doc(config)

    def update_config(self, partial_config: Optional[Config]):
        pass

    def load_config(self):
        with open(self.config_file_path, "rb") as f:
            config = tomlkit.load(f)
            self._config = config

    def save_config(self, with_timestamp: bool = False):
        config_file_path = self.config_file_path

        if with_timestamp:
            timstamp = datetime.now().strftime("%Y%m%d-%H%M")

            config_file_path = Path(
                self.config_file_path.parent, f"{timstamp}_{self.config_file_path.stem}{self.config_file_path.suffix}"
            )
        with open(config_file_path, "w") as f:
            # convert config to tomlkit document
            tomlkit.dump(self._config.unwrap(), f)

    def _pin_to_id(self, pin: InputPin | OutputPin | VirtualPin):
        return pin.id

    def _dict_to_toml_doc(self, config: Config):
        pass
        # doc = tomlkit.document()

        # doc.add
        # config.items()
        # project_table = tomlkit.table()
        # project_table.add("name", config["Project"]["name"])

        # doc.add("Project", project_table)

        # input_pins_array = tomlkit.array()
        # for input_pin in config["InputPins"]:
        #     input_pin_table = tomlkit.table()
        #     input_pin_table.add("id", input_pin.id)
        #     input_pin_table.add("display_name", input_pin.display_name)
        #     input_pin_table.add("gpio_pin", input_pin.gpio_pin)
        #     input_pin_table.add("activation_delay", input_pin.activation_delay)
        #     input_pin_table.add("is_blocked", input_pin.is_blocked)
        #     input_pin_table.add("pins_to_block", input_pin.pins_to_block)
        #     input_pin_table.add("pins_to_unblock", input_pin.pins_to_unblock)

        #     pins_to_trigger_ids = map(self._pin_to_id, input_pin.pins_to_trigger)

        #     input_pin_table.add("pins_to_trigger", pins_to_trigger_ids)

        # doc.add("InputPins", input_pins_array)

        # return doc


if __name__ == "__main__":
    from pathlib import Path

    # get root dir
    root_dir = Path(__file__).parent.parent.parent
    parser = ConfigParser(root_dir / "tests/ConfigParser/resources/testconfig.toml", {"name": "dpt-media-control"})
    parser.load_config()
    config = parser.config
    print(config)
