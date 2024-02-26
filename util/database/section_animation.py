from util.database.database import Database
from util.database.animation import fetch_animations


def recreate_section_animation(section_animation_data) -> dict:
    return {
        'id': section_animation_data[0],
        'variation': section_animation_data[1],
        'direction': section_animation_data[2],
        'offset': section_animation_data[3]
    }


def add_section_animations(section_id: int) -> bool:
    animations = fetch_animations()

    if not animations:
        return False

    for animation in animations:
        if not add_section_animation(section_id, animation['id']):  # TODO: Fix key error id
            return False

    return True


def add_section_animation(section_id: int, animation_id: int) -> bool:
    if not Database.push_to_db('INSERT INTO section_animations VALUES(:section_id, :animation_id, 0, 0, 0)',
                               {
                                   'section_id': section_id,
                                   'animation_id': animation_id
                               }):
        return False

    return True


def remove_section_animation(section_id: int, animation_id: int) -> bool:
    if not Database.push_to_db(
            'DELETE FROM section_animations WHERE section_id = :section_id AND animation_id = :animation_id',
            {
                'section_id': section_id,
                'animation_id': animation_id
            }):
        return False

    return True


def update_section_animation(section_id: int, animation_id: int, variation: int, direction: int, offset: int) -> bool:
    if not Database.push_to_db('UPDATE section_animations SET variation = :variation, direction = :direction, \
                                offset = :offset WHERE section_id = :section_id AND animation_id = :animation_id',
                               {
                                   'section_id': section_id,
                                   'animation_id': animation_id,
                                   'variation': variation,
                                   'direction': direction,
                                   'offset': offset
                               }):
        return False

    return True


def fetch_section_animation(section_id: int, animation_id: int) -> dict | bool:
    section_animation_data = Database.fetchone_from_db(
        'SELECT animation_id, variation, direction, offset FROM section_animations \
         WHERE section_id = :section_id AND animation_id = :animation_id',
        {
            'section_id': section_id,
            'animation_id': animation_id
        })

    if section_animation_data == None:
        return False

    return recreate_section_animation(section_animation_data)


def fetch_section_animations(section_id: int) -> list | bool:
    section_animations_data = Database.fetchall_from_db(
        'SELECT animation_id, variation, direction, offset FROM section_animations WHERE section_id = :section_id',
        {
            'section_id': section_id
        })

    if section_animations_data == None:
        return False

    # Check if multiple section_animations were fetched
    if type(section_animations_data) == list:
        # Go through all datasets and recreate section_animations from data
        section_animations = []

        for section_animation_data in section_animations_data:
            section_animations.append(recreate_section_animation(section_animation_data))

        return section_animations

    return recreate_section_animation(section_animations_data)
