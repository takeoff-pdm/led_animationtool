from util.database.database import Database


def recreate_scene_animation(scene_animation_data):
    return {
        'scene_id': scene_animation_data[0],
        'animation_id': scene_animation_data[1],
        'section_id': scene_animation_data[2],
        'color_sequence_id': scene_animation_data[3]
    }


def add_scene_animation(scene_id: int, animation_id: int, section_id: int, color_sequence_id: int) -> bool:
    if not Database.push_to_db('INSERT INTO scenes VALUES(:scene_id, :animation_id, :section_id, :color_sequence_id)',
                               {
                                   'scene_id': scene_id,
                                   'animation_id': animation_id,
                                   'section_id': section_id,
                                   'color_sequence_id': color_sequence_id
                               }):
        return False

    return True


def remove_scene_animations(scene_id: int) -> bool:
    if not Database.push_to_db('DELETE FROM scenes WHERE scene_id = :scene_id',
                               {'scene_id': scene_id}):
        return False

    return True


def remove_scene_animation(scene_id: int, animation_id: int) -> bool:
    if not Database.push_to_db('DELETE FROM scenes WHERE scene_id = :scene_id AND animation_id = :animation_id',
                               {
                                   'scene_id': scene_id,
                                   'animation_id': animation_id
                               }):
        return False

    return True


def update_scene_animation(scene_id: int, animation_id: int, section_id: int, color_sequence_id: int) -> bool:
    """Update scene-animation by scene-id and animation-id.
    """
    if not Database.push_to_db('UPDATE scenes SET section_id = :section_id, color_sequence_id = :color_sequence_id \
                                WHERE scene_id = :scene_id',
                               {
                                   'scene_id': scene_id,
                                   'animation_id': animation_id,
                                   'section_id': section_id,
                                   'color_sequence_id': color_sequence_id
                               }):
        return False

    return True


def fetch_scene_animations() -> list:
    scene_animations_data = Database.fetchall_from_db('SELECT scene_id, animation_id, section_id, color_sequence_id \
                                                       FROM scenes', {})

    if scene_animations_data == None:
        return False

    # Check if multiple scene-animations were fetched
    if type(scene_animations_data) == list:
        # Go through all datasets and recreate scene-animations from data
        scene_animations = []

        for scene_animation_data in scene_animations_data:
            scene_animations.append(recreate_scene_animation(scene_animation_data))

        return scene_animations

    else:
        return [recreate_scene_animation(scene_animations_data)]


def fetch_scene_animations_from_scene(scene_id: int) -> dict:
    scene_animations_data = Database.fetchone_from_db('SELECT scene_id, animation_id, section_id, color_sequence_id \
                                                       FROM scenes WHERE scene_id = :scene_id',
                                                      {'scene_id': scene_id})

    if scene_animations_data == None:
        return False

    # Check if multiple scene-animations were fetched
    if type(scene_animations_data) == list:
        # Go through all datasets and recreate scene-animations from data
        scene_animations = []

        for scene_animation_data in scene_animations_data:
            scene_animations.append(recreate_scene_animation(scene_animation_data))

        return scene_animations

    else:
        return [recreate_scene_animation(scene_animations_data)]


def fetch_scene_animation(scene_id: int, animation_id: int) -> dict:
    scene_animation_data = Database.fetchone_from_db('SELECT scene_id, animation_id, section_id, color_sequence_id \
                                                      FROM scenes WHERE scene_id = :scene_id \
                                                      AND animation_id = :animation_id',
                                                     {
                                                         'scene_id': scene_id,
                                                         'animation_id': animation_id
                                                     })

    if scene_animation_data == None:
        return False

    return recreate_scene_animation(scene_animation_data)
