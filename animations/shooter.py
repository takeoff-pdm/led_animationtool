from time import sleep

from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Shooter(Animation):
    def animate(self):
        print('shooot')

        # color = Color(255, 255, 255)
        # random_color = True

        # if random_color:
        #     color = wheel((randint(0, 256)) & 255)

        for x in range(self.start_led, self.end_led):
            for i in range(self.start_led, self.end_led):
                if i in range(x - int((self.end_led - self.start_led) * .2), x + 1):
                    if i < 0:
                        continue
                    
                    self.strip.setPixelColor(i, 255)
                
                else:
                    self.strip.setPixelColor(i, 0)

            self.strip.show()
            sleep(self.sleep_time / int(self.end_led - self.start_led))
