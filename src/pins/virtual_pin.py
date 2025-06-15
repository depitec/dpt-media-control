from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from aiopjlink import PJLink  # type: ignore

from .pin import Pin

if TYPE_CHECKING:
    from .output_pin import TriggerContext

type VirtualTriggerMethod = Literal["pjlink_power_on", "pjlink_power_off", "nothing"]


class VirtualPin(Pin):
    _ip_address: str
    _virtual_trigger_method: VirtualTriggerMethod
    _password: str

    def __init__(self, id: str, virtual_gpio_pin: int, password: str = ""):
        super().__init__(id, virtual_gpio_pin, "virtual")
        self._ip_address = ""
        self._virtual_trigger_method = "nothing"
        self._password = password

    # === PROPERTIES ===
    # --- Pin Address ---
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

    # --- Password ---
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    # === METHODS ===

    def set_pin_address(self, pin_address: str):
        self._ip_address = pin_address

    async def after_activate(self, trigger_context: TriggerContext):
        if (self._virtual_trigger_method == "nothing") or (self._ip_address == ""):
            return

        try:
            match self._virtual_trigger_method:
                case "pjlink_power_on":
                    await self._trigger_pjlink_power_on(trigger_context)

                case "pjlink_power_off":
                    await self._trigger_pjlink_power_off(trigger_context)
        except Exception as e:
            print(e)

    # --- Trigger Methods ---
    async def _trigger_pjlink_power_on(self, trigger_context: TriggerContext):
        async with PJLink(address=self.ip_address, password=self.password) as link:  # type: ignore
            await link.power.turn_on()

    async def _trigger_pjlink_power_off(self, trigger_context: TriggerContext):
        async with PJLink(address=self.ip_address, password=self.password) as link:  # type: ignore
            await link.power.turn_off()
