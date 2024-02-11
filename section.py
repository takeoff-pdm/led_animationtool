from util.database.database import Database
from util.database.section import fetch_section, add_section, remove_section, update_section


class Section():
    def __init__(self, id: int = None, name: str = None, start_led: int = None, end_led: int = None):
        self.id = id
        print(name, start_led, end_led)
        
        if name != None and start_led != None and end_led != None:
            self.name = name
            self.start_led = start_led
            self.end_led = end_led
        
        elif self.id != None:
            section_data = fetch_section(self.id)

            self.name = section_data['name']
            self.start_led = section_data['start_led']
            self.end_led = section_data['end_led']

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            max_id = Database.fetchone_from_db('SELECT MAX(id) FROM sections', {})[0]
            
            self.id = 0
            if max_id != None:
                self.id = max_id + 1
            
            return add_section(self.id, self.name, self.start_led, self.end_led)
        
        return update_section(self.id, self.name, self.start_led, self.end_led)

    # def set_name(self, name) -> bool:
    #     self.name = name

    #     return self.sync_changes_to_db()

    # def set_start_led(self, start_led: int) -> bool:
    #     self.start_led = start_led

    #     return self.sync_changes_to_db()
        
    # def set_end_led(self, end_led: int) -> bool:
    #     self.end_led = end_led

    #     return self.sync_changes_to_db()
