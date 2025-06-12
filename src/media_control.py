from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Literal, Tuple, Union, cast, overload

import RPi.GPIO as GPIO

from config import ConfigParser
from pins import InputPin, OutputPin, VirtualPin

if TYPE_CHECKING:
    from .pins import PinType

type PinUnion = InputPin | OutputPin | VirtualPin


type TriggerContext = Tuple[InputPin | VirtualPin, float]  # (pin, timestamp)

# Default config path is $HOME/.config/dpt-media-control/config.toml
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "dpt-media-control" / "config.toml"


class MediaControl:
    prjoct_name: str | Path
    pins: Dict[str, Union[InputPin, VirtualPin, OutputPin]]
    event_loop: asyncio.AbstractEventLoop
    config_parser: ConfigParser

    def __init__(self, project_name: str, config_path: str | Path = DEFAULT_CONFIG_PATH):
        self.prjoct_name = project_name
        self.pins = {}
        self.event_loop = asyncio.new_event_loop()
        self.config_parser = ConfigParser(config_path)

    def has_pin_been_setup(self, pin_number: int):
        # check if the gpio_pin has been setup
        pin_function = GPIO.gpio_function(pin_number)
        return pin_function != GPIO.UNKNOWN

    @overload
    def register_pin(self, pin_number: int, pin_type: Literal["input"]) -> InputPin: ...

    @overload
    def register_pin(self, pin_number: int, pin_type: Literal["output"]) -> OutputPin: ...

    @overload
    def register_pin(self, pin_number: int, pin_type: Literal["virtual"]) -> VirtualPin: ...

    def register_pin(self, pin_number: int, pin_type: PinType) -> InputPin | OutputPin | VirtualPin:
        # if self.has_pin_been_setup(pin_number):
        #     return

        if pin_type == "input":
            print(f"registering input pin {pin_number}")
            GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            input_pin_name = f"I#{pin_number}"
            new_input_pin: InputPin = InputPin(input_pin_name, pin_number)
            self.pins[input_pin_name] = new_input_pin

            self.add_callback_to_eventloop(new_input_pin)

            return new_input_pin

        if pin_type == "output":
            print(f"registering output pin {pin_number}")
            GPIO.setup(pin_number, GPIO.OUT)
            output_pin_name = f"O#{pin_number}"
            new_output_pin: OutputPin = OutputPin(output_pin_name, pin_number)
            self.pins[output_pin_name] = new_output_pin

            return new_output_pin

        if pin_type == "virtual":
            print(f"registering virtual pin {pin_number}")
            virtual_pin_name = f"V#{pin_number}"
            new_virtual_pin: VirtualPin = VirtualPin(virtual_pin_name)
            self.pins[virtual_pin_name] = new_virtual_pin

            return new_virtual_pin

    def unregister_pin(self, pin: InputPin | OutputPin):
        if pin.pin_type == "input":
            del self.pins[pin.id]
            GPIO.cleanup(pin.gpio_pin)

        if pin.pin_type == "output":
            del self.pins[pin.id]
            GPIO.cleanup(pin.gpio_pin)

        if pin.pin_type == "virtual":
            del self.pins[pin.id]

    def get_pin_by_gpio(self, gpio_pin: int) -> InputPin | OutputPin | VirtualPin | None:
        for pin in self.pins.values():
            if pin.gpio_pin == gpio_pin:
                return pin
        return None

    def get_input_pins(self):
        input_pins: list[InputPin] = []
        for pin in self.pins.values():
            if pin.pin_type == "input":
                input_pins.append(cast(InputPin, pin))
        return input_pins

    def get_output_pins(self):
        output_pins: list[OutputPin] = []
        for pin in self.pins.values():
            if pin.pin_type == "output":
                output_pins.append(cast(OutputPin, pin))
        return output_pins

    def get_virtual_pins(self):
        virtual_pins: list[VirtualPin] = []
        for pin in self.pins.values():
            if pin.pin_type == "virtual":
                virtual_pins.append(cast(VirtualPin, pin))
        return virtual_pins

    async def on_input_callback(self, pin: InputPin):
        while True:
            trigger_context = (pin, datetime.timestamp(datetime.now()))
            if GPIO.input(pin.gpio_pin) and not pin.is_triggered:
                pin.is_triggered = True
                print(f"Pin {pin.id} triggered")
                loop = asyncio.get_event_loop()
                loop.create_task(pin.trigger(trigger_context))

            if not GPIO.input(pin.gpio_pin) and pin.is_triggered:
                pin.is_triggered = False
                print(f"Pin {pin.id} released")
                pin.untrigger(trigger_context)

            await asyncio.sleep(0.1)

    def add_callback_to_eventloop(self, pin: InputPin):
        task = self.event_loop.create_task(self.on_input_callback(pin))
        return task

    def start_event_loop(self):
        self.event_loop.run_forever()

    def stop_event_loop(self):
        self.event_loop.stop()


if __name__ == "__main__":
    import RPi.GPIO as GPIO

    try:
        GPIO.setmode(GPIO.BCM)

        controller = MediaControl("dpt-media-control.toml")

        input1 = controller.register_pin(17, "input")
        output1 = controller.register_pin(27, "output")
        input2 = controller.register_pin(23, "input")
        output2 = controller.register_pin(24, "output")

        input1.add_triggered_pin(output1)
        input2.add_triggered_pin(output2)

        output1.hold_time = 3
        output1.trigger_method = "hold"
        output2.trigger_method = "while_input"

        controller.start_event_loop()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        GPIO.cleanup()
