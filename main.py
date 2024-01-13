from random import randint
from time import sleep
from rpi_ws281x import Adafruit_NeoPixel, Color

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def color_wipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow_flow(strip, sleep_time):
    first_led = int(LED_COUNT / 2)
    second_led = first_led + 1
    color_randomizer = randint(0, 256)

    for x in range(int(LED_COUNT / 2)):
        for i in range(strip.numPixels()):
            # White blind effect
            if i in range(int(LED_COUNT / 2) - int(LED_COUNT / 6) + int(x / 3), int(LED_COUNT / 2) + int(LED_COUNT / 6) + 1 - int(x / 3)):# and x < int(LED_COUNT / 2) * .5:
                strip.setPixelColor(i, Color(255, 255, 255))
            
            # Rainbow flow
            elif i in range(first_led - int(LED_COUNT / 5), first_led + 1):
                strip.setPixelColor(i, wheel((i * 2 + color_randomizer) & 255))
            
            elif i in range(second_led, second_led + int(LED_COUNT / 5) + 1):
                strip.setPixelColor(i, wheel((i * 2 + color_randomizer) & 255))
            
            # Rest
            elif i <= int(LED_COUNT / 2):
                strip.setPixelColor(i, wheel((color_randomizer - 64) & 255))
            
            else:
                strip.setPixelColor(i, wheel((color_randomizer + 64) & 255))

        strip.show()

        first_led -= 1
        second_led += 1

        sleep(sleep_time / int(LED_COUNT / 2))

def shooting_color(strip, sleep_time):
    color = Color(255, 255, 255)
    random_color = True

    if random_color:
        color = wheel((randint(0, 256)) & 255)

    for x in range(int(LED_COUNT)):
        for i in range(strip.numPixels()):
            if i in range(x - int(LED_COUNT * .2), x + 1):
                if i < 0:
                    continue
                
                strip.setPixelColor(i, color)
            
            else:
                strip.setPixelColor(i, 0)

        strip.show()
        sleep(sleep_time / int(LED_COUNT))

def strobo(strip, sleep_time):
    color = Color(255, 255, 255)
    speed = 4
    random_color = True

    for x in range(4):
        if random_color:
            color = wheel((randint(0, 256)) & 255)
        
        for y in range(speed):
            for i in range(strip.numPixels()):
                if y % 2 == 0 and not (x == 0 and y == 2):
                    strip.setPixelColor(i, color)
                
                elif x == 0 and y == 1:
                    strip.setPixelColor(i, color)
                
                else:
                    strip.setPixelColor(i, 0)

            strip.show()
            sleep(sleep_time / speed)

def main():
    # Initialize strip
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Arguments
    bpm = 128
    sleep_time = 60 / bpm

    try:
        while True:
            strobo(strip, sleep_time)

    except KeyboardInterrupt:
        color_wipe(strip, Color(0,0,0))
        return

if __name__ == '__main__':
    main()
