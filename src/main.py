import threading
from PinManager import PinManager
import RPi.GPIO as GPIO

import asyncio


async def thread_name():
    while True:
        print(f"thread name: {threading.current_thread().name}")
        await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)

        pin_manager = PinManager()

        input1 = pin_manager.register_pin(17, "input")
        output1 = pin_manager.register_pin(27, "output")
        input2 = pin_manager.register_pin(23, "input")
        output2 = pin_manager.register_pin(24, "output")

        input1.add_trigger_pin(output1)
        input2.add_trigger_pin(output2)

        output1.hold_time = 3
        output1.trigger_method_name = "hold"
        output2.trigger_method_name = "while_input"

        pin_manager.start_event_loop()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        GPIO.cleanup()
