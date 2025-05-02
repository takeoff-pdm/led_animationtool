from util.database.database import Database
from util.database.scene import fetch_scene, add_scene, update_scene, load_scene, save_scene
from util.database.scene_animation import fetch_scene_animations_from_scene, remove_scene_animations, add_scene_animation


class Scene:
    def __init__(self, id: int | None = None, name: str | None = None,
                 description: str | None = None, scene_animations: list = []):
        self.id = id
        self.scene_animations = scene_animations

        if name != None and description != None:
            self.name = name
            self.description = description

        elif self.id != None:
            scene_data = fetch_scene(self.id)

            if scene_data:  # Check if scene exists
                self.name = scene_data['name']
                self.description = scene_data['description']

        if len(self.scene_animations) == 0:  # Fetch animations to run
            scene_animations_data = fetch_scene_animations_from_scene(self.id)

            if scene_animations_data:
                self.scene_animations = scene_animations_data

    def sync_changes_to_db(self, new: bool = False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM scenes', {})[0]

            self.id = 0
            if max_id != None:
                self.id = max_id + 1

            return add_scene(self.id, self.name, self.description)

        return update_scene(self.id, self.name, self.description)

    def load(self) -> list | bool:
        """Load scene into workspace and return running animations.
        """
        if not load_scene(self.id):
            return False

        return self.scene_animations

    def save(self, running_animations: list) -> bool:
        """Save scene to database.
        """
        remove_scene_animations(self.id)
        
        for animation in running_animations:
            # 'scene_id': scene_animation_data[0],
            # 'animation_id': scene_animation_data[1],
            # 'section_id': scene_animation_data[2],
            # 'color_sequence_id': scene_animation_data[3]
            if animation.color_sequence == None:
                continue
            
            add_scene_animation(self.id, animation.id, animation.section_id, animation.color_sequence.id)
            
        if len(self.scene_animations) == 0:  # Fetch animations to run
            scene_animations_data = fetch_scene_animations_from_scene(self.id)

            if scene_animations_data:
                self.scene_animations = scene_animations_data
        
        return save_scene(self.id)
