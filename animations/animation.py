from util.database.animation import fetch_animation, add_animation, remove_animation, update_animation

from color_sequence import ColorSequence
from section import Section
from colro import Color

class Animation():
    def __init__(self, name: str, description: str= None, variation: int= None, 
                 direction: int= None):
        if not description or not variation or not direction:
            self.name = name
            self.description = description
            self.variation = variation
            self.direction = direction
        
        else:
            animation_data = fetch_animation(name)

            self.name = animation_data['name']
            self.description = animation_data['description']
            self.variation = animation_data['variation']
            self.direction = animation_data['direction']
        
        self.bpm = 1
        self.start_led = 0
        self.end_led = 0
        
        self.strip = None
        self.color_sequence = None

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            return add_animation(self.name, self.description, self.variation, 
                                 self.direction)
        
        return update_animation(self.name, self.description, self.variation, 
                                self.direction)
        
    def select_color() -> Color:
        pass

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

    async def animate(self, strip, bpm: int, section: Section, color_sequence: ColorSequence):
        pass
