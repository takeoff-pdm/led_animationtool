from util.database.color_sequence import fetch_color_sequence, update_color_sequence, add_color_sequence, remove_color_sequence
from util.database.color import fetch_colors_from_sequence
from util.database.database import Database

from color import Color


class ColorSequence():
    def __init__(self, id: int = None, name: str = None, description: str= None, 
                 selection: int= None, color_amount: int= None):
        self.id = id
        self.color_list = []  # Do not use this value outside the class, rather use colors property
        
        if name != None and description != None and selection != None and color_amount != None:
            self.name = name
            self.description = description
            self.selection = selection
            self.color_amount = color_amount
        
        elif self.id != None:
            color_sequence_data = fetch_color_sequence(self.id)

            self.name = color_sequence_data['name']
            self.description = color_sequence_data['description']
            self.variation = color_sequence_data['selection']
            self.direction = color_sequence_data['color_amount']
    
    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM color_sequences', {})[0]
            
            self.id = 0
            if max_id != None:
                self.id = max_id + 1
            
            return add_color_sequence(self.id, self.name, self.description, self.selection, self.color_amount)
        
        return update_color_sequence(self.id, self.name, self.description, self.selection, self.color_amount)

    @property
    def colors(self):
        if len(self.color_list) > 0:
            return self.color_list
        
        colors_data = fetch_colors_from_sequence(self.id)

        colors = []

        for color_data in colors_data:
            colors.append(Color(color_data['id'], self.name, color_data['position'], color_data['red'], 
                             color_data['green'], color_data['blue']))
        
        self.color_list = colors
        return colors
    
    def update_colors(self):
        self.color_list = []
        self.colors

    # def set_name(self, name) -> bool:
    #     self.name = name

    #     return self.sync_changes_to_db()

    # def set_description(self, description: str) -> bool:
    #     self.description = description

    #     return self.sync_changes_to_db()
        
    # def set_selection(self, selection: int) -> bool:
    #     self.selection = selection
        
    #     return self.sync_changes_to_db()
        
    # def set_color_amount(self, color_amount: int) -> bool:
    #     self.color_amount = color_amount
        
    #     return self.sync_changes_to_db()
    
    def add_color(self, color: Color) -> bool:
        color.position = len(self.color_list)  # Set new position
        
        if not color.sync_changes_to_db(new=True):
            return False
        
        self.color_list.append(color)
        
        return True
