from util.database.database import Database

def recreate_color(section_data):
    return {
        'color_sequence': section_data[0],
        'position': section_data[1],
        'red': section_data[2],
        'green': section_data[3],
        'blue': section_data[4]
    }

def add_color(color_sequence: str, position: int, red: int, green: int, blue: int) -> bool:
    if not Database.push_to_db('INSERT INTO sections VALUES(:color_sequence, :position, :red, :green, :blue)', 
                                  {
                                      'color_sequence': color_sequence,
                                      'position': position,
                                      'red': red, 
                                      'green': green,
                                      'blue': blue
                                  }):
        return False
    
    return True

def remove_color(color_sequence: str):
    if not Database.push_to_db('DELETE FROM colors Where color_sequence = :color_sequence', 
                               {'color_sequence': color_sequence}):
        return False
    
    return True

def fetch_colors():
    colors_data = Database.fetchall_from_db('SELECT color_sequence, position, red, green, blue FROM colors', {})

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

def fetch_colors_from_sequence(color_sequence: str):
    colors_data = Database.fetchall_from_db('SELECT color_sequence, position, red, green, blue FROM colors \
                                            WHERE color_sequence = :color_sequence', 
                                           {'color_sequence': color_sequence})

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
