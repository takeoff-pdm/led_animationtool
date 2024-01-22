from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Strobo(Animation):
    async def animate(self, bpm: int, section: Section):
        print('Flacka flacka flacka')

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
