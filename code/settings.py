# game setup
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SCALE_FACTOR = 4
WIDTH = WINDOW_WIDTH/SCALE_FACTOR
HEIGHT = WINDOW_HEIGHT/SCALE_FACTOR
FPS = 60
TILESIZE = 16

OVERLAY_TRANSPARENCY = 250

# colours
BG_COLOR = "#15172e"
COLORKEY = (254, 254, 254)
TEXT_COLOR = (255, 255, 255)

# raycasting
MAX_RAY_DIST = 50
RAY_STEP = 2

# debug
TESTING_OVERLAY = False

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/Minecraftia-Regular.ttf'
UI_FONT_SIZE = 18
UI_BG_COLOR = '#222222'
UI_BORDER_COLOUR = '#111111'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOUR_ACTIVE = 'gold'

#enemy
monster_data = {
    'stalker':{'health':100,'exp': 100,'damage':2,'attack_type':'poop','attack_sound':'graphics/audio/fart-with-reverb-39675.mp3','sprite_path': 'graphics/player/Untitled_Artwork 12.png','speed':1,'resistance':3,'attack_radius':80,'notice_radius':360},
    'blind': {'health':100,'exp': 100,'damage':2,'attack_type':'poop','attack_sound':'graphics/audio/fart-with-reverb-39675.mp3','sprite_path': 'graphics/player/Untitled_Artwork 11.png','speed':1,'resistance':3,'attack_radius':80,'notice_radius':360}
}



WORLD_MAP = [
    [
        'x', 'x', 'x', 'x', 'x', 'x', 'x', ' ', 'x', 'x', 'x', 'x', 'x', 'x',
        'x', 'x', 'x', 'x', 'x', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', 'p', 'b', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', 's', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x',
        'x', 'x', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ', ' ', 'x'
    ],
    [
        'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
        'x', 'x', 'x', 'x', 'x', 'x'
    ],
]
