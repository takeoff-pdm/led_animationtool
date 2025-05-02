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


def load_scene(scene_id: int) -> bool:
    """Loads all data from scene to workspace (scene-id: -1)
    """
    success = False

    # Sections
    # Remove all section from scene with id = -1
    workspace_sections = fetch_sections(scene_id)  # Workspace is scene with id = -1

    if workspace_sections != False:
        success = True

        for section in workspace_sections:
            remove_section(section['id'])

    sections = fetch_sections(scene_id)  # Fetch sections with scene_id

    # Add fetched sections to scene with id = -1
    if sections != False:
        success = True

        for section in sections:
            add_section(section['id'], section['name'], section['start_led'], section['end_led'])

    # Color Sequences
    # Remove all color sequences from scene with id = -1
    workspace_color_sequences = fetch_color_sequences(scene_id)  # Workspace is scene with id = -1

    if workspace_color_sequences != False:
        success = True

        for color_sequence in workspace_color_sequences:
            remove_color_sequence(color_sequence['id'])
    
    color_sequences = fetch_color_sequences(scene_id)  # Fetch color sequences with scene_id

    # Add fetched color sequences to scene with id = -1
    if color_sequences != False:
        success = True

        for color_sequence in color_sequences:
            add_color_sequence(color_sequence['id'], color_sequence['name'], color_sequence['description'], 
                               color_sequence['selection'], color_sequence['color_amount'])

    # Colors
    # Remove all colors from scene with id = -1
    workspace_colors = fetch_colors(scene_id)  # Workspace is scene with id = -1

    if workspace_colors != False:
        success = True

        for color in workspace_colors:
            remove_color(color['id'])

    colors = fetch_colors(scene_id)  # Fetch colors with scene_id

    # Add fetched colors to scene with id = -1
    if colors != False:
        success = True

        for color in colors:
            add_color(color['id'], color['color_sequence_id'], color['red'], color['green'], 
                      color['blue'], color['position'])

    # Section Animations
    # Remove all section animations from scene with id = -1
    workspace_section_animations = fetch_section_animations(scene_id)  # Workspace is scene with id = -1

    if workspace_section_animations != False:
        success = True

        for section_animation in workspace_section_animations:
            remove_section_animation(section_animation['section_id'], section_animation['animation_id'])

    section_animations = fetch_section_animations(scene_id)  # Fetch section animations with scene_id

    # Add fetched section animations to scene with id = -1
    if section_animations != False:
        success = True

        for section_animation in section_animations:
            add_section_animation(section_animation['id'], section_animation['section_id'], 
                                  section_animation['color_sequence_id'], section_animation['animation_id'])
    
    return success

def save_scene(scene_id: int) -> bool:
    """Saves all data from workspace to scene with id = scene_id
    """
    success = False
    
    # Section Animations
    # Remove all section animations from scene with id = scene_id
    section_animations = fetch_section_animations(scene_id)

    if section_animations != False:
        success = True

        for section_animation in section_animations:
            remove_section_animation(section_animation['section_id'], section_animation['animation_id'], scene_id)

    # Sections
    # Remove all section from scene with id = scene_id
    sections = fetch_sections(scene_id)

    if sections != False:
        success = True

        for section in sections:
            remove_section(section['id'], scene_id)

    # Add fetched sections to scene with id = scene_id
    workspace_sections = fetch_sections(-1)  # Workspace is scene with id = -1

    if workspace_sections != False:
        success = True

        for section in workspace_sections:
            add_section(section['id'], section['name'], section['start_led'], section['end_led'], scene_id)
            
            # Add fetched section animations to scene with id = scene_id
            workspace_section_animations = fetch_section_animations(section['id'], scene_id=-1)

            if workspace_section_animations != False:
                success = True

                for section_animation in workspace_section_animations:
                    add_section_animation(section_animation['section_id'], section_animation['animation_id'], scene_id, 
                                          section_animation['variation'], section_animation['direction'], section_animation['offset'])
    
    # Color Sequences
    # Remove all color sequences from scene with id = scene_id
    color_sequences = fetch_color_sequences(scene_id)

    if color_sequences != False:
        success = True

        for color_sequence in color_sequences:
            remove_color_sequence(color_sequence['id'], scene_id)

    # Add fetched color sequences to scene with id = scene_id
    workspace_color_sequences = fetch_color_sequences(-1)

    if workspace_color_sequences != False:
        success = True

        for color_sequence in workspace_color_sequences:
            add_color_sequence(color_sequence['id'], color_sequence['name'], color_sequence['description'], 
                                color_sequence['selection'], color_sequence['color_amount'], scene_id)
    
    # Colors
    # Remove all colors from scene with id = scene_id
    colors = fetch_colors(scene_id)

    if colors != False:
        success = True

        for color in colors:
            remove_color(color['id'], scene_id)

    # Add fetched colors to scene with id = scene_id
    workspace_colors = fetch_colors(-1)
    
    if workspace_colors != False:
        success = True

        for color in workspace_colors:
            add_color(color['id'], color['color_sequence_id'], color['red'], 
                      color['green'], color['blue'], color['position'], scene_id)

    return success
