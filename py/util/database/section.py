from util.database.database import Database
from util.database.section_animation import add_section_animations


def recreate_section(section_data) -> dict:
    return {
        'id': section_data[0],
        'name': section_data[1],
        'start_led': section_data[2],
        'end_led': section_data[3]
    }


def add_section(id: int, name: str, start_led: int, end_led: int, scene_id: int = -1) -> bool:
    # print((Database.fetchone_from_db('SELECT MAX(id) FROM sections', {}) 
    #                                       if not None and not (None,) else :scene_id) + 1)
    if not Database.push_to_db('INSERT INTO sections VALUES(:scene_id, :id, :name, :start_led, :end_led)',
                               {
                                   'scene_id': scene_id,
                                   'id': id,
                                   'name': name,
                                   'start_led': start_led,
                                   'end_led': end_led
                               }):
        return False

    if not add_section_animations(id):
        return False

    return True


def remove_section(id: int, scene_id: int = -1) -> bool:
    if not Database.push_to_db('DELETE FROM sections WHERE scene_id = :scene_id AND id = :id',
                               {
                                   'id': id,
                                   'scene_id': scene_id
                               }):
        return False

    return True


def update_section(id: int, name: str, start_led: int, end_led: int, scene_id: int = -1) -> bool:
    """Update section by name.
    """
    if not Database.push_to_db('UPDATE sections SET name = :name, start_led = :start_led, end_led = :end_led \
                                WHERE scene_id = :scene_id AND id = :id',
                               {
                                   'id': id,
                                   'name': name,
                                   'start_led': start_led,
                                   'end_led': end_led,
                                    'scene_id': scene_id
                               }):
        return False

    return True


def fetch_sections(scene_id: int = -1) -> list | bool:
    sections_data = Database.fetchall_from_db('SELECT id, name, start_led, end_led FROM sections \
                                               WHERE scene_id = :scene_id',
                                              {'scene_id': scene_id})

    if sections_data == None:
        return False

    # Check if multiple sections were fetched
    if type(sections_data) == list:
        # Go through all datasets and recreate sections from data
        sections = []

        for section_data in sections_data:
            sections.append(recreate_section(section_data))

        return sections

    else:
        return [recreate_section(sections_data)]


def fetch_section(id: int, scene_id: int = -1) -> dict | bool:
    section_data = Database.fetchone_from_db('SELECT id, name, start_led, end_led FROM sections \
                                              WHERE scene_id = :scene_id AND id = :id',
                                             {
                                                 'id': id,
                                                 'scene_id': scene_id
                                             })

    if section_data == None:
        return False

    return recreate_section(section_data)
