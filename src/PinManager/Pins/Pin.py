from __future__ import annotations

from typing import Literal, TYPE_CHECKING, final

if TYPE_CHECKING:
    from ..PinManager import TriggerContext

type PinState = Literal["active", "inactive", "blocked"]


type PinType = Literal["input", "output", "virtual"]


class Pin:
    _gpio_pin: int
    _pin_type: PinType
    _id: str
    _display_name: str
    _state: PinState
    _is_triggered: bool
    _pins_to_unblock: list[Pin]
    _pins_to_block: list[Pin]

    def __init__(
        self,
        id: str,
        gpio_pin: int,  # fixed value never change
        pin_type: PinType,  # fixed value never change
        is_blocked: bool = False,
        unblock_pins: list[Pin] = [],
        pins_to_block: list[Pin] = [],
    ):
        self._id = id
        self._gpio_pin = gpio_pin
        self._pin_type = pin_type
        self._display_name = id
        self._state = "inactive"
        self._is_triggered = False
        self._pins_to_unblock = unblock_pins
        self._pins_to_block = pins_to_block

        if is_blocked:
            self._state = "blocked"

    # === PROPERTIES ===
    # --- Name ---
    @property
    def id(self):
        return self._id

    # --- GPIO Pin ---
    @property
    def gpio_pin(self):
        return self._gpio_pin

    # --- Pin Type ---
    @property
    def pin_type(self):
        return self._pin_type

    # --- Is Triggered ---
    @property
    def is_triggered(self):
        return self._is_triggered

    @is_triggered.setter
    def is_triggered(self, value: bool):
        self._is_triggered = value

    # --- Is Blocked ---
    @property
    def is_blocked(self):
        return self._state == "blocked"

    # --- Display Name ---
    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value: str):
        self._display_name = value

    # --- State ---
    @property
    def state(self):
        return self._state

    # --- Block/Unblock Pins ---
    @property
    def pins_to_block(self):
        return self._pins_to_block

    @property
    def pins_to_unblock(self):
        return self._pins_to_unblock

    def add_unblock_pin(self, pin: Pin):
        self._pins_to_unblock.append(pin)

    def add_block_pin(self, pin: Pin):
        self._pins_to_block.append(pin)

    def remove_unblock_pin(self, pin: Pin):
        self._pins_to_unblock.remove(pin)

    def remove_block_pin(self, pin: Pin):
        self._pins_to_block.remove(pin)

    # --- Methods ---
    def block_pins(self, pins: list[Pin]):
        for pin in pins:
            pin.block()

    def unblock_pins(self, pins: list[Pin]):
        for pin in pins:
            pin.unblock()

    async def on_trigger_start(self, trigger_context: TriggerContext) -> bool:
        return False

    async def on_trigger_end(self, trigger_context: TriggerContext):
        pass

    async def after_activate(self, trigger_context: TriggerContext):
        pass

    async def before_deactivate(self):
        pass

    @final
    def block(self):
        self._state = "blocked"

    @final
    def unblock(self):
        self._state = "inactive"

    @final
    async def activate(self, context: TriggerContext):
        self._state = "active"

        [trigger_pin, timestamp] = context
        print(f"Pin {self.id} activated. Triggered by {trigger_pin.id} at {timestamp}")
        await self.after_activate(context)

    @final
    async def deactivate(self):
        print(f"Pin {self.id} deactivated")
        self._state = "inactive"

        await self.before_deactivate()

    @final
    def untrigger(self, trigger_context: TriggerContext):
        pass

    @final
    async def trigger(self, trigger_context: TriggerContext):
        if self._state == "active" or self._state == "blocked":
            return
        # Pin got triggered
        stop = await self.on_trigger_start(trigger_context)
        if stop:
            return

        # Block pins that should be blocked
        self.block_pins(self.pins_to_block)
        # Unblock pins that should be unblocked
        self.unblock_pins(self.pins_to_unblock)
        # Activate Pin functionality
        await self.activate(trigger_context)
        # Deactivate Pin functionality
        await self.deactivate()
        # Unblock pins that where blocked
        self.unblock_pins(self.pins_to_block)
        # Block pins that where unblocked
        self.block_pins(self.pins_to_unblock)
        # Pin trigger ended
        await self.on_trigger_end(trigger_context)
