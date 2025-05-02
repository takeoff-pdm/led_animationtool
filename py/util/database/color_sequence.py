from util.database.database import Database


def recreate_color_sequence(color_sequence_data):
    return {
        'id': color_sequence_data[0],
        'name': color_sequence_data[1],
        'description': color_sequence_data[2],
        'selection': color_sequence_data[3],
        'color_amount': color_sequence_data[4]
    }


def add_color_sequence(id: int, name: str, description: str, selection: int, color_amount: int, scene_id: int = -1) \
        -> bool:
    if not Database.push_to_db(
            'INSERT INTO color_sequences VALUES(:scene_id, :id, :name, :description, :selection, :color_amount)',
            {
                'id': id,
                'name': name,
                'description': description,
                'selection': selection,
                'color_amount': color_amount,
                'scene_id': scene_id
            }):
        return False

    return True


def remove_color_sequence(id: int, scene_id: int = -1):
    if not Database.push_to_db('DELETE FROM color_sequences WHERE scene_id = :scene_id AND id = :id',
                               {
                                   'id': id,
                                   'scene_id': scene_id
                               }):
        return False

    return True


def update_color_sequence(id: int, name: str, description: str, selection: int, color_amount: int, scene_id: int = -1) \
        -> bool:
    """Update color_sequence by id.
    """
    if not Database.push_to_db('UPDATE color_sequences SET name = :name, description = :description, \
                                selection = :selection, color_amount = :color_amount WHERE scene_id = :scene_id AND id = :id',
                               {
                                   'id': id,
                                   'name': name,
                                   'description': description,
                                   'selection': selection,
                                   'color_amount': color_amount,
                                   'scene_id': scene_id
                               }):
        return False

    return True


def fetch_color_sequences(scene_id: int = -1):
    color_sequences_data = Database.fetchall_from_db(
        'SELECT id, name, description, selection, color_amount FROM color_sequences WHERE scene_id = :scene_id',
        {
            'scene_id': scene_id
        })

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
        return [recreate_color_sequence(color_sequences_data)]


def fetch_color_sequence(id: int, scene_id: int = -1):
    color_sequence_data = Database.fetchone_from_db('SELECT id, name, description, selection, color_amount \
                                                     FROM color_sequences WHERE scene_id = :scene_id AND id = :id',
                                                    {
                                                        'id': id,
                                                        'scene_id': scene_id
                                                    })

    if not color_sequence_data:
        return False

    return recreate_color_sequence(color_sequence_data)
