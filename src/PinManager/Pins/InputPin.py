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
    _pins_to_trigger: list[TriggerablePins]
    _trigger_delay: float

    def __init__(
        self,
        name: str,
        gpio_pin: int,
    ):
        super().__init__(name, gpio_pin, "input")
        self._pins_to_trigger = []
        self._trigger_delay = 0

    # === PROPERTIES ===
    # --- Trigger Pins ---
    @property
    def pins_to_trigger(self):
        return self._pins_to_trigger

    def add_triggered_pin(self, pin: TriggerablePins):
        self._pins_to_trigger.append(pin)

    def remove_triggered_pin(self, pin: TriggerablePins):
        self._pins_to_trigger.remove(pin)

    # --- Trigger Delay ---
    @property
    def trigger_delay(self):
        return self._trigger_delay

    @trigger_delay.setter
    def trigger_delay(self, value: float):
        self._trigger_delay = value

    # === METHODS ===

    async def on_trigger_start(self, trigger_context: TriggerContext) -> bool:
        if self.trigger_delay > 0:
            await asyncio.sleep(self.trigger_delay)
            return not self.is_triggered

        return False

    async def after_activate(self, trigger_context: TriggerContext):
        activate_time = datetime.timestamp(datetime.now())
        context = (self, activate_time)

        loop = asyncio.get_event_loop()
        for pin in self.pins_to_trigger:
            loop.create_task(pin.trigger(context))
