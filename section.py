from util.database.section import fetch_section, add_section, remove_section, update_section


class Section():
    def __init__(self, id: int, name: str = None, start_led: int = None, end_led: int = None):
        self.id = id
        
        if name and start_led and end_led:
            self.name = name
            self.start_led = start_led
            self.end_led = end_led
        
        else:
            section_data = fetch_section(id)

            self.name = section_data['name']
            self.start_led = section_data['start_led']
            self.end_led = section_data['end_led']

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            return add_section(self.name, self.start_led, self.end_led)
        
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
