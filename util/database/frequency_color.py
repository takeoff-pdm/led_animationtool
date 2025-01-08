from util.database.database import Database


def recreate_frequency_color(frequency_color_data):
    return {
        'scene_id': frequency_color_data[0],
        'color_sequence_id_1': frequency_color_data[1],
        'color_sequence_id_2': frequency_color_data[2],
        'color_sequence_id_3': frequency_color_data[3]
    }


def add_frequency_color(scene_id: int, color_sequence_id_1: int, 
                        color_sequence_id_2: int, color_sequence_id_3: int) -> bool:
    if not Database.push_to_db(
            'INSERT INTO frequency_colors VALUES(:scene_id, :color_sequence_id_1, :color_sequence_id_2, :color_sequence_id_3)',
            {
                'scene_id': scene_id,
                'color_sequence_id_1': color_sequence_id_1,
                'color_sequence_id_2': color_sequence_id_2,
                'color_sequence_id_3': color_sequence_id_3
            }):
        return False

    return True


def remove_frequency_color(scene_id: int = -1):
    if not Database.push_to_db('DELETE FROM frequency_colors WHERE scene_id = :scene_id',
                               {
                                   'scene_id': scene_id
                               }):
        return False

    return True


def update_frequency_color(scene_id: int, color_sequence_id_1: int, 
                        color_sequence_id_2: int, color_sequence_id_3: int) -> bool:
    """Update frequency_color by id.
    """
    if not Database.push_to_db('UPDATE frequency_colors SET scene_id = :scene_id, color_sequence_id_1 = :color_sequence_id_1, \
                                color_sequence_id_2 = :color_sequence_id_2, color_sequence_id_3 = :color_sequence_id_3 WHERE scene_id = :scene_id',
                               {
                                    'scene_id': scene_id,
                                    'color_sequence_id_1': color_sequence_id_1,
                                    'color_sequence_id_2': color_sequence_id_2,
                                    'color_sequence_id_3': color_sequence_id_3
                               }):
        return False

    return True


def fetch_frequency_colors(scene_id: int = -1):
    frequency_colors_data = Database.fetchall_from_db(
        'SELECT scene_id, color_sequence_id_1, color_sequence_id_2, color_sequence_id_3 \
         FROM frequency_colors WHERE scene_id = :scene_id',
        {
            'scene_id': scene_id
        })

    if frequency_colors_data == None:
        return False

    # Check if multiple frequency_colors were fetched
    if type(frequency_colors_data) == list:
        # Go through all datasets and recreate frequency_colors from data
        frequency_colors = []

        for frequency_color_data in frequency_colors_data:
            frequency_colors.append(recreate_frequency_color(frequency_color_data))

        return frequency_colors

    else:
        return [recreate_frequency_color(frequency_colors_data)]


def fetch_frequency_color(id: int, scene_id: int = -1):
    frequency_color_data = Database.fetchone_from_db(
        'SELECTscene_id, color_sequence_id_1, color_sequence_id_2, color_sequence_id_3 \
         FROM frequency_colors WHERE scene_id = :scene_id',
        {
            'scene_id': scene_id
        })

    if not frequency_color_data:
        return False

    return recreate_frequency_color(frequency_color_data)
