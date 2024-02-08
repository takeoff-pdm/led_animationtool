from util.database.color import add_color, remove_color, update_color, fetch_color


class Color():
    def __init__(self, id, color_sequence: int = None, position: int = None,
                 red: int = None, green: int = None, blue: int = None):
        self.id = id
        
        if color_sequence and position and red and green and blue:
            self.color_sequence = color_sequence  # Id of sequence
            self.position = position
            self.red = red
            self.green = green
            self.blue = blue
        
        else:
            color_data = fetch_color(id)
            
            self.color_sequence = color_data['color_sequence']  # Id of sequence
            self.position = color_data['position']
            self.red = color_data['red']
            self.green = color_data['green']
            self.blue = color_data['blue']

    def sync_changes_to_db(self, new: bool = False) -> bool:
        if new:
            return add_color(self.color_sequence, self.position, self.red, self.green, self.blue)
        
        return update_color(self.id, self.color_sequence, self.position, self.red, self.green, self.blue)
    
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
