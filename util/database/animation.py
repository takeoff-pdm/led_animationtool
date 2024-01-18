from util.database.database import Database

def recreate_animation(animation_data):
    return {
        'name': animation_data[0],
        'description': animation_data[1],
        'variation': animation_data[2],
        'direction': animation_data[3],
        'color_sequence': animation_data[4]
    }

def add_animation(name: str, description: str, variation: int, direction: int, color_sequence: str) -> bool:
    if not Database.push_to_db('INSERT INTO animations VALUES(:name, :description, :variation, :color_sequence)', 
                                  {
                                      'name': name, 
                                      'description': description, 
                                      'variation': variation, 
                                      'direction': direction,
                                      'color_sequence': color_sequence
                                  }):
        return False
    
    return True

def remove_animation(name: str):
    if not Database.push_to_db('DELETE FROM animations Where name = :name', {'name': name}):
        return False
    
    return True

def update_animation(name: str, description: str, variation: int, direction: int, color_sequence: str) -> bool:
    """Update animation by name.
    """
    if not Database.push_to_db('UPDATE animations SET description = :description, variation = :variation, \
                                direction = :direction, color_sequence = :color_sequence WHERE name = :name', 
                                  {
                                      'name': name, 
                                      'description': description, 
                                      'variation': variation, 
                                      'direction': direction, 
                                      'color_sequence': color_sequence
                                  }):
        return False
    
    return True

def fetch_animations():
    animations_data = Database.fetchall_from_db('SELECT name, description, variation, direction, \
                                                 color_sequence FROM animations', {})

    if animations_data == None:
        return False

    # Check if multiple animations were fetched
    if type(animations_data) == list:
        # Go through all datasets and recreate animations from data
        animations = []

        for animation_data in animations_data:
            animations.append(recreate_animation(animation_data))

        return animations
    
    else:
        return [ recreate_animation(animations_data) ]

def fetch_animation(name: str):
    animation_data = Database.fetchone_from_db('SELECT name, description, variation, direction, \
                                                color_sequence FROM animations \
                                                WHERE name = :name', {'name': name})

    if animation_data == None:
        return False

    return recreate_animation(animation_data)
