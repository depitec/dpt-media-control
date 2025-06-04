from typing import Union
from .Pin import PinState as PinState
from .Pin import PinType as PinType
from .Pin import Pin as Pin
from .InputPin import InputPin as InputPin
from .OutputPin import OutputPin as OutputPin
from .VirtualPin import VirtualPin as VirtualPin

type PinUnion = Union[InputPin, OutputPin, VirtualPin]
