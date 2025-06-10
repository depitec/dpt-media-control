from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Union

from .Pin import Pin

if TYPE_CHECKING:
    from ..PinManager import TriggerContext
    from .OutputPin import OutputPin
    from .VirtualPin import VirtualPin

type TriggerablePins = Union[OutputPin, VirtualPin]


class InputPin(Pin):
    _pins_to_trigger: list[TriggerablePins]
    _activation_delay: float

    def __init__(self, name: str, gpio_pin: int):
        super().__init__(name, gpio_pin, "input")
        self._pins_to_trigger = []
        self._activation_delay = 0

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
    def activation_delay(self):
        return self._activation_delay

    @activation_delay.setter
    def activation_delay(self, value: float):
        self._activation_delay = value

    # === METHODS ===

    async def on_trigger_start(self, trigger_context: TriggerContext) -> bool:
        if self.activation_delay > 0:
            await asyncio.sleep(self.activation_delay)

        return False

    async def after_activate(self, trigger_context: TriggerContext):
        activate_time = datetime.timestamp(datetime.now())
        context = (self, activate_time)

        loop = asyncio.get_event_loop()
        for pin in self.pins_to_trigger:
            loop.create_task(pin.trigger(context))
