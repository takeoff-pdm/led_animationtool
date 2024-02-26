from time import time_ns, sleep
from rpi_ws281x import Color as StripColor

from __init__ import ANIMATION_STEPS

from animations.animation import Animation


class MonoColor(Animation):
    def select_range(self, index: int, colors: list) -> list:
        animation_range = []

        match self.direction:
            case 0:
                animation_range.append(range(int(self.start_led + 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * index),
                                             int(self.end_led + 1
                                                 - 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * (len(colors) - index - 1))))

            case 1:
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

    def animate(self, beat: int, reverse: bool = False):
        # Split strip up into slices for the different sections
        colors = self.select_colors(beat)

        match self.direction:
            case 4:
                self.direction = 0

                match (beat % 2):
                    case 0:
                        self.animate(1, reverse=True)

                    case 1:
                        self.animate(0)

                self.direction = 4

                return

            case 5:
                self.direction = 0

                match (beat % 4):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(2, reverse=True)

                    case 2:
                        self.animate(1, reverse=True)

                    case 3:
                        self.animate(0)

                self.direction = 5

                return

            case 6:
                self.direction = 0

                match (beat % 8):
                    case 0:
                        self.animate(1)

                    case 1:
                        self.animate(2)

                    case 2:
                        self.animate(3)

                    case 3:
                        self.animate(4, reverse=True)

                    case 4:
                        self.animate(3, reverse=True)

                    case 5:
                        self.animate(2, reverse=True)

                    case 6:
                        self.animate(1, reverse=True)

                    case 7:
                        self.animate(0)

                self.direction = 6

                return

            case 7:
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
                        self.animate(8, reverse=True)

                    case 8:
                        self.animate(7, reverse=True)

                    case 9:
                        self.animate(6, reverse=True)

                    case 10:
                        self.animate(5, reverse=True)

                    case 11:
                        self.animate(4, reverse=True)

                    case 12:
                        self.animate(3, reverse=True)

                    case 13:
                        self.animate(2, reverse=True)

                    case 14:
                        self.animate(1, reverse=True)

                    case 15:
                        self.animate(0)

                self.direction = 7

                return

        if self.variation == 0:  # No transition color change
            for index, color in enumerate(colors):
                animation_range = self.select_range(index, colors)

                if len(animation_range) == 0:
                    break

                for i in animation_range:
                    for j in i:
                        self.strip.setPixelColor(j, color)

            self.strip.show()

        elif self.variation == 1:  # Soft transition color change
            starting_time = time_ns() // 1_000_000
            next_colors = self.select_colors(beat + 1 if beat < 16 else 0)

            if reverse == True:
                next_colors = self.select_colors(beat - 1 if beat > 0 else 15)

            red_transitions = []
            green_transitions = []
            blue_transitions = []

            for color, next_color in zip(colors, next_colors):
                if color.r < next_color.r:
                    red_transitions.append(list(range(color.r, next_color.r,
                                                      (next_color.r - color.r) // ANIMATION_STEPS
                                                      if (next_color.r - color.r) // ANIMATION_STEPS != 0
                                                      else 1)))
                else:
                    red_transitions.append(list(reversed(range(next_color.r, color.r,
                                                               (color.r - next_color.r) // ANIMATION_STEPS
                                                               if (color.r - next_color.r) // ANIMATION_STEPS != 0
                                                               else 1))))

                if color.g < next_color.g:
                    green_transitions.append(list(range(color.g, next_color.g,
                                                        (next_color.g - color.g) // ANIMATION_STEPS
                                                        if (next_color.g - color.g) // ANIMATION_STEPS != 0
                                                        else 1)))
                else:
                    green_transitions.append(list(reversed(range(next_color.g, color.g,
                                                                 (color.g - next_color.g) // ANIMATION_STEPS
                                                                 if (color.g - next_color.g) // ANIMATION_STEPS != 0
                                                                 else 1))))

                if color.b < next_color.b:
                    blue_transitions.append(list(range(color.b, next_color.b,
                                                       (next_color.b - color.b) // ANIMATION_STEPS
                                                       if (next_color.b - color.b) // ANIMATION_STEPS != 0
                                                       else 1)))
                else:
                    blue_transitions.append(list(reversed(range(next_color.b, color.b,
                                                                (color.b - next_color.b) // ANIMATION_STEPS
                                                                if (color.b - next_color.b) // ANIMATION_STEPS != 0
                                                                else 1))))

            # The number of transitions until next color is reached 
            # (Wait half the time to still show this color)
            for x in range(ANIMATION_STEPS * 2):
                if x == 0:  # Show current/initial color
                    self.variation = 0
                    self.animate(beat)
                    self.variation = 1

                if x < ANIMATION_STEPS:
                    continue

                for index, (red_transition, green_transition, blue_transition) \
                        in enumerate(zip(red_transitions, green_transitions, blue_transitions)):
                    animation_range = self.select_range(index, colors)

                    if len(animation_range) == 0:
                        break

                    for i in animation_range:
                        for j in i:
                            red = red_transition[x - ANIMATION_STEPS] \
                                if len(red_transition) > x - ANIMATION_STEPS \
                                else red_transition[len(red_transition) - 1] \
                                if len(red_transition) > 0 else colors[index].r

                            green = green_transition[x - ANIMATION_STEPS] \
                                if len(green_transition) > x - ANIMATION_STEPS \
                                else green_transition[len(green_transition) - 1] \
                                if len(green_transition) > 0 else colors[index].g

                            blue = blue_transition[x - ANIMATION_STEPS] \
                                if len(blue_transition) > x - ANIMATION_STEPS \
                                else blue_transition[len(blue_transition) - 1] \
                                if len(blue_transition) > 0 else colors[index].b

                            self.strip.setPixelColor(j, StripColor(red, green, blue))

                self.strip.show()

                sleep(self.sleep_time / (ANIMATION_STEPS * 2) - ((time_ns() // 1_000_000 - starting_time) // 1_000))
                starting_time = time_ns() // 1_000_000
