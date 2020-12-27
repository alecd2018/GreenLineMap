TOTAL_LED_COUNT = 300
LED_CHIP_NUMBER = 3
R = 0
G = 162
B = 255

from rpi_ws281x import *
strip = PixelStrip(TOTAL_LED_COUNT, 18, 800000, 5, False, 255)
strip.begin()
strip.setPixelColorRGB(LED_CHIP_NUMBER, R, G, B)
strip.show()
