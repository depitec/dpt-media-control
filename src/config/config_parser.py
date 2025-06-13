from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Sequence, TypedDict

import tomlkit

if TYPE_CHECKING:
    from pins.input_pin import InputPin
    from pins.output_pin import OutputPin, OutputTriggerMethods
    from pins.pin import Pin
    from pins.virtual_pin import VirtualPin, VirtualPinMethod

    class Project(TypedDict):
        name: str

    class PinConfig(TypedDict):
        id: str
        gpio_pin: int
        display_name: str
        pins_to_block: list[str]
        pins_to_unblock: list[str]

    class InputPinConfig(PinConfig):
        activation_delay: int
        triggered_pins: list[str]

    class OutputPinConfig(PinConfig):
        hold_time: int
        trigger_method: OutputTriggerMethods

    class VirtualPinConfig(PinConfig):
        ip_adress: str
        virtual_pin_method: VirtualPinMethod

    class Config(TypedDict):
        Project: Project
        InputPins: list[InputPinConfig]
        OutputPins: list[OutputPinConfig]
        VirtualPins: list[VirtualPinConfig]


class ConfigParser:
    config_file_path: Path

    def __init__(self, config_file_path: str | Path):
        self.config_file_path = Path(config_file_path)
        self.init_check()

    def init_check(self):
        if not self.config_file_path.exists():
            # create config file and parent directories if they don't exist
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_file_path.touch()

    def load_config(self) -> Config:
        with open(self.config_file_path, "rb") as f:
            config = tomlkit.load(f)
            config_dict = config.unwrap()
            # typecase config_dict to Config
            # retrn type is wrong see: https://github.com/python/mypy/issues/8890
            return config_dict  # type: ignore

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

    def pins_to_ids(self, pins: Sequence[Pin | VirtualPin | OutputPin | InputPin]):
        return [pin.id for pin in pins]

    def config_to_toml(self, config: Config):
        toml_project_table = tomlkit.table()
        toml_project_table.add("name", config["Project"]["name"])

        toml_input_pins_array = tomlkit.array()

        for input_pin in config["InputPins"]:
            toml_input_pin_table = tomlkit.table()
            toml_input_pin_table.add("id", input_pin["id"])
            toml_input_pin_table.add("display_name", input_pin["display_name"])
            toml_input_pin_table.add("gpio_pin", input_pin["gpio_pin"])
            toml_input_pin_table.add("activation_delay", input_pin["activation_delay"])
            toml_input_pin_table.add("pins_to_trigger", input_pin["triggered_pins"])
            toml_input_pin_table.add("pins_to_block", input_pin["pins_to_block"])
            toml_input_pin_table.add("pins_to_unblock", input_pin["pins_to_unblock"])

            toml_input_pins_array.append(toml_input_pin_table)  # type: ignore

        toml_output_pins_array = tomlkit.array()
        for output_pin in config["OutputPins"]:
            toml_output_pin_table = tomlkit.table()
            toml_output_pin_table.add("id", output_pin["id"])
            toml_output_pin_table.add("display_name", output_pin["display_name"])
            toml_output_pin_table.add("gpio_pin", output_pin["gpio_pin"])
            toml_output_pin_table.add("trigger_method", output_pin["trigger_method"])
            toml_output_pin_table.add("hold_time", output_pin["hold_time"])
            toml_output_pin_table.add("pins_to_block", output_pin["pins_to_block"])
            toml_output_pin_table.add("pins_to_unblock", output_pin["pins_to_unblock"])

            toml_output_pins_array.append(toml_output_pin_table)  # type: ignore

        toml_virtual_pins_array = tomlkit.array()
        for virtual_pin in config["VirtualPins"]:
            toml_virtual_pin_table = tomlkit.table()
            toml_virtual_pin_table.add("id", virtual_pin["id"])
            toml_virtual_pin_table.add("display_name", virtual_pin["display_name"])
            toml_virtual_pin_table.add("ip_address", virtual_pin["ip_adress"])
            toml_virtual_pin_table.add("virtual_pin_method", virtual_pin["virtual_pin_method"])
            toml_virtual_pin_table.add("pins_to_block", virtual_pin["pins_to_block"])
            toml_virtual_pin_table.add("pins_to_unblock", virtual_pin["pins_to_unblock"])

            toml_virtual_pins_array.append(toml_virtual_pin_table)  # type: ignore

        doc = tomlkit.document()

        doc.add("Project", toml_project_table)
        doc.add("InputPins", toml_input_pins_array)
        doc.add("OutputPins", toml_output_pins_array)
        doc.add("VirtualPins", toml_virtual_pins_array)

        return doc


if __name__ == "__main__":
    from pathlib import Path

    # git this file dir
    this_dir = Path(__file__).parent
    parser = ConfigParser(this_dir / "./test_config.toml")
    config = parser.load_config()
    print(config)
