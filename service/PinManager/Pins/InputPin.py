from __future__ import annotations
import asyncio

from .Pin import Pin
from typing import Union, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from ..PinManager import TriggerContext
    from .OutputPin import OutputPin
    from .VirtualPin import VirtualPin

type TriggerablePins = Union[OutputPin, VirtualPin]


class InputPin(Pin):
    trigger_pins: list[TriggerablePins]
    trigger_delay: float

    def __init__(
        self,
        name: str,
        gpio_pin: int,
    ):
        super().__init__(name, gpio_pin, "input")
        self.trigger_pins = []
        self.trigger_delay = 0

    def add_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.append(pin)

    def remove_trigger_pin(self, pin: TriggerablePins):
        self.trigger_pins.remove(pin)

    async def on_trigger_start(self, trigger_context: TriggerContext) -> bool:
        if self.trigger_delay > 0:
            await asyncio.sleep(self.trigger_delay)
            return not self.is_triggered

        return False

    async def after_activate(self, trigger_context: TriggerContext):
        activate_time = datetime.timestamp(datetime.now())
        context = (self, activate_time)

        for pin in self.trigger_pins:
            await pin.trigger(context)
