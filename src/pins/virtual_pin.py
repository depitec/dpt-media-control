from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pypjlink import Projector  # type: ignore

from .pin import Pin

if TYPE_CHECKING:
    from .output_pin import TriggerContext

type VirtualTriggerMethod = Literal["pjlink_power_on", "pjlink_power_off", "nothing"]


class VirtualPin(Pin):
    _ip_address: str
    _virtual_trigger_method: VirtualTriggerMethod

    def __init__(self, id: str, virtual_gpio_pin: int):
        super().__init__(id, virtual_gpio_pin, "virtual")
        self._ip_address = ""
        self._virtual_trigger_method = "nothing"

    # === PROPERTIES ===
    # --- Pin Adress ---
    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value: str):
        self._ip_address = value

    # --- Virtual Pin Method Name ---
    @property
    def virtual_trigger_method(self):
        return self._virtual_trigger_method

    @virtual_trigger_method.setter
    def virtual_trigger_method(self, value: VirtualTriggerMethod):
        self._virtual_trigger_method = value

    # === METHODS ===

    def set_pin_address(self, pin_address: str):
        self._ip_address = pin_address

    async def after_activate(self, trigger_context: TriggerContext):
        if (self._virtual_trigger_method == "nothing") or (self._ip_address == ""):
            return

        match self._virtual_trigger_method:
            case "pjlink_power_on":
                self._trigger_pjlink_power_on(trigger_context)

            case "pjlink_power_off":
                self._trigger_pjlink_power_off(trigger_context)

    # --- Trigger Methods ---
    def _trigger_pjlink_power_on(self, trigger_context: TriggerContext):
        print("trigger pjlink power on")
        with Projector.from_address(self.ip_address) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("on")  # type: ignore

    def _trigger_pjlink_power_off(self, trigger_context: TriggerContext):
        with Projector.from_address(self.ip_address) as projector:  # type: ignore
            projector.authenticate()  # type: ignore
            projector.set_power("off")  # type: ignore
