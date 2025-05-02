from util.database.database import Database


def recreate_animation(animation_data) -> dict:
    return {
        'id': animation_data[0],
        'name': animation_data[1],
        'description': animation_data[2]
    }


def add_animation(id: int, name: str, description: str) -> bool:
    if not Database.push_to_db('INSERT INTO animations VALUES(:id, :name, :description)',
                               {
                                   'id': id,
                                   'name': name,
                                   'description': description
                               }):
        return False

    return True


def remove_animation(id: int) -> bool:
    if not Database.push_to_db('DELETE FROM animations Where id = :id', {'id': id}):
        return False

    return True


def update_animation(id: int, name: str, description: str) -> bool:
    """Update animation by id.
    """
    if not Database.push_to_db('UPDATE animations SET name = :name, description = :description \
                                WHERE id = :id',
                               {
                                   'id': id,
                                   'name': name,
                                   'description': description
                               }):
        return False

    return True


def fetch_animations() -> list:
    animations_data = Database.fetchall_from_db('SELECT id, name, description FROM animations', {})

    if animations_data == None:
        return False

    # Check if multiple animations were fetched
    if type(animations_data) == list:
        # Go through all datasets and recreate animations from data
        animations = []

        for animation_data in animations_data:
            animations.append(recreate_animation(animation_data))

        return animations

    else:
        return [recreate_animation(animations_data)]


def fetch_animation(id: int) -> dict:
    animation_data = Database.fetchone_from_db('SELECT id, name, description FROM animations WHERE id = :id',
                                               {'id': id})

    if animation_data == None:
        return False

    return recreate_animation(animation_data)
