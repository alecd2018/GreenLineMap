
from rpi_ws281x import *
from var import *


# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#Colors:
WHITE = Color(255, 255, 255)
GREEN = Color(0, 200, 110)
YELLOW = Color(0, 0, 0)
BLANK = COLOR(0, 0, 0)

class LEDControl(object):

    def __init__(self):
        self.strip = Adafruit_NeoPixel(TOTAL_NUM_PIXELS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

        self.strip.begin()

    def marker(self, i):
        if self.trains.get(i) and len(self.trains.get(i)):
            flags = [False, False]
            for t in self.trains.get(i):
                flags[t.direction] = True
            if flags[0] and flags[1]:
                return RED if self.stops.get(i) else BLUE
            elif flags[0]:
                return YELLOW if self.stops.get(i) else WHITE
            else:
                return YELLOW if self.stops.get(i) else WHITE
        if self.stops.get(i):
            return GREEN
        else:
            return GREEN

    def tick(self):
        colorMap = map(self.marker, range(TOTAL_NUM_PIXELS))
        for i, color in enumerate(colorMap):
            self.strip.setPixelColor(i, color)

    def pause(self):
    # Turn off all LEDs
        for i in range(strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
    