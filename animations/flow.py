from time import time_ns, sleep
from rpi_ws281x import Color

from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Flow(Animation):
    def select_range(self, animation_stage: int, index: int, colors: list) -> list:
        animation_range = []

        match self.direction:
            case 0:
                animation_range.append(range(int(self.start_led 
                                                 + animation_stage 
                                                 - 1/len(colors) 
                                                 * (self.end_led - self.start_led) 
                                                 * (len(colors) - index)),
                                             int(self.end_led + 1
                                                 + animation_stage
                                                 - (self.end_led - self.start_led))))  # TODO: Fix bug: Skips around 2-4 pixels (is quite fast) at beat change
        
        return animation_range

    def animate(self, beat: int):
        starting_time = time_ns() // 1_000_000
        colors = self.select_colors(beat)
        previous_colors = self.select_colors(beat - 1)

        if self.variation == 0:
            for animation_stage in range(self.end_led - self.start_led + 1):
                for index, (color, previous_color) in enumerate(zip(colors, previous_colors)):
                    animation_range = self.select_range(animation_stage, index, colors)

                    if len(animation_range) == 0:
                        break
                    
                    for i in animation_range:
                        for j in i:
                            if j + (self.end_led + self.start_led) in range(self.start_led, self.end_led + 1):
                                self.strip.setPixelColor(j + (self.end_led + self.start_led), previous_color)
                            
                            if j not in range(self.start_led, self.end_led + 1):
                                continue

                            self.strip.setPixelColor(j, color)
                            
                    
                self.strip.show()

                sleep(self.sleep_time / (self.end_led - self.start_led) 
                    - ((time_ns() // 1_000_000 - starting_time) // 1_000))
                starting_time = time_ns() // 1_000_000
        
        elif self.variation == 1:
            self.strip.setPixelColor(59, Color(255, 255, 255))
            self.strip.show()

        # print('whoooooohw de floooohw')

        # first_led = int((self.end_led - self.start_led) / 2)
        # second_led = first_led + 1

        # for x in range(int((self.end_led - self.start_led) / 2)):
        #     starting_time = time_ns() // 1_000_000
            
        #     for i in range(self.start_led, self.end_led):
        #         # White blind effect
        #         if i in range(self.start_led + int((self.end_led - self.start_led) / 2) - int((self.end_led - self.start_led) / 6) + int(x / 3),
        #                         int((self.end_led - self.start_led) / 2) + int((self.end_led - self.start_led) / 6) + 1 - int(x / 3)): # and variation ...
        #             self.strip.setPixelColor(i, Color(255, 255, 255))
                
        #         # Flow
        #         elif i in range(first_led - int((self.end_led - self.start_led) / 5), first_led):
        #             self.strip.setPixelColor(i, self.wheel((i * 2) & 255))
                
        #         elif i in range(second_led, second_led + int((self.end_led - self.start_led) / 5)):
        #             self.strip.setPixelColor(i, self.wheel((i * 2) & 255))
                
        #         # Rest
        #         # elif i <= int(LED_COUNT / 2):
        #         #     self.strip.setPixelColor(i, self.wheel((color_randomizer - 64) & 255))
                
        #         # else:
        #         #     self.strip.setPixelColor(i, self.wheel((color_randomizer + 64) & 255))
                    
        #         else:
        #             self.strip.setPixelColor(i,Color(0, 0, 0))

        #     self.strip.show()

        #     first_led -= 1
        #     second_led += 1

        #     sleep(self.sleep_time / int((self.end_led - self.start_led) / 2) - ((time_ns() // 1_000_000 - starting_time) // 1_000))
