from time import sleep, time_ns
from rpi_ws281x import Color as StripColor

from animations.animation import Animation
from color_sequence import ColorSequence
from section import Section

class Shooter(Animation):
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
                                                 - (self.end_led - self.start_led))))
        
            case 1:
                animation_range.append(range(int(self.start_led
                                                 - animation_stage
                                                 + (self.end_led - self.start_led)),
                                             int(self.end_led + 1 
                                                 - animation_stage 
                                                 + 1/len(colors) 
                                                 * (self.end_led - self.start_led) 
                                                 * (len(colors) - index))))
            
            case 2:  # TODO: Make it like shooter, not like flow
                animation_range.append(range(int(self.start_led + 1
                                                 + animation_stage 
                                                 + ((self.end_led - self.start_led) / 2)
                                                 - 1/len(colors) 
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
                                                 + 1/len(colors) 
                                                 * ((self.end_led - self.start_led) / 2)
                                                 * (len(colors) - index))))
        
        return animation_range


    def animate(self, beat: int):
        if beat % 2 == 1:  # Start animation at every second beat
            return
        
        starting_time = time_ns() // 1_000_000
        colors = self.select_colors(beat)

        if self.variation == 0 or self.variation == 1:
            step = 2 if (self.end_led - self.start_led) + 1 > 60 \
                   else 3 if (self.end_led - self.start_led) + 1 > 240 \
                   else 4 if (self.end_led - self.start_led) + 1 > 360 else 1  # Avoid having too slow code by skipping some pixels

            step = int(step * (self.bpm / 100 + 1))  # Adjust speed to bpm
        
            strip_section = range(self.start_led, self.end_led + 1)

            for animation_stage in range(0, (self.end_led - self.start_led) * 2 + 1, step):
                for index, color in enumerate(colors):
                    animation_range = self.select_range(animation_stage, index, colors)

                    if len(animation_range) == 0:
                        break
                    
                    for i in animation_range:
                        if self.direction == 0:
                            black_out = range(i[0], 
                                              i[0] + int((self.end_led - self.start_led) 
                                                   * 1/len(colors) 
                                                   * .666))
                        
                        elif self.direction == 1:
                            black_out = range(i[-1] - int((self.end_led - self.start_led) 
                                                   * 1/len(colors) 
                                                   * .666), 
                                              i[-1] )
                        
                        if self.variation == 1:  # TODO: Get variation 1 to work --> looks exactly like variation 0, although it should fade out
                            fade_out_step = color.r // len(i) if color.r // len(i) != 0 else 1

                            fade_out_r = list(reversed(range(0, color.r, fade_out_step)))
                            fade_out_g = list(reversed(range(0, color.g, fade_out_step)))
                            fade_out_b = list(reversed(range(0, color.b, fade_out_step)))
                            
                        for position, j in enumerate(i):
                            if j not in strip_section:
                                continue
                            
                            if j in black_out:  # Check if color needs to be removed
                                self.set_pixel_color(j, StripColor(0, 0, 0))
                                continue

                            if self.variation == 0:
                                self.set_pixel_color(j, color)
                            
                            elif self.variation == 1:  # Fade color into black the closer to the end of this color range
                                if self.direction == 0:
                                    self.set_pixel_color(j, StripColor(fade_out_r[position] if position < len(fade_out_r) else 0,
                                                                       fade_out_g[position] if position < len(fade_out_g) else 0,
                                                                       fade_out_b[position] if position < len(fade_out_b) else 0))

                                elif self.direction == 1:
                                    self.set_pixel_color(j, StripColor(fade_out_r[-position] if position < len(fade_out_r) else 0,
                                                                       fade_out_g[-position] if position < len(fade_out_g) else 0,
                                                                       fade_out_b[-position] if position < len(fade_out_b) else 0))

                
                self.strip.show()

                sleep_time = self.sleep_time * 2 / (self.end_led - self.start_led) * step \
                            - ((time_ns() // 1_000_000 - starting_time) / 1_000)

                if sleep_time > 0:
                    sleep(sleep_time)
                # else:
                #     print("sloow flow")
                
                starting_time = time_ns() // 1_000_000
