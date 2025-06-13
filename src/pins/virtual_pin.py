from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pypjlink import Projector  # type: ignore

from .pin import Pin

if TYPE_CHECKING:
    from .output_pin import TriggerContext

type VirtualPinMethod = Literal["pjlink_power_on", "pjlink_power_off"]


class VirtualPin(Pin):
    _ip_adress: str | None
    _virtual_pin_method: VirtualPinMethod | None

    def __init__(self, id: str, virtual_gpio_pin: int):
        super().__init__(id, virtual_gpio_pin, "virtual")
        self._ip_adress = None
        self._virtual_pin_method = None

    # === PROPERTIES ===
    # --- Pin Adress ---
    @property
    def ip_adress(self):
        return self._ip_adress

    @ip_adress.setter
    def ip_adress(self, value: str):
        self._ip_adress = value

    # --- Virtual Pin Method Name ---
    @property
    def virtual_pin_method(self):
        return self._virtual_pin_method

    @virtual_pin_method.setter
    def virtual_pin_method(self, value: VirtualPinMethod):
        self._virtual_pin_method = value

    # === METHODS ===

    def set_pin_adress(self, pin_adress: str):
        self._ip_adress = pin_adress

    async def after_activate(self, trigger_context: TriggerContext):
        if (self._virtual_pin_method is None) or (self._ip_adress is None):
            return

        match self._virtual_pin_method:
            case "pjlink_power_on":
                self._trigger_pjlink_power_on(trigger_context)

            case "pjlink_power_off":
                self._trigger_pjlink_power_off(trigger_context)

    # --- Trigger Methods ---
    def _trigger_pjlink_power_on(self, trigger_context: TriggerContext):
        with Projector.from_address(self.ip_adress) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("on")  # type: ignore

    def _trigger_pjlink_power_off(self, trigger_context: TriggerContext):
        with Projector.from_address(self.ip_adress) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("off")  # type: ignore
