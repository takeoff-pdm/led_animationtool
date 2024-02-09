from util.database.database import Database

def recreate_color(color_data) -> dict:
    return {
        'id': color_data[0],
        'color_sequence_id': color_data[1],
        'position': color_data[2],
        'red': color_data[3],
        'green': color_data[4],
        'blue': color_data[5]
    }

def add_color(id: int, color_sequence_id: int, position: int, red: int, green: int, blue: int) -> bool:
    if not Database.push_to_db('INSERT INTO colors VALUES(:id, :color_sequence_id, :position, :red, :green, :blue)', 
                                  {
                                      'id': id,
                                      'color_sequence_id': color_sequence_id,
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

def update_color(id: int, color_sequence_id: int, position: int, red: int, green: int, blue: int) -> bool:
    '''Update color by id.
    '''
    if not Database.push_to_db('UPDATE colors SET color_sequence_id = :color_sequence_id, position = :position, \
                                red = :red, green = :green, blue = :blue WHERE id = :id', 
                                {
                                    'id': id, 
                                    'color_sequence_id': color_sequence_id,
                                    'position': position, 
                                    'red': red, 
                                    'green': green, 
                                    'blue': blue
                                }):
        return False
    
    return True

def fetch_colors() -> list | bool:
    colors_data = Database.fetchall_from_db('SELECT id, color_sequence_id, position, red, green, blue FROM colors', {})

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
    colors_data = Database.fetchall_from_db('SELECT id, color_sequence_id, position, red, green, \
                                             blue FROM colors WHERE color_sequence_id = :color_sequence_id', 
                                             {'color_sequence_id': id})

    if not colors_data:
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
    color_data = Database.fetchone_from_db('SELECT id, color_sequence_id, position, red, green, \
                                            blue FROM colors WHERE id = :id', {'id': id})

    if not color_data:
        return False

    return recreate_color(color_data)
