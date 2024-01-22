from util.database.section import fetch_section, add_section, remove_section, update_section


class Section():
    def __init__(self, name: str,start_led: int= None, end_led: int= None):
        if not start_led or not end_led:
            self.name = name
            self.start_led = start_led
            self.end_led = end_led
        
        else:
            section_data = fetch_section(name)

            self.name = section_data['name']
            self.start_led = section_data['start_led']
            self.end_led = section_data['end_led']

    def sync_changes_to_db(self, new: bool=False) -> bool:
        if new:
            return add_section(self.name, self.start_led, self.end_led)
        
        return update_section(self.name, self.start_led, self.end_led)

    def set_name(self, name) -> bool:
        # Check if section with this name already exists
        if fetch_section(name) != None:
            return False

        if not remove_section(self.name):
            return False

        self.name = name

        if not add_section(self.name, self.start_led, self.end_led):
            return False
        
        return True

    def set_start_led(self, start_led: int):
        self.start_led = start_led

        self.sync_changes_to_db()
        
    def set_end_led(self, end_led: int):
        self.end_led = end_led

        self.sync_changes_to_db()
