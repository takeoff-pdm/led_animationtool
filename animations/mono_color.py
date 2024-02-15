from time import time_ns, sleep
from rpi_ws281x import Color as StripColor

from __init__ import ANIMATION_STEPS

from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class MonoColor(Animation):
    def animate(self, beat: int):
        if self.variation == 0:
            colors = self.select_colors(beat)

            for index, color in enumerate(colors):
                # Split strip up into slices for the different colors
                if self.direction == 0:
                    for i in range(int(self.start_led + 1/len(colors) 
                                        * (self.end_led - self.start_led) * index), 
                                   int(self.end_led - 1/len(colors) * (self.end_led - self.start_led)
                                        * (len(colors) - index - 1))):
                        self.strip.setPixelColor(i, color)
                
                elif self.direction == 1:
                    for i in range(int(self.start_led + 1/len(colors) 
                                   * (self.end_led - self.start_led) 
                                   * (len(colors) - index - 1)),
                                   int(self.end_led - 1/len(colors) 
                                   * (self.end_led - self.start_led)
                                   * index)):
                        self.strip.setPixelColor(i, color)
                
                elif self.direction == 3:  # Outer to inner
                    for i in range(int(self.start_led + 1/len(colors) 
                                   * ((self.end_led - self.start_led) / 2)
                                   * (len(colors) - index - 1)), 
                                   int(self.end_led
                                   - 1/len(colors) 
                                   * ((self.end_led - self.start_led) / 2)
                                   * index 
                                   - (self.end_led - self.start_led) / 2)):
                        self.strip.setPixelColor(i, color)
                
                    for i in range(int(self.start_led 
                                        + 1/len(colors) 
                                        * ((self.end_led - self.start_led) / 2)
                                        * index
                                        + (self.end_led - self.start_led) / 2 + 1), 
                                   int(self.end_led - 1/len(colors) * ((self.end_led - self.start_led) / 2)
                                        * (len(colors) - index - 1))):
                        self.strip.setPixelColor(i, color)
                
            self.strip.show()

        elif self.variation == 1:
            starting_time = time_ns() // 1_000_000
            colors = self.select_colors(beat)
            next_colors = self.select_colors(beat + 1)

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

            for x in range(ANIMATION_STEPS * 2):  # The number of transitions until next color is reached (Wait half the time to still show this color)
                if x == 0:
                    self.variation = 0
                    self.animate(beat)
                    self.variation = 1

                if x < ANIMATION_STEPS:
                    continue

                for index, (red_transition, green_transition, blue_transition) \
                    in enumerate(zip(red_transitions, green_transitions, blue_transitions)):
                    # Split strip up into slices for the different colors
                    if self.direction == 0:
                        for i in range(int(self.start_led + 1/len(colors) * (self.end_led - self.start_led) * index), 
                                    int(self.end_led - 1/len(colors) * (self.end_led - self.start_led)
                                        * (len(colors) - index - 1))):
                            red = red_transition[x - ANIMATION_STEPS] if len(red_transition) > x - ANIMATION_STEPS else red_transition[len(red_transition) - 1] if len(red_transition) > 0 else colors[index].r
                            green = green_transition[x - ANIMATION_STEPS] if len(green_transition) > x - ANIMATION_STEPS else green_transition[len(green_transition) - 1] if len(green_transition) > 0 else colors[index].g
                            blue = blue_transition[x - ANIMATION_STEPS] if len(blue_transition) > x - ANIMATION_STEPS else blue_transition[len(blue_transition) - 1] if len(blue_transition) > 0 else colors[index].b

                            self.strip.setPixelColor(i, StripColor(red, green, blue))
                    
                    elif self.direction == 1:
                        for i in reversed(range(int(self.start_led + 1/len(colors) * (self.end_led - self.start_led) * index), 
                                    int(self.end_led - 1/len(colors) * (self.end_led - self.start_led)
                                        * (len(colors) - index - 1)))):
                            red = red_transition[x - ANIMATION_STEPS] if len(red_transition) > x - ANIMATION_STEPS else red_transition[len(red_transition) - 1] if len(red_transition) > 0 else colors[index].r
                            green = green_transition[x - ANIMATION_STEPS] if len(green_transition) > x - ANIMATION_STEPS else green_transition[len(green_transition) - 1] if len(green_transition) > 0 else colors[index].g
                            blue = blue_transition[x - ANIMATION_STEPS] if len(blue_transition) > x - ANIMATION_STEPS else blue_transition[len(blue_transition) - 1] if len(blue_transition) > 0 else colors[index].b

                            self.strip.setPixelColor(i, StripColor(red, green, blue))
                    
                self.strip.show()
            
                sleep(self.sleep_time / (ANIMATION_STEPS * 2) - ((time_ns() // 1_000_000 - starting_time) // 1_000))
                starting_time = time_ns() // 1_000_000
