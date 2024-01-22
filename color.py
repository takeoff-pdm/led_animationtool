from util.database.color import add_color, remove_color, update_color, fetch_color


class Color():
    def __init__(self, color_sequence: str, position: int, red: int, green: int, blue: int):
        self.color_sequence = color_sequence
        self.position = position
        self.red = red
        self.green = green
        self.blue = blue

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            return add_color(self.color_sequence, self.position, self.red, self.green, self.blue)
        
        return update_color(self.color_sequence, self.position, self.red, self.green, self.blue)

    def set_color_sequence(self, color_sequence: str) -> bool:
        # Check if sequence with this name already exists
        if fetch_color(color_sequence, self.position) != None:
            return False

        if not remove_color(self.color_sequence):
            return False

        self.color_sequence = color_sequence

        if not add_color(self.color_sequence, self.position, self.red, self.green, self.blue):
            return False
        
        return True
    
    def set_position(self, position: int):
        self.position = position

        self.sync_changes_to_db()
            
    def set_red(self, red: int):
        self.red = red

        self.sync_changes_to_db()
            
    def set_position(self, green: int):
        self.green = green

        self.sync_changes_to_db()
            
    def set_position(self, blue: int):
        self.blue = blue

        self.sync_changes_to_db()
