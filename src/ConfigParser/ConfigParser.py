import tomlkit

from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from PinManager.Pins.InputPin import InputPin
    from PinManager.Pins.OutputPin import OutputPin
    from PinManager.Pins.VirtualPin import VirtualPin

    class ProjectType(TypedDict):
        name: str
        version: str
        description: str
        authors: list[str]

    class ConfigType(TypedDict):
        Project: ProjectType
        InputPins: list[type[InputPin]]
        OutputPins: list[type[OutputPin]]
        VirtualPins: list[type[VirtualPin]]


class ConfigParser:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def read_config(self):
        with open(self.config_file_path, "rb") as f:
            config = tomlkit.load(f)
            return config

    def write_config(self, config):
        with open(self.config_file_path, "w") as f:
            tomlkit.dump(config, f)
