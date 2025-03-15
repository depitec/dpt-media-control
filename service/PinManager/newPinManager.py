# This will be the new Pin Controller/Manager based on asyncio and zmq
# following is just a small but working example of how it can work
import RPi.GPIO as GPIO
import asyncio

# Define the GPIO pins for the buttons
button_pins = [17, 23]  # Example pins

# Set up the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


async def led_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    await asyncio.sleep(0.1)
    GPIO.output(pin, GPIO.LOW)


async def button_monitor(pin, output_pin):
    while True:
        if GPIO.input(pin):
            print(f"Button pressed on channel {pin}")
            await led_on(output_pin)
        await asyncio.sleep(0.1)


async def createTaskLater():
    await asyncio.sleep(5)
    print("Task created later")
    loop = asyncio.get_running_loop()
    task = loop.create_task(button_monitor(23, 24))

    await asyncio.sleep(10)
    print("Cancelling task")
    task.cancel()


def main():
    loop = asyncio.new_event_loop()

    loop.create_task(button_monitor(17, 27))

    loop.create_task(createTaskLater())

    loop.run_forever()


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
