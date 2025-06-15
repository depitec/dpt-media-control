import RPi.GPIO as GPIO

from media_control import MediaControl

GPIO.setmode(GPIO.BCM)
controller = MediaControl("dpt-media-control")

try:
    controller.start_event_loop()

except KeyboardInterrupt:
    controller.stop_event_loop()
    GPIO.cleanup()
