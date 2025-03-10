from __future__ import annotations
from datetime import datetime
from typing import Dict, Literal, Union, TYPE_CHECKING, cast, Tuple, overload
import RPi.GPIO as GPIO
from .Pins import InputPin, OutputPin, VirtualPin

if TYPE_CHECKING:
    from .Pins import PinType

type PinUnion = InputPin | OutputPin | VirtualPin


type TriggerContext = Tuple[InputPin | VirtualPin, float]  # (pin, timestamp)


class PinManager:
    pins: Dict[str, Union[InputPin, VirtualPin, OutputPin]]

    def __init__(self):
        self.pins = {}

    def has_pin_been_setup(self, pin_number: int):
        # check if the gpio_pin has been setup
        pin_function = GPIO.gpio_function(pin_number)
        return pin_function != GPIO.UNKNOWN

    @overload
    def register_pin(self, pin_number: int, pin_type: Literal["input"]) -> InputPin: ...

    @overload
    def register_pin(
        self, pin_number: int, pin_type: Literal["output"]
    ) -> OutputPin: ...

    @overload
    def register_pin(
        self, pin_number: int, pin_type: Literal["virtual"]
    ) -> VirtualPin: ...

    def register_pin(
        self, pin_number: int, pin_type: PinType
    ) -> InputPin | OutputPin | VirtualPin:
        # if self.has_pin_been_setup(pin_number):
        #     return

        if pin_type == "input":
            print(f"registering input pin {pin_number}")
            GPIO.setup(pin_number, GPIO.IN)
            input_pin_name = f"I#{pin_number}"
            new_input_pin: InputPin = InputPin(input_pin_name, pin_number)
            self.pins[input_pin_name] = new_input_pin
            GPIO.add_event_detect(
                pin_number,
                GPIO.RISING,
                callback=self.event_trigger(new_input_pin),
                bouncetime=200,
            )

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
            del self.pins[pin.name]
            GPIO.cleanup(pin._gpio_pin)
            GPIO.remove_event_detect(pin._gpio_pin)

        if pin.pin_type == "output":
            del self.pins[pin.name]
            GPIO.cleanup(pin._gpio_pin)

        if pin.pin_type == "virtual":
            del self.pins[pin.name]

    def get_input_pins(self):
        input_pins = []
        for pin in self.pins.values():
            if pin.pin_type == "input":
                input_pins.append(pin)
        return cast(list[InputPin], input_pins)

    def get_output_pins(self):
        output_pins = []
        for pin in self.pins.values():
            if pin.pin_type == "output":
                output_pins.append(pin)
        return cast(list[OutputPin], output_pins)

    def get_virtual_pins(self):
        virtual_pins = []
        for pin in self.pins.values():
            if pin.pin_type == "virtual":
                virtual_pins.append(pin)
        return cast(list[VirtualPin], virtual_pins)

    def event_trigger(self, pin: InputPin):
        def callback(channel):
            if channel != pin._gpio_pin:
                print(
                    f"Channel mismatch (Channel:{channel} != PinGPIO:{pin._gpio_pin}), need to investigate. Still triggering."
                )
            pin.trigger((pin, datetime.timestamp(datetime.now())))

        return callback
