from util.database.color_sequence import fetch_color_sequence, update_color_sequence, add_color_sequence, remove_color_sequence
from util.database.color import fetch_colors_from_sequence

from color import Color


class ColorSequence():
    def __init__(self, name: str, description: str= None, selection: int= None, color_amount: int= None):
        if not description or not selection or not color_amount:
            self.name = name
            self.description = description
            self.selection = selection
            self.color_amount = color_amount
            self.color_list = []
        
        else:
            color_sequence_data = fetch_color_sequence(name)

            self.name = color_sequence_data['name']
            self.description = color_sequence_data['description']
            self.variation = color_sequence_data['selection']
            self.direction = color_sequence_data['color_amount']
            self.color_list = []

    @property
    def colors(self):
        if len(self.color_list) > 0:
            return self.color_list
        
        colors_data = fetch_colors_from_sequence()

        colors = []

        for color_data in colors_data:
            colors.add(Color(self.name, color_data['position'], color_data['red'], 
                             color_data['green'], color_data['blue']))
        
        self.color_list = colors
        return colors
    
    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            return add_color_sequence(self.name, self.description, self.selection, self.color_amount)
        
        return update_color_sequence(self.name, self.description, self.selection, self.color_amount)

    def set_name(self, name) -> bool:
        # Check if sequence with this name already exists
        if fetch_color_sequence(name) != None:
            return False

        if not remove_color_sequence(self.name):
            return False

        self.name = name

        if not add_color_sequence(self.name, self.description, self.selection, self.color_amount):
            return False
        
        for color in self.colors:
            if not color.set_color_sequence(self.name):
                return False
        
        return True

    def set_description(self, description: str):
        self.description = description

        self.sync_changes_to_db()
        
    def set_selection(self, selection: int):
        self.selection = selection
        
        self.sync_changes_to_db()
        
    def set_color_amount(self, color_amount: int):
        self.color_amount = color_amount
        
        self.sync_changes_to_db()
