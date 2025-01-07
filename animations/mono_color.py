from time import time_ns, sleep
from rpi_ws281x import Color as StripColor

from __init__ import ANIMATION_STEPS

from animations.animation import Animation


class MonoColor(Animation):
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

    def animate(self, beat: int, step: int, reverse: bool = False):
        match self.direction:
            case 4:  # Normal and reverse
                self.direction = 0

                match (beat % 2):
                    case 0:
                        self.animate(1, reverse=True)

                    case 1:
                        self.animate(0)

                self.direction = 4

                return

            case 5:  # 2x Normal and 2x reverse
                self.direction = 0

                match (beat % 4):
                    case 0:
                        self.animate(1, step)

                    case 1:
                        self.animate(2, step, reverse=True)

                    case 2:
                        self.animate(1, step, reverse=True)

                    case 3:
                        self.animate(0, step)

                self.direction = 5

                return

            case 6:  # 4x Normal and 4x reverse
                self.direction = 0

                match (beat % 8):
                    case 0:
                        self.animate(1, step)

                    case 1:
                        self.animate(2, step)

                    case 2:
                        self.animate(3, step)

                    case 3:
                        self.animate(4, step, reverse=True)

                    case 4:
                        self.animate(3, step, reverse=True)

                    case 5:
                        self.animate(2, step, reverse=True)

                    case 6:
                        self.animate(1, step, reverse=True)

                    case 7:
                        self.animate(0, step)

                self.direction = 6

                return

            case 7:  # 8x Normal and 8x reverse
                self.direction = 0

                match (beat):
                    case 0:
                        self.animate(1, step)

                    case 1:
                        self.animate(2, step)

                    case 2:
                        self.animate(3, step)

                    case 3:
                        self.animate(4, step)

                    case 4:
                        self.animate(5, step)

                    case 5:
                        self.animate(6, step)

                    case 6:
                        self.animate(7, step)

                    case 7:
                        self.animate(8, step, reverse=True)

                    case 8:
                        self.animate(7, step, reverse=True)

                    case 9:
                        self.animate(6, step, reverse=True)

                    case 10:
                        self.animate(5, step, reverse=True)

                    case 11:
                        self.animate(4, step, reverse=True)

                    case 12:
                        self.animate(3, step, reverse=True)

                    case 13:
                        self.animate(2, step, reverse=True)

                    case 14:
                        self.animate(1, step, reverse=True)

                    case 15:
                        self.animate(0, step)

                self.direction = 7

                return

        # Split strip up into slices for the different sections
        colors = self.select_colors(beat)

        if self.variation == 0:  # No transition color change
            for index, color in enumerate(colors):
                animation_range = self.select_range(index, colors)

                if len(animation_range) == 0:
                    break

                for i in animation_range:
                    for j in i:
                        self.set_pixel_color(j, color)


        elif self.variation == 1:  # Soft transition color change
            next_colors = self.select_colors(beat + 1 if beat < 16 else 0)

            if reverse == True:
                next_colors = self.select_colors(beat - 1 if beat > 0 else 15)

            red_transitions = []
            green_transitions = []
            blue_transitions = []

            for color, next_color in zip(colors, next_colors):
                red_transitions.append(self.color_transition(color.r, next_color.r))
                green_transitions.append(self.color_transition(color.g, next_color.g))
                blue_transitions.append(self.color_transition(color.b, next_color.b))

            # step = 2 if (self.end_led - self.start_led) + 1 > 120 \
            #     else 3 if (self.end_led - self.start_led) + 1 > 240 \
            #     else 4 if (self.end_led - self.start_led) + 1 > 360 \
            #     else 5 if (self.end_led - self.start_led) + 1 > 480 \
            #     else 6 if (self.end_led - self.start_led) + 1 > 600 \
            #     else 1  # Avoid having too slow code by skipping some pixels

            # The number of transitions until next color is reached 
            # (Wait half the time to still show this color)
            # for x in range(0, ANIMATION_STEPS * 2, step):
            if step == 0:  # Show current/initial color
                self.variation = 0
                self.animate(beat, step)
                self.variation = 1

            if step * 2 > ANIMATION_STEPS:  # Transition to next color, when half the time has passed
                for index, (red_transition, green_transition, blue_transition) \
                        in enumerate(zip(red_transitions, green_transitions, blue_transitions)):

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

                    animation_range = self.select_range(index, colors)

                    if len(animation_range) == 0:
                        break

                    for i in animation_range:
                        for j in i:
                            self.set_pixel_color(j, StripColor(red, green, blue))

                # sleep_time = self.sleep_time / (ANIMATION_STEPS * 2) * step \
                #              - ((time_ns() // 1_000_000 - starting_time) / 1_000)

                # if sleep_time > 0:
                #     sleep(sleep_time)

                # starting_time = time_ns() // 1_000_000
