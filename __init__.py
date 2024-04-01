ADDRESS = 'localhost'
PORT = '8000'

CONFIG_FILE = 'config.json'
DATABASE_FILE = './db.db'

# Animations
ANIMATION_STEPS = 30  # The more steps, the more accurate flowy transitions, but also more power drawn & slower ->
                      # Maximum 40

ANIMATION_DATA = [
    {
        'name': 'MonoColor',
        'description': 'Monochromatic color switching. Variation 1: No fade; Variation 2: Fade out'
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
        'description': 'Strobe effect. Variation 1: All blinks shortly after each other; Variation 2: All blinks are equally distributed'
    },
    {
        'name': 'Squeeze',
        'description': 'Squeeze section more in more to one side/into the center'
    }
]
