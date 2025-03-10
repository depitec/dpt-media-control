from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from ..PinManager import TriggerContext

type PinState = Literal["active", "inactive"]


type PinType = Literal["input", "output", "virtual"]


class Pin:
    _gpio_pin: int
    _pin_type: PinType
    _name: str
    display_name: str
    state: PinState
    is_triggered: bool
    is_blocked: bool
    pins_to_unblock: list[type[Pin]]
    pins_to_block: list[type[Pin]]
    trigger_delay: float

    def __init__(
        self,
        name: str,
        gpio_pin: int,  # fixed value never change
        pin_type: PinType,  # fixed value never change
        is_blocked: bool = False,
        unblock_pins: list[type[Pin]] = [],
        pins_to_block: list[type[Pin]] = [],
        trigger_delay: float = 0,
    ):
        self._name = name
        self._gpio_pin = gpio_pin
        self._pin_type = pin_type
        self.display_name = name
        self.state = "inactive"
        self.is_triggered = False
        self.is_blocked = is_blocked
        self.pins_to_unblock = unblock_pins
        self.pins_to_block = pins_to_block
        self.trigger_delay = trigger_delay

    @property
    def name(self):
        return self._name

    @property
    def gpio_pin(self):
        return self._gpio_pin

    @property
    def pin_type(self):
        return self._pin_type

    def set_display_name(self, display_name: str):
        self.display_name = display_name

    # TODO: add @property and @setter for unblock_pins, block_pins + validation
    def add_unblock_pin(self, pin: type[Pin]):
        self.pins_to_unblock.append(pin)

    def add_block_pin(self, pin: type[Pin]):
        self.pins_to_block.append(pin)

    def remove_unblock_pin(self, pin: type[Pin]):
        self.pins_to_unblock.remove(pin)

    def remove_block_pin(self, pin: type[Pin]):
        self.pins_to_block.remove(pin)

    def block_pins(self, pins: list[type[Pin]]):
        for pin in pins:
            pin.is_blocked = True

    def unblock_pins(self, pins: list[type[Pin]]):
        for pin in pins:
            pin.is_blocked = False

    def trigger_start(self):
        self.is_triggered = True

    def trigger_end(self):
        self.is_triggered = False

    def activate(self, context: TriggerContext):
        self.state = "active"

        [trigger_pin, timestamp] = context
        print(
            f"Pin {self.name} activated. Triggered by {trigger_pin.name} at {timestamp}"
        )

    def deactivate(self):
        self.state = "inactive"

    def trigger(self, trigger_context: TriggerContext):
        # Pin got triggered
        self.trigger_start()
        # Check if pin is blocked and return if it is
        if self.is_blocked:
            return
        # Block pins that should be blocked
        self.block_pins(self.pins_to_block)
        # Unblock pins that should be unblocked
        self.unblock_pins(self.pins_to_unblock)
        # Activate Pin functionality
        self.activate(trigger_context)
        # Deactivate Pin functionality
        self.deactivate()
        # Unblock pins that where blocked
        self.unblock_pins(self.pins_to_block)
        # Block pins that where unblocked
        self.block_pins(self.pins_to_unblock)
        # Pin trigger ended
        self.trigger_end()
