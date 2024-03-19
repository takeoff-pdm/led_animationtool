from util.database.database import Database

from util.database.section import fetch_sections, remove_section, add_section
from util.database.color import fetch_colors, remove_color, add_color
from util.database.color_sequence import fetch_color_sequences, remove_color_sequence, add_color_sequence
from util.database.section_animation import fetch_section_animations, remove_section_animation, add_section_animation


def recreate_scene(scene_data) -> dict:
    return {
        'id': scene_data[0],
        'name': scene_data[1],
        'description': scene_data[2]
    }


def add_scene(id: int, name: str, description: str) -> bool:
    if not Database.push_to_db('INSERT INTO scenes VALUES(:id, :name, :description)',
                               {
                                   'id': id,
                                   'name': name,
                                   'description': description
                               }):
        return False

    return True


def remove_scene(id: int) -> bool:
    if not Database.push_to_db('DELETE FROM scenes Where id = :id', {'id': id}):
        return False

    return True


def update_scene(id: int, name: str, description: str) -> bool:
    """Update scnee by id.
    """
    if not Database.push_to_db('UPDATE scenes SET name = :name, description = :description WHERE id = :id',
                               {
                                   'id': id,
                                   'name': name,
                                   'description': description
                               }):
        return False

    return True


def fetch_scenes() -> list:
    scenes_data = Database.fetchall_from_db('SELECT id, name, description FROM scenes', {})

    if scenes_data == None:
        return False

    # Check if multiple scenes were fetched
    if type(scenes_data) == list:
        # Go through all datasets and recreate scenes from data
        scenes = []

        for scene_data in scenes_data:
            scenes.append(recreate_scene(scene_data))

        return scenes

    else:
        return [recreate_scene(scenes_data)]


def fetch_scene(id: int) -> dict:
    scene_data = Database.fetchone_from_db('SELECT id, name, description FROM scenes WHERE id = :id',
                                           {'id': id})

    if scene_data == None:
        return False

    return recreate_scene(scene_data)


def load(scene_id: int):
    """Loads all data from scene to workspace (scene-id: -1)
    """
    # Sections
    # Remove all section from scene with id = -1

    # Fetch sections with scene_id

    # Add fetched sections to scene with id = -1
