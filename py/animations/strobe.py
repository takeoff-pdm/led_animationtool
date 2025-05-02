from time import sleep, time_ns
from rpi_ws281x import Color as StripColor

from __init__ import ANIMATION_STEPS
from animations.animation import Animation


class Strobe(Animation):
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
        colors = self.select_colors(beat)
        third = round(ANIMATION_STEPS * .33)
        half = round(ANIMATION_STEPS * .5)
        two_third = round(ANIMATION_STEPS * .66)
        half_third = round(ANIMATION_STEPS * .125)

        # Direction is used to determine how often a flash occurs
        if self.direction == 0 or (self.direction == 1 and beat % 2 == 0) or \
           (self.direction == 2 and beat % 4 == 0) or (self.direction == 3 and beat % 8 == 0):
            if self.variation == 0:  # Flash on the beat and turn off after 1/3 of the beat
                if step == 0:
                    # Set the color of the strip to the beat color
                    for index, color in enumerate(colors):
                        animation_range = self.select_range(index, colors)

                        if len(animation_range) == 0:
                            break

                        for i in animation_range:
                            for j in i:
                                self.set_pixel_color(j, color)
                
                elif step == third:
                    # Turn off the strip
                    for i in range(self.start_led, self.end_led + 1):
                        self.set_pixel_color(i, StripColor(0, 0, 0))
            
            elif self.variation == 1:  # Flash twice per beat and each flash turns off after 1/6 of the beat
                if step == 0 or step == half:
                    # Set the color of the strip to the beat color
                    for index, color in enumerate(colors):
                        animation_range = self.select_range(index, colors)

                        if len(animation_range) == 0:
                            break

                        for i in animation_range:
                            for j in i:
                                self.set_pixel_color(j, color)
                
                elif step == half_third or step == round(ANIMATION_STEPS * .66):
                    # Turn off the strip
                    for i in range(self.start_led, self.end_led + 1):
                        self.set_pixel_color(i, StripColor(0, 0, 0))

            elif self.variation == 2:  # Flash three times per beat and each flash turns off after 1/8 of the beat
                if step == 0 or step == third or step == two_third:
                    # Set the color of the strip to the beat color
                    for index, color in enumerate(colors):
                        animation_range = self.select_range(index, colors)

                        if len(animation_range) == 0:
                            break

                        for i in animation_range:
                            for j in i:
                                self.set_pixel_color(j, color)

                elif step == half_third or step == third + half_third or step == two_third + half_third:
                    # Turn off the strip
                    for i in range(self.start_led, self.end_led + 1):
                        self.set_pixel_color(i, StripColor(0, 0, 0))
