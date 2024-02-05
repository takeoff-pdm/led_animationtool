from time import sleep
from rpi_ws281x import Color

from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Flow(Animation):
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
    
    async def animate(self, strip, bpm: int, section: Section, color_sequence: ColorSequence):
        print('whoooooohw de floooohw')

        first_led = int((self.end_led - self.start_led) / 2)
        second_led = first_led + 1

        for x in range(int((self.end_led - self.start_led) / 2)):
            starting_time = time_ns() // 1_000_000
            
            for i in range(self.start_led, self.end_led):
                # White blind effect
                if i in range(self.start_led + int((self.end_led - self.start_led) / 2) - int((self.end_led - self.start_led) / 6) + int(x / 3),
                                int((self.end_led - self.start_led) / 2) + int((self.end_led - self.start_led) / 6) + 1 - int(x / 3)): # and variation ...
                    self.strip.setPixelColor(i, Color(255, 255, 255))
                
                # Flow
                elif i in range(first_led - int((self.end_led - self.start_led) / 5), first_led):
                    self.strip.setPixelColor(i, self.wheel((i * 2) & 255))
                
                elif i in range(second_led, second_led + int((self.end_led - self.start_led) / 5)):
                    self.strip.setPixelColor(i, self.wheel((i * 2) & 255))
                
                # Rest
                # elif i <= int(LED_COUNT / 2):
                #     self.strip.setPixelColor(i, self.wheel((color_randomizer - 64) & 255))
                
                # else:
                #     self.strip.setPixelColor(i, self.wheel((color_randomizer + 64) & 255))
                    
                else:
                    self.strip.setPixelColor(i,Color(0, 0, 0))

            self.strip.show()

            first_led -= 1
            second_led += 1

            sleep(self.sleep_time / int((self.end_led - self.start_led) / 2) - (time_ns() // 1_000_000 - starting_time))
