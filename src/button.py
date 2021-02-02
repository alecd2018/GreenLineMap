import time
from gpiozero import Button

button = Button(21)

while True:
    button.wait_for_press()
    print("Pressed")
    button.wait_for_release()
    print("Released")