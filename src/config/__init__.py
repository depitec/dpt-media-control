from typing import TYPE_CHECKING

from .config_parser import ConfigParser as ConfigParser

if TYPE_CHECKING:
    from .config_parser import Config as Config
    from .config_parser import InputPinConfig as InputPinConfig
    from .config_parser import OutputPinConfig as OutputPinConfig
    from .config_parser import VirtualPinConfig as VirtualPinConfig
