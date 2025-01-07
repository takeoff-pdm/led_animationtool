from time import time_ns, sleep
from rpi_ws281x import Color as StripColor

from __init__ import ANIMATION_STEPS

from animations.animation import Animation


class Squeeze(Animation):
    def select_range(self, index: int, colors: list) -> list:
        animation_range = []

        match self.direction:
            case 0:  # Normal
                animation_range.append(range(int(self.start_led + 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * index),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * (len(colors) - index - 1))))

            case 1:  # Reverse
                animation_range.append(range(int(self.start_led + 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * (len(colors) - index - 1)),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * index)))

            case 2:  # Innter to outer
                animation_range.append(range(int(self.start_led + 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * index),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index - 1)
                                                 - (self.end_led - self.start_led) / 2)))

                animation_range.append(range(int(self.start_led
                                                 + 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index - 1)
                                                 + (self.end_led - self.start_led) / 2),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * index)))

            case 3:  # Outer to inner
                animation_range.append(range(int(self.start_led + 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index - 1)),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * index
                                                 - (self.end_led - self.start_led) / 2)))

                animation_range.append(range(int(self.start_led
                                                 + 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * index
                                                 + (self.end_led - self.start_led) / 2),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index - 1))))

        return animation_range

    def animate(self, beat: int, step: int):
        starting_time = time_ns() // 1_000_000

        match self.direction:
            case 4:  # Normal and reverse
                self.direction = 0

                match (beat % 2):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(0)

                self.direction = 4

                return

            case 5:  # 2x Normal and 2x reverse
                self.direction = 0

                match (beat % 4):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(2)

                    case 2:
                        self.animate(1)

                    case 3:
                        self.animate(0)

                self.direction = 5

                return

            case 6:  # 4x Normal and 4x reverse
                self.direction = 0

                match (beat % 8):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(2)

                    case 2:
                        self.animate(3)

                    case 3:
                        self.animate(4)

                    case 4:
                        self.animate(3)

                    case 5:
                        self.animate(2)

                    case 6:
                        self.animate(1)

                    case 7:
                        self.animate(0)

                self.direction = 6

                return

            case 7:  # 8x Normal and 8x reverse
                self.direction = 0

                match (beat):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(2)

                    case 2:
                        self.animate(3)

                    case 3:
                        self.animate(4)

                    case 4:
                        self.animate(5)

                    case 5:
                        self.animate(6)

                    case 6:
                        self.animate(7)

                    case 7:
                        self.animate(8)

                    case 8:
                        self.animate(7)

                    case 9:
                        self.animate(6)

                    case 10:
                        self.animate(5)

                    case 11:
                        self.animate(4)

                    case 12:
                        self.animate(3)

                    case 13:
                        self.animate(2)

                    case 14:
                        self.animate(1)

                    case 15:
                        self.animate(0)

                self.direction = 7

                return

        # Split strip up into slices for the different sections
        colors = self.select_colors(beat)

        if self.variation == 0:
            for index, color in enumerate(colors):
                animation_range = self.select_range(index, colors)

                if len(animation_range) == 0:
                    break

                for i in animation_range:
                    for j in i:
                        self.set_pixel_color(j, color)

            # step = 2 if (self.end_led - self.start_led) + 1 > 120 \
            #     else 3 if (self.end_led - self.start_led) + 1 > 240 \
            #     else 4 if (self.end_led - self.start_led) + 1 > 360 \
            #     else 5 if (self.end_led - self.start_led) + 1 > 480 \
            #     else 6 if (self.end_led - self.start_led) + 1 > 600 \
            #     else 1  # Avoid having too slow code by skipping some pixels

            # sleep_time = self.sleep_time / ANIMATION_STEPS \
            #              - ((time_ns() // 1_000_000 - starting_time) / 1_000)

            # if sleep_time > 0:
            #     sleep(sleep_time)

            # starting_time = time_ns() // 1_000_000

            reduce_per_step = (self.end_led - self.start_led) / ANIMATION_STEPS
            original_start_led = self.start_led
            original_end_led = self.end_led

            match self.direction:
                case 0:  # Normal -> Only reduce the end_led
                    self.end_led = int(original_end_led - reduce_per_step * step)

                case 1:  # Reverse -> Only reduce the start_led
                    self.start_led = int(original_start_led + reduce_per_step * step)

                case 2:  # Inner to outer -> Reduce both start_led and end_led
                    self.start_led = int(original_start_led + reduce_per_step * step)
                    self.end_led = int(original_end_led - reduce_per_step * step)

                case 3:  # ? Reduce from middle
                    pass

            # Set the colors
            for index, color in enumerate(colors):
                animation_range = self.select_range(index, colors)

                if len(animation_range) == 0:
                    break

                for i in animation_range:
                    for j in i:
                        self.set_pixel_color(j, color)

            # Remove old colors
            if self.direction != 3:
                if self.direction != 0:
                    for i in range(original_start_led, self.start_led):
                        self.set_pixel_color(i, StripColor(0, 0, 0))

                if self.direction != 1:
                    for i in range(self.end_led + 1, original_end_led + 1):
                        self.set_pixel_color(i, StripColor(0, 0, 0))

            if step >= ANIMATION_STEPS:
                self.start_led = original_start_led
                self.end_led = original_end_led

            # sleep_time = self.sleep_time / ANIMATION_STEPS * step \
            #                 - ((time_ns() // 1_000_000 - starting_time) / 1_000)

            # if sleep_time > 0:
            #     sleep(sleep_time)

            # starting_time = time_ns() // 1_000_000

        elif self.variation == 1:  # Do not squeeze, but just blackout more and more
            pass  # TODO: Add this when first variation is tested!
