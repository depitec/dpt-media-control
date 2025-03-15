from __future__ import annotations

from pypjlink import Projector

from .Pin import Pin

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .OutputPin import TriggerContext

type VirtualPinMethodName = Literal["pjlink_power_on", "pjlink_power_off"]


class VirtualPin(Pin):
    pin_adress: str
    virtual_pin_method_name: VirtualPinMethodName

    def __init__(
        self,
        name: str,
    ):
        super().__init__(name, -1, "virtual")

    def set_pin_adress(self, pin_adress: str):
        self.pin_adress = pin_adress

    def after_activate(self, trigger_context: TriggerContext):
        match self.virtual_pin_method_name:
            case "pjlink_power_on":
                self._trigger_pjlink_power_on(trigger_context)

            case "pjlink_power_off":
                self._trigger_pjlink_power_off(trigger_context)

    # --- Trigger Methods ---
    def _trigger_pjlink_power_on(self, trigger_context: TriggerContext):
        with Projector.from_address(self.pin_adress) as projector:
            projector.authenticate()
            projector.set_power("on")

    def _trigger_pjlink_power_off(self, trigger_context: TriggerContext):
        with Projector.from_address(self.pin_adress) as projector:
            projector.authenticate()
            projector.set_power("off")
