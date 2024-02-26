ADDRESS = 'localhost'
PORT = '8000'

CONFIG_FILE = 'config.json'
DATABASE_FILE = './db.db'

# Animations
ANIMATION_STEPS = 50 # The more steps, the more accurate flowy transitions, but also more power drawn

ANIMATION_DATA = [
    {
        'name': 'MonoColor',
        'description': 'Monochromatic color switching (different sections possible)'
    },
    {
        'name': 'Flow',
        'description': 'Flowing colors'
    },
    {
        'name': 'Shooter',
        'description': 'Shooting colors'
    },
    {
        'name': 'Strobo',
        'description': 'Strobo effect'
    }
]
