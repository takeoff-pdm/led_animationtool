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
                                                 - 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * (len(colors) - index)),
                                             int(self.end_led + 1
                                                 + animation_stage
                                                 - (self.end_led - self.start_led))))

            case 1:
                animation_range.append(range(int(self.start_led
                                                 - animation_stage
                                                 + (self.end_led - self.start_led)),
                                             int(self.end_led + 1
                                                 - animation_stage
                                                 + 1 / len(colors)
                                                 * (self.end_led - self.start_led)
                                                 * (len(colors) - index))))

            case 2:
                animation_range.append(range(int(self.start_led + 1
                                                 + animation_stage
                                                 + ((self.end_led - self.start_led) / 2)
                                                 - 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index)),
                                             int(self.end_led + 1
                                                 + animation_stage
                                                 - (self.end_led - self.start_led))))

                animation_range.append(range(int(self.start_led
                                                 - animation_stage
                                                 + (self.end_led - self.start_led) / 2),
                                             int(self.end_led + 1
                                                 - animation_stage
                                                 - ((self.end_led - self.start_led) / 2)
                                                 + 1 / len(colors)
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index))))

        return animation_range

    def animate(self, beat: int, show_strip_request):
        if beat % 2 == 1:  # Start animation at every second beat
            return

        starting_time = time_ns() // 1_000_000
        colors = self.select_colors(beat)

        if self.variation == 0 or self.variation == 1:
            step = 2 if (self.end_led - self.start_led) + 1 > 60 \
                else 3 if (self.end_led - self.start_led) + 1 > 240 \
                else 4 if (self.end_led - self.start_led) + 1 > 360 \
                else 5 if (self.end_led - self.start_led) + 1 > 480 \
                else 6 if (self.end_led - self.start_led) + 1 > 600 \
                else 1  # Avoid having too slow code by skipping some pixels

            step = int(step * (self.bpm / 100 + 1))  # Adjust speed to bpm

            strip_section = range(self.start_led, self.end_led + 1)

            for animation_stage in range(0, (self.end_led - self.start_led) * 2 + 1, step):
                for index, color in enumerate(colors):
                    animation_range = self.select_range(animation_stage, index, colors)

                    if len(animation_range) == 0:
                        break

                    for i in animation_range:
                        for j in i:
                            if j not in strip_section:
                                continue

                            self.set_pixel_color(j, color)

                show_strip_request()

                if self.variation == 0:  # Consistent flow speed
                    sleep_time = self.sleep_time * 2 / (self.end_led - self.start_led) * step \
                                 - ((time_ns() // 1_000_000 - starting_time) / 1_000)

                elif self.variation == 1:  # Slowing down until middle, then speeding up again  # TODO: Fix the animation (looks awful at the moment)
                    if animation_stage < (self.end_led - self.start_led):
                        speed_variance = ((self.end_led - self.start_led) - animation_stage) \
                                         / ((self.end_led - self.start_led) * 2)

                    else:
                        speed_variance = (animation_stage - (self.end_led - self.start_led)) \
                                         / ((self.end_led - self.start_led) * 2)

                    sleep_time = self.sleep_time * 2 / (self.end_led - self.start_led) * step \
                                 * speed_variance \
                                 - ((time_ns() // 1_000_000 - starting_time) / 1_000)

                # * (1.5 if animation_stage > ((self.end_led - self.start_led) * 2 + 1) / 2 else .75) \ # After '* step'

                if sleep_time > 0:
                    sleep(sleep_time)

                starting_time = time_ns() // 1_000_000
