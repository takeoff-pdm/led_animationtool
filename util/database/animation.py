from util.database.database import Database

def recreate_animation(animation_data) -> dict:
    return {
        'id': animation_data[0],
        'name': animation_data[1],
        'description': animation_data[2],
        'variation': animation_data[3],
        'direction': animation_data[4]
    }

def add_animation(name: str, description: str, variation: int, direction: int, color_sequence: str) -> bool:
    if not Database.push_to_db('INSERT INTO animations VALUES(:id, :name, :description, :variation)', 
                                  {
                                      'id': Database.fetchone_from_db('SELECT MAX(id) FROM animations', {}) if not None else 0 + 1,
                                      'name': name, 
                                      'description': description, 
                                      'variation': variation, 
                                      'direction': direction
                                  }):
        return False
    
    return True

def remove_animation(id: int) -> bool:
    if not Database.push_to_db('DELETE FROM animations Where id = :id', {'id': id}):
        return False
    
    return True

def update_animation(id: int, name: str, description: str, variation: int, direction: int) -> bool:
    '''Update animation by name.
    '''
    if not Database.push_to_db('UPDATE animations SET name = :name, description = :description, \
                                variation = :variation, direction = :direction WHERE id = :id', 
                                  {
                                      'id': id,
                                      'name': name, 
                                      'description': description, 
                                      'variation': variation, 
                                      'direction': direction
                                  }):
        return False
    
    return True

def fetch_animations() -> list:
    animations_data = Database.fetchall_from_db('SELECT id, name, description, variation, direction \
                                                 FROM animations', {})

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

def fetch_animation(id: int) -> dict:
    animation_data = Database.fetchone_from_db('SELECT id, name, description, variation, direction, \
                                                FROM animations WHERE id = :id', {'id': id})

    if animation_data == None:
        return False

    return recreate_animation(animation_data)
