from rpi_ws281x import Color as StripColor

from util.database.animation import fetch_animation, add_animation, remove_animation, update_animation
from util.database.database import Database

from color_sequence import ColorSequence
from section import Section
from color import Color

class Animation():
    def __init__(self, id: int = None, name: str = None, description: str = None, variation: int = None, 
                 direction: int = None):
        self.id = id
        
        if description != None and variation != None and direction != None:
            self.name = name
            self.description = description
            self.variation = variation
            self.direction = direction
        
        elif self.id != None:
            animation_data = fetch_animation(self.id)

            if animation_data:  # Check if animation exists
                self.name = animation_data['name']
                self.description = animation_data['description']
                self.variation = animation_data['variation']
                self.direction = animation_data['direction']
        
        self.bpm = 1
        self.section_id = 0
        self.start_led = 0
        self.end_led = 0
        
        self.strip = None
        self.color_sequence = None

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM animations', {})[0]
            
            self.id = 0
            if max_id != None:
                self.id = max_id + 1
            
            return add_animation(self.id, self.name, self.description, self.variation, 
                                 self.direction)
        
        return update_animation(self.name, self.description, self.variation, 
                                self.direction)
        
    @property
    def sleep_time(self):
        return 60 / self.bpm
    
    def color_wipe(self, color):
        '''Change color of all pixels of selected section.
        '''
        for i in range(self.start_led, self.end_led):
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
            color = self.color_sequence.colors[(x + beat * self.color_sequence.color_amount) 
                                               % len(self.color_sequence.colors)]
                
            colors.append(StripColor(color.red, color.green, color.blue))
        
        return colors

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

    def animate(self, beat: int):
        pass
