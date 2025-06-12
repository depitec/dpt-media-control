from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pypjlink import Projector  # type: ignore

from .pin import Pin

if TYPE_CHECKING:
    from .output_pin import TriggerContext

type VirtualPinMethodName = Literal["pjlink_power_on", "pjlink_power_off"]


class VirtualPin(Pin):
    _pin_adress: str | None
    _virtual_pin_method_name: VirtualPinMethodName | None

    def __init__(self, name: str):
        super().__init__(name, -1, "virtual")
        self._pin_adress = None
        self._virtual_pin_method_name = None

    # === PROPERTIES ===
    # --- Pin Adress ---
    @property
    def pin_adress(self):
        return self._pin_adress

    # --- Virtual Pin Method Name ---
    @property
    def virtual_pin_method_name(self):
        return self._virtual_pin_method_name

    @virtual_pin_method_name.setter
    def virtual_pin_method_name(self, value: VirtualPinMethodName):
        self._virtual_pin_method_name = value

    # === METHODS ===

    def set_pin_adress(self, pin_adress: str):
        self._pin_adress = pin_adress

    async def after_activate(self, trigger_context: TriggerContext):
        if (self._virtual_pin_method_name is None) or (self._pin_adress is None):
            return

        match self._virtual_pin_method_name:
            case "pjlink_power_on":
                self._trigger_pjlink_power_on(trigger_context)

            case "pjlink_power_off":
                self._trigger_pjlink_power_off(trigger_context)

    # --- Trigger Methods ---
    def _trigger_pjlink_power_on(self, trigger_context: TriggerContext):
        with Projector.from_address(self.pin_adress) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("on")  # type: ignore

    def _trigger_pjlink_power_off(self, trigger_context: TriggerContext):
        with Projector.from_address(self.pin_adress) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("off")  # type: ignore
