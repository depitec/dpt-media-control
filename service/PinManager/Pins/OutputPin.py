from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Literal
from .Pin import Pin

if TYPE_CHECKING:
    from ..PinManager import TriggerContext

import RPi.GPIO as GPIO

type OutputTriggerMethodName = Literal["pulse", "hold"]
# type OutputTriggerMethodName = Literal["pulse", "hold", "while_input"]


class OutputPin(Pin):
    trigger_method_name: OutputTriggerMethodName
    hold_time: float

    def __init__(
        self,
        name: str,
        gpio_pin: int,
        trigger_type: OutputTriggerMethodName = "pulse",
        hold_time: float = 5,
    ):
        super().__init__(name, gpio_pin, "output")
        self.trigger_method_name = trigger_type
        self.hold_time = hold_time

    async def after_activate(self, trigger_context: TriggerContext):
        match self.trigger_method_name:
            case "pulse":
                await self._trigger_pulse()
            case "hold":
                await self._trigger_hold()
            # case "while_input":
            #     await self._trigger_while_input(trigger_context)

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

    # async def _trigger_while_input(self, trigger_context: TriggerContext):
    #     [trigger_pin, _] = trigger_context

    #     GPIO.output(self._gpio_pin, GPIO.HIGH)

    #     while GPIO.input(trigger_pin.gpio_pin) == GPIO.HIGH:
    #         pass

    #     GPIO.output(self._gpio_pin, GPIO.LOW)
