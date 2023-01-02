
from rpi_ws281x import *
from var import *
import time
import logging


# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#Colors:
WHITE = Color(50, 50, 50)
GREEN = Color(0, 50, 0)
BLUE = Color(0, 0, 50)
RED = Color(50, 0, 0)
PURPLE = Color(40, 0, 40)
YELLOW = Color(50, 50, 0)
OFF = Color(0, 0, 0)


class LEDControl(object):

    def __init__(self):
        logging.info("Initializing LED strip")

        self.strip = Adafruit_NeoPixel(TOTAL_NUM_PIXELS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        logging.info("LED strip initialized successfully")

        self.trains = []
        self.stops = []

        self.interrupt = False


    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            if self.interrupt:
                break
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=3):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            if self.interrupt:
                break
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    # For Halloween - spooky lighting
    def fadeRedInAndOut(self, wait_ms=3):
        """Fade a color in and out."""
        for c in range(255):
            newRed = Color(c, 0, 0)
            for i in range(self.strip.numPixels()):
                if self.interrupt:
                    break
                self.strip.setPixelColor(i, newRed)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

        for c in range(255):
            newRed = Color(255 - c, 0, 0)
            for i in range(self.strip.numPixels()):
                if self.interrupt:
                    break
                self.strip.setPixelColor(i, newRed)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def marker(self, i):
        if self.trains.get(i) and len(self.trains.get(i)):
            flags = [False, False]
            for t in self.trains.get(i):
                flags[t.direction] = True
            # Two trains in same stop = RED
            # Two trains in same spot = BLUE
            if flags[0] and flags[1]:
                return RED if self.stops.get(i) else BLUE
            # Train at stop = YELLOW
            # Moving train = GREEN
            elif flags[0]:
                return YELLOW if self.stops.get(i) else BLUE
            else:
                return YELLOW if self.stops.get(i) else GREEN
        if self.stops.get(i):
            return WHITE
        else:
            return OFF

    def party(self):
        logging.debug("Running party cycle")

        self.colorWipe(Color(255, 0, 0))  # Red wipe
        self.colorWipe(Color(0, 255, 0))  # Blue wipe
        self.colorWipe(Color(0, 0, 255))  # Green wipe
        self.rainbowCycle()

    def tick(self, trains, stops):
        self.trains = trains
        self.stops = stops
        colorMap = map(self.marker, range(TOTAL_NUM_PIXELS))
        for i, color in enumerate(colorMap):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def pause(self):
        # Turn off all LEDs
        self.interrupt = True
        for i in range(TOTAL_NUM_PIXELS):
            self.strip.setPixelColor(i, OFF)
            self.strip.show()
        logging.info("Lights out")