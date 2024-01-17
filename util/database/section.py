from util.database.database import Database

def recreate_section(section_data):
    return {
        'name': section_data[0],
        'start_led': section_data[1],
        'end_led': section_data[2]
    }

def add_section(name: str, start_led: int, end_led: int) -> bool:
    if not Database.push_to_db('INSERT INTO sections VALUES(:name, :start_led, :end_led)', 
                                  {'name': name, 'start_led': start_led, 'end_led': end_led}):
        return False
    
    return True

def remove_section(name: str):
    if not Database.push_to_db('DELETE FROM sections Where name = :name', {'name': name}):
        return False
    
    return True

def fetch_sections():
    sections_data = Database.fetchall_from_db('SELECT name, start_led, end_led FROM sections', {})

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

def fetch_section(name: str):
    section_data = Database.fetchone_from_db('SELECT name, start_led, end_led FROM sections \
                                              WHERE name = :name', {'name': name})

    if section_data == None:
        return False

    return recreate_section(section_data)
