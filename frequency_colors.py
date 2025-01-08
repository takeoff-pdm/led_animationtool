from util.database.frequency_color import fetch_frequency_color, update_frequency_color, add_frequency_color, remove_frequency_color
from util.database.database import Database


class FrequencyColors:
    def __init__(self, scene_id: int | None = None, color_sequence_id_1: int | None = None, 
                        color_sequence_id_2: int | None = None, color_sequence_id_3: int | None = None):
        self.scene_id = scene_id
        
        if scene_id != None and color_sequence_id_1 != None and color_sequence_id_2 != None and color_sequence_id_3 != None:
            self.color_sequence_id_1 = color_sequence_id_1
            self.color_sequence_id_2 = color_sequence_id_2
            self.color_sequence_id_3 = color_sequence_id_3
        
        elif self.scene_id != None:
            frequency_color_data = fetch_frequency_color(self.scene_id)

            if not frequency_color_data:
                self.sync_changes_to_db(new=True)
                
                self.color_sequence_id_1 = 0
                self.color_sequence_id_2 = 0
                self.color_sequence_id_3 = 0

            self.color_sequence_id_1 = frequency_color_data['color_sequence_id_1']
            self.color_sequence_id_2 = frequency_color_data['color_sequence_id_2']
            self.color_sequence_id_3 = frequency_color_data['color_sequence_id_3']
    
    def sync_changes_to_db(self, new: bool = False) -> bool:
        if new:
            return add_frequency_color(self.scene_id, self.color_sequence_id_1, 
                                       self.color_sequence_id_2, self.color_sequence_id_3)
        
        return update_frequency_color(self.scene_id, self.color_sequence_id_1, 
                                      self.color_sequence_id_2, self.color_sequence_id_3)
