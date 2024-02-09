from util.database.color import add_color, remove_color, update_color, fetch_color
from util.database.database import Database


class Color():
    def __init__(self, id, color_sequence_id: int = None, position: int = None,
                 red: int = None, green: int = None, blue: int = None):
        self.id = id
        
        if color_sequence_id != None and red != None and green != None and blue != None:  # Position not included, because it is often added later
            self.color_sequence_id = color_sequence_id
            self.position = position
            self.red = red
            self.green = green
            self.blue = blue
        
        elif not self.id:
            color_data = fetch_color(id)
            
            self.color_sequence_id = color_data['color_sequence_id']
            self.position = color_data['position']
            self.red = color_data['red']
            self.green = color_data['green']
            self.blue = color_data['blue']

    def sync_changes_to_db(self, new: bool = False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM colors', {})[0]
            
            self.id = 0
            if max_id != None:
                self.id = max_id + 1
            
            return add_color(self.id, self.color_sequence_id, self.position, self.red, self.green, self.blue)
        
        return update_color(self.id, self.color_sequence_id, self.position, self.red, self.green, self.blue)
    
    # def set_position(self, position: int):
    #     self.position = position

    #     return self.sync_changes_to_db()
            
    # def set_red(self, red: int):
    #     self.red = red

    #     return self.sync_changes_to_db()
            
    # def set_green(self, green: int):
    #     self.green = green

    #     return self.sync_changes_to_db()
            
    # def set_blue(self, blue: int):
    #     self.blue = blue

    #     return self.sync_changes_to_db()
