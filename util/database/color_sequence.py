from util.database.database import Database

def recreate_color_sequence(color_sequence_data):
    return {
        'id': color_sequence_data[0],
        'name': color_sequence_data[1],
        'description': color_sequence_data[2],
        'selection': color_sequence_data[3],
        'color_amount': color_sequence_data[4]
    }

def add_color_sequence(name: str, description: str, selection: int, color_amount: int) -> bool:
    if not Database.push_to_db('INSERT INTO color_sequences VALUES(:id, :name, :description, :selection, :color_amount)', 
                               {
                                   'id': Database.fetchone_from_db('SELECT MAX(id) FROM color_sequences', {}) if not None else 0 + 1,
                                   'name': name, 
                                   'description': description, 
                                   'selection': selection, 
                                   'color_amount': color_amount
                                }):
        return False
    
    return True

def remove_color_sequence(id: int):
    if not Database.push_to_db('DELETE FROM color_sequences Where id = :id', {'id': id}):
        return False
    
    return True

def update_color_sequence(id: int, name: str, description: str, selection: int, color_amount: int) -> bool:
    """Update color_sequence by id.
    """
    if not Database.push_to_db('UPDATE color_sequences SET name = :name, description = :description, selection = :selection, color_amount = :color_amount \
                                WHERE id = :id', 
                                  {'name': name, 'description': description, 'selection': selection, 'color_amount': color_amount}):
        return False
    
    return True

def fetch_color_sequences():
    color_sequences_data = Database.fetchall_from_db('SELECT id, name, description, selection, color_amount FROM color_sequences', {})

    if color_sequences_data == None:
        return False

    # Check if multiple color_sequences were fetched
    if type(color_sequences_data) == list:
        # Go through all datasets and recreate color_sequences from data
        color_sequences = []

        for color_sequence_data in color_sequences_data:
            color_sequences.append(recreate_color_sequence(color_sequence_data))

        return color_sequences
    
    else:
        return [ recreate_color_sequence(color_sequences_data) ]

def fetch_color_sequence(id: int):
    color_sequence_data = Database.fetchone_from_db('SELECT id, name, description, selection, color_amount \
                                                     FROM color_sequences WHERE id = :id', {'id': id})

    if not color_sequence_data:
        return False

    return recreate_color_sequence(color_sequence_data)
