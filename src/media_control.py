from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Literal, Tuple, Union, cast, overload

import RPi.GPIO as GPIO

from config import Config, ConfigParser, InputPinConfig, OutputPinConfig, VirtualPinConfig
from pins import InputPin, OutputPin, VirtualPin

if TYPE_CHECKING:
    from pins import PinType

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

        # load config and see if it contains values
        config: Config = self.config_parser.load_config()
        if len(config.keys()) > 0:
            self.apply_config(config)

    def has_pin_been_setup(self, pin_number: int):
        # check if the gpio_pin has been setup
        pin_function = GPIO.gpio_function(pin_number)
        return pin_function != GPIO.UNKNOWN

    @overload
    def register_pin(self, pin_type: Literal["input"], gpio_pin: int, display_name: str | None = None) -> InputPin: ...

    @overload
    def register_pin(
        self, pin_type: Literal["output"], gpio_pin: int, display_name: str | None = None
    ) -> OutputPin: ...

    @overload
    def register_pin(
        self, pin_type: Literal["virtual"], gpio_pin: int, display_name: str | None = None
    ) -> VirtualPin: ...

    def register_pin(
        self, pin_type: PinType, gpio_pin: int, display_name: str | None = None
    ) -> InputPin | OutputPin | VirtualPin:
        # if self.has_pin_been_setup(pin_number):
        #     return

        if pin_type == "input":
            print(f"registering input pin {gpio_pin}")
            GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            input_pin_id = f"I#{gpio_pin}"
            new_input_pin: InputPin = InputPin(input_pin_id, gpio_pin)
            new_input_pin.display_name = display_name if display_name else input_pin_id
            self.pins[input_pin_id] = new_input_pin

            self.add_callback_to_eventloop(new_input_pin)

            return new_input_pin

        if pin_type == "output":
            print(f"registering output pin {gpio_pin}")
            GPIO.setup(gpio_pin, GPIO.OUT)
            output_pin_id = f"O#{gpio_pin}"
            new_output_pin: OutputPin = OutputPin(output_pin_id, gpio_pin)
            new_output_pin.display_name = display_name if display_name else output_pin_id

            self.pins[output_pin_id] = new_output_pin

            return new_output_pin

        if pin_type == "virtual":
            if gpio_pin > 0:
                raise ValueError("virtual pin must be negative")

            print("registering virtual pin")
            virtual_pin_name = f"V#{abs(gpio_pin)}"
            new_virtual_pin: VirtualPin = VirtualPin(virtual_pin_name, gpio_pin)
            new_virtual_pin.display_name = display_name if display_name else virtual_pin_name

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

    def get_pin_by_id(self, pin_id: str) -> InputPin | OutputPin | VirtualPin | None:
        return self.pins.get(pin_id)

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

    def apply_config(self, config: Config):
        pass


if __name__ == "__main__":
    # get args from command line
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config file", default="dpt-media-control.toml")

    parser.add_argument("--no-rpi", help="try running without RPi.GPIO", action="store_true")

    args = parser.parse_args()
    config_file_path = args.config
    no_rpi = args.no_rpi

    import RPi.GPIO as GPIO

    try:
        if not no_rpi:
            GPIO.setmode(GPIO.BCM)

        controller = MediaControl("dpt-media-control.toml")

        if not no_rpi:
            input1 = controller.register_pin("input", 17)
            output1 = controller.register_pin("output", 27)
            input2 = controller.register_pin("input", 23)
            output2 = controller.register_pin("output", 24)

            input1.add_triggered_pin(output1)
            input2.add_triggered_pin(output2)

            output1.hold_time = 3
            output1.trigger_method = "hold"
            output2.trigger_method = "while_input"

        controller.start_event_loop()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        if not no_rpi:
            GPIO.cleanup()
