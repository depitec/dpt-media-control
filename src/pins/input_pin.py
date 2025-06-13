from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Union

from .pin import Pin

if TYPE_CHECKING:
    from ..media_control import TriggerContext
    from .output_pin import OutputPin
    from .virtual_pin import VirtualPin

type TriggerablePins = Union[OutputPin, VirtualPin]


class InputPin(Pin):
    _triggered_pins: list[TriggerablePins]
    _activation_delay: float

    def __init__(self, id: str, gpio_pin: int):
        super().__init__(id, gpio_pin, "input")
        self._triggered_pins = []
        self._activation_delay = 0

    # === PROPERTIES ===
    # --- Trigger Pins ---
    @property
    def triggered_pins(self):
        return self._triggered_pins

    def add_triggered_pin(self, pin: TriggerablePins):
        self._triggered_pins.append(pin)

    def remove_triggered_pin(self, pin: TriggerablePins):
        self._triggered_pins.remove(pin)

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
        for pin in self.triggered_pins:
            loop.create_task(pin.trigger(context))
