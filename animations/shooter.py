from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Shooter(Animation):
    async def animate(self, bpm: int, section: Section):
        print('shooot')

        # color = Color(255, 255, 255)
        # random_color = True

        # if random_color:
        #     color = wheel((randint(0, 256)) & 255)

        # for x in range(int(LED_COUNT)):
        #     for i in range(strip.numPixels()):
        #         if i in range(x - int(LED_COUNT * .2), x + 1):
        #             if i < 0:
        #                 continue
                    
        #             strip.setPixelColor(i, color)
                
        #         else:
        #             strip.setPixelColor(i, 0)

        #     strip.show()
        #     sleep(sleep_time / int(LED_COUNT))
