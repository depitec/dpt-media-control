from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Literal

from .pin import Pin

if TYPE_CHECKING:
    from ..media_control import TriggerContext

import RPi.GPIO as GPIO

# type OutputTriggerMethodName = Literal["pulse", "hold"]
type OutputTriggerMethods = Literal["pulse", "hold", "while_input"]


class OutputPin(Pin):
    _trigger_method: OutputTriggerMethods
    _hold_time: float

    def __init__(self, id: str, gpio_pin: int, trigger_type: OutputTriggerMethods = "pulse", hold_time: float = 5):
        super().__init__(id, gpio_pin, "output")
        self._trigger_method = trigger_type
        self._hold_time = hold_time

    # === PROPERTIES ===
    # --- Trigger Method Name ---
    @property
    def trigger_method(self):
        return self._trigger_method

    @trigger_method.setter
    def trigger_method(self, value: OutputTriggerMethods):
        self._trigger_method = value

    # --- Hold Time ---
    @property
    def hold_time(self):
        return self._hold_time

    @hold_time.setter
    def hold_time(self, value: float):
        self._hold_time = value

    # === METHODS ===

    async def after_activate(self, trigger_context: TriggerContext):
        match self._trigger_method:
            case "pulse":
                await self._trigger_pulse()
            case "hold":
                await self._trigger_hold()
            case "while_input":
                await self._trigger_while_input(trigger_context)

    async def before_deactivate(self):
        GPIO.output(self._gpio_pin, GPIO.LOW)

    # --- Trigger Methods ---

    async def _trigger_pulse(self):
        # pulse all trigger pins
        GPIO.output(self._gpio_pin, GPIO.HIGH)
        await asyncio.sleep(0.1)
        GPIO.output(self._gpio_pin, GPIO.LOW)

    async def _trigger_hold(self):
        # hold all trigger pins
        GPIO.output(self._gpio_pin, GPIO.HIGH)
        await asyncio.sleep(self.hold_time)
        GPIO.output(self._gpio_pin, GPIO.LOW)

    async def _trigger_while_input(self, trigger_context: TriggerContext):
        GPIO.output(self._gpio_pin, GPIO.HIGH)
        while True:
            if not trigger_context[0].is_triggered:
                break

            await asyncio.sleep(0.2)

        GPIO.output(self._gpio_pin, GPIO.LOW)
