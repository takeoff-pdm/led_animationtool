from time import sleep, time_ns
from rpi_ws281x import Color as StripColor

from animations.animation import Animation


class Strobe(Animation):
    def animate(self, beat: int, step: int):
        # NEEDS COMPLETE RENEWAL!!!!
        # (Reformat old code by using step to determine the current state of the animation)
        pass

        # starting_time = time_ns() // 1_000_000
        # print('Flacka flacka flacka')

        # # Select colors and therefore the amount of blinks
        # colors = self.select_colors(beat)

        # animation_range = range(self.start_led, self.end_led + 1)

        # if self.variation == 0:  # Do all the blinking shortly after each other
        #     for color in colors:
        #         for i in animation_range:
        #             self.set_pixel_color(i, color)

        #         show_strip_request()

        #         sleep(self.sleep_time * (0.2 / len(colors))
        #               - (time_ns() // 1_000_000 - starting_time) / 1_000)  # Wait until blink shuts off

        #         starting_time = time_ns() // 1_000_000

        #         for i in animation_range:
        #             self.set_pixel_color(i, StripColor(0, 0, 0))

        #         show_strip_request()

        #         sleep(self.sleep_time * (0.3 / len(colors))
        #               - (time_ns() // 1_000_000 - starting_time) / 1_000)  # Wait until it's time to blink again

        # elif self.variation == 1:  # Do all the blinking equally distributed
        #     for color in colors:
        #         for i in animation_range:
        #             self.set_pixel_color(i, color)

        #         show_strip_request()

        #         sleep(self.sleep_time / len(colors) * (1/3)
        #               - (time_ns() // 1_000_000 - starting_time) / 1_000)

        #         starting_time = time_ns() // 1_000_000

        #         for i in animation_range:
        #             self.set_pixel_color(i, StripColor(0, 0, 0))

        #         show_strip_request()

        #         sleep(self.sleep_time / len(colors) * (2/3)
        #               - (time_ns() // 1_000_000 - starting_time) / 1_000)

        # color = Color(255, 255, 255)
        # speed = 4
        # random_color = True

        # for x in range(4):
        #     if random_color:
        #         color = wheel((randint(0, 256)) & 255)

        #     for y in range(speed):
        #         for i in range(strip.numPixels()):
        #             if y % 2 == 0 and not (x == 0 and y == 2):
        #                 strip.setPixelColor(i, color)

        #             elif x == 0 and y == 1:
        #                 strip.setPixelColor(i, color)

        #             else:
        #                 strip.setPixelColor(i, 0)

        #         strip.show()
        #         sleep(sleep_time / speed)
