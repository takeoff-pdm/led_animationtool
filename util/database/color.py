from util.database.database import Database
from color import Color

def recreate_color(color_data) -> dict:
    return {
        'color_sequence': color_data[0],
        'position': color_data[1],
        'red': color_data[2],
        'green': color_data[3],
        'blue': color_data[4]
    }

def add_color(color_sequence: str, position: int, red: int, green: int, blue: int) -> bool:
    if not Database.push_to_db('INSERT INTO colors VALUES(:id, :color_sequence, :position, :red, :green, :blue)', 
                                  {
                                      'id': Database.fetchone_from_db('SELECT MAX(id) FROM colors', {}) if not None else 0 + 1,
                                      'color_sequence': color_sequence,
                                      'position': position,
                                      'red': red, 
                                      'green': green,
                                      'blue': blue
                                  }):
        return False
    
    return True

def remove_color(id: int) -> bool:
    if not Database.push_to_db('DELETE FROM colors Where id = :id', {'id': id}):
        return False
    
    return True

def update_color(id: int, position: int, red: int, green: int, blue: int) -> bool:
    """Update color by sequence and position.
    """
    if not Database.push_to_db('UPDATE colors SET position = :position, red = :red, green = :green, blue = :blue \
                                WHERE id = :id', {'id': id, 'position': position, 'red': red, 'green': green, 'blue': blue}):
        return False
    
    return True

def fetch_colors() -> list | bool:
    colors_data = Database.fetchall_from_db('SELECT id, color_sequence, position, red, green, blue FROM colors', {})

    if colors_data == None:
        return False

    # Check if multiple colors were fetched
    if type(colors_data) == list:
        # Go through all datasets and recreate colors from data
        colors = []

        for color_data in colors_data:
            colors.append(recreate_color(color_data))

        return colors
    
    else:
        return [ recreate_color(colors_data) ]

def fetch_colors_from_sequence(id: int) -> list | bool:
    colors_data = Database.fetchall_from_db('SELECT id, color_sequence, position, red, green, blue FROM colors \
                                             WHERE color_sequence = :color_sequence', {'id': id})

    if not color_data:
        return False

    # Check if multiple colors were fetched
    if type(colors_data) == list:
        # Go through all datasets and recreate colors from data
        colors = []

        for color_data in colors_data:
            colors.append(recreate_color(color_data))

        return colors
    
    else:
        return [ recreate_color(colors_data) ]

def fetch_color(id: int) -> dict | bool:
    color_data = Database.fetchone_from_db('SELECT id, color_sequence, position, red, green, blue FROM colors \
                                            WHERE id = :id', {'id': id})

    if not color_data:
        return False

    return recreate_color(color_data)
