from typing import Union

from .input_pin import InputPin as InputPin
from .output_pin import OutputPin as OutputPin
from .output_pin import OutputTriggerMethods as OutputTriggerMethods
from .pin import Pin as Pin
from .pin import PinState as PinState
from .pin import PinType as PinType
from .virtual_pin import VirtualPin as VirtualPin
from .virtual_pin import VirtualTriggerMethod as VirtualTriggerMethod

type PinUnion = Union[InputPin, OutputPin, VirtualPin]
