ADDRESS = 'localhost'
PORT = '8000'

CONFIG_FILE = 'config.json'
DATABASE_FILE = './db.db'

# Animations
ANIMATION_STEPS = 30 # The more steps, the more accurate flowy transitions, but also more power drawn & slower -> Maximum 40

ANIMATION_DATA = [
    {
        'name': 'MonoColor',
        'description': 'Monochromatic color switching'
    },
    {
        'name': 'Flow',
        'description': 'Flows given colors through the section (Pixel by pixel)'
    },
    {
        'name': 'Shooter',
        'description': 'Shoots given colors through the section (Pixel by pixel)'
    },
    {
        'name': 'Strobe',
        'description': 'Strobe effect'
    },
]
