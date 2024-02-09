from util.database.database import Database

def recreate_section(section_data) -> dict:
    return {
        'id': section_data[0],
        'name': section_data[1],
        'start_led': section_data[2],
        'end_led': section_data[3]
    }

def add_section(name: str, start_led: int, end_led: int) -> bool:
    if not Database.push_to_db('INSERT INTO sections VALUES(:name, :start_led, :end_led)', 
                                  { 
                                    'id': Database.fetchone_from_db('SELECT MAX(id) FROM sections', {}) 
                                          if not None else 0 + 1,
                                    'name': name, 
                                    'start_led': start_led, 
                                    'end_led': end_led
                                  }):
        return False
    
    return True

def remove_section(id: int) -> bool:
    if not Database.push_to_db('DELETE FROM sections Where id = :id', {'id': id}):
        return False
    
    return True

def update_section(id: int, name: str, start_led: int, end_led: int) -> bool:
    '''Update section by name.
    '''
    if not Database.push_to_db('UPDATE sections SET name = :name, start_led = :start_led, end_led = :end_led \
                                WHERE id = :id', 
                                  {'id': id, 'name': name, 'start_led': start_led, 'end_led': end_led}):
        return False
    
    return True

def fetch_sections() -> list | bool:
    sections_data = Database.fetchall_from_db('SELECT id, name, start_led, end_led FROM sections', {})

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
        return [ recreate_section(sections_data) ]

def fetch_section(id: int) -> dict | bool:
    section_data = Database.fetchone_from_db('SELECT id, name, start_led, end_led FROM sections \
                                              WHERE id = :id', {'id': id})

    if section_data == None:
        return False

    return recreate_section(section_data)
