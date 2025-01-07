from rpi_ws281x import Color as StripColor

from util.database.animation import fetch_animation, add_animation, remove_animation, update_animation
from util.database.section_animation import fetch_section_animation, update_section_animation
from util.database.database import Database

from __init__ import ANIMATION_STEPS


class Animation:
    def __init__(self, id: int | None = None, section_id: int = 0, name: str | None = None,
                 description: str | None = None, variation: int | None = None, direction: int | None = None,
                 offset: int | None = None):
        self.id = id
        self.variation = 0
        self.direction = 0
        self.offset = 0

        if description != None and variation != None and direction != None and offset != None:
            self.name = name
            self.description = description
            self.variation = variation
            self.direction = direction
            self.offset = offset

        elif self.id != None:
            animation_data = fetch_animation(self.id)

            if animation_data:  # Check if animation exists
                self.name = animation_data['name']
                self.description = animation_data['description']

            if section_id != None:
                section_animation_data = fetch_section_animation(section_id, self.id)

                if section_animation_data:
                    self.variation = section_animation_data['variation']
                    self.direction = section_animation_data['direction']
                    self.offset = section_animation_data['offset']

        self.bpm = 1
        self.section_id = section_id
        self.start_led = 0
        self.end_led = 0

        self.strip = None
        self.brightness = 255
        self.color_sequence = None

    def sync_changes_to_db(self, new: bool = False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM animations', {})[0]

            self.id = 0
            if max_id != None:
                self.id = max_id + 1

            return add_animation(self.id, self.name, self.description, self.variation,
                                 self.direction)

        if not update_animation(self.id, self.name, self.description):
            return False
        
        return update_section_animation(self.section_id, self.id, self.variation, self.direction, self.offset)

    @property
    def sleep_time(self):
        return 60 / self.bpm
    
    def set_pixel_color(self, pixel: int, color: StripColor):        
        # Update pixel brightness
        self.strip.setPixelColor(pixel, StripColor(int(color.r * self.brightness),
                                                   int(color.g * self.brightness),
                                                   int(color.b * self.brightness)))

    def color_wipe(self, color):
        """Change color of all pixels of selected section.
        """
        for i in range(self.start_led, self.end_led + 1):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return StripColor(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return StripColor(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return StripColor(0, pos * 3, 255 - pos * 3)

    def select_colors(self, beat: int) -> list:
        if len(self.color_sequence.colors) == 0:  # Make sure, there are colors
            return []

        colors = []

        for x in range(self.color_sequence.color_amount):  # Select the required colors
            color = None
            if self.color_sequence.selection == 0:
                color = self.color_sequence.colors[(x + beat * self.color_sequence.color_amount)
                                                   % len(self.color_sequence.colors)]

            else:
                color = self.color_sequence.colors[(x + beat * self.color_sequence.selection)
                                                   % len(self.color_sequence.colors)]

            colors.append(StripColor(color.red, color.green, color.blue))

        if len(colors) == 0:
            return [StripColor(0, 0, 0)]

        return colors
            
    def color_transition(self, color: int, next_color: int) -> list:
        """Make range of colors between two color parts (Only R, G or B).
        """
        if color < next_color:
                    return list(range(color, next_color, 
                                      (next_color - color) // ANIMATION_STEPS 
                                      if (next_color - color) // ANIMATION_STEPS != 0 
                                      else 1))
        
        return list(reversed(range(next_color, color,
                                   (color - next_color) // ANIMATION_STEPS 
                                   if (color - next_color) // ANIMATION_STEPS != 0 
                                   else 1)))

    # def set_name(self, name) -> bool:
    #     # Check if section with this name already exists
    #     if fetch_animation(name) != None:
    #         return False

    #     if not remove_animation(self.name):
    #         return False

    #     self.name = name

    #     if not add_animation(self.name, self.description, self.variation, 
    #                          self.direction):
    #         return False

    #     return True

    # def set_description(self, description: str):
    #     self.description = description

    #     self.sync_changes_to_db()

    # def set_variation(self, variation: int):
    #     self.variation = variation

    #     self.sync_changes_to_db()

    # def set_direction(self, direction: int):
    #     self.direction = direction

    #     self.sync_changes_to_db()

    def animate(self, beat: int, step: int):
        pass
