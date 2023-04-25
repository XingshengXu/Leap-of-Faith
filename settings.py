import pygame as pg
pg.init()

"""
The settings module for the "Leap of Faith: The 100-Floor Trials" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""


# Game Play Settings
FPS = 60
NUM_SAW = 16
NUM_WALL = 10
TERRAIN_SPEED = 2
SAW_SPEED = 3
CONVEYOR_SPEED = 2
MOVING_SPEED = 6
FALL_SPEED = 6
MAX_HEALTH = 3
TOP_LEVEL = 100
FRAME_INCREMENT = 1
ANIMATION_INCREMENT = 0.2

# Game Dimensions
WIDTH, HEIGHT = 800, 640  # Game Window Display Dimensions
GAMENAME_HEIGHT = 100  # Game Name Height
GAMESUBNAME_HEIGHT = 200  # Game Subname Height
GAMEMESSAGE_HEIGHT = HEIGHT // 1.25  # Game Message Height
SCOREMESSAGE_HEIGHT = HEIGHT // 1.25  # Score Message Heigh
BG_WIDTH, BG_HEIGHT = 64, 64  # Background Tile Dimensions
WALL_WIDTH, WALL_HEIGHT = 32, 64  # Wall Dimensions
SAW_WIDTH, SAW_HEIGHT = 38, 38  # Saw Dimensions
SAW_SPACING = (WIDTH - WALL_WIDTH * 2 - NUM_SAW * SAW_WIDTH) / \
    (NUM_SAW - 1)  # The Spacing Between Saws
HEART_SPACING = 10  # The Spacing Between HEARTS
LEVEL_DISPLAY_OFFSET = 50  # Level Display Offset
TERRAIN_WIDTH, TERRAIN_HEIGHT = 160, 32  # Terrain Dimensions
TERRAIN_SPAWNLEFT, TERRAIN_SPAWNRIGHT = WALL_WIDTH + \
    TERRAIN_WIDTH // 2, WIDTH - WALL_WIDTH - TERRAIN_WIDTH // 2
# Cutscene of hero's appearing and disappearing Dimensions
CUTSCENE_WIDTH, CUTSCENE_HEIGHT = 96, 96
HERO_X, HERO_Y = WIDTH // 2, 500  # Hero Appear Position
HERO_WIDTH, HERO_HEIGHT = 32, 32  # Hero Dimensions
HERO_SPACING = (WIDTH - 6 * HERO_WIDTH) // 4  # The Spacing Between Heroes
HUD_NUMBER_OFFSET_X, HUD_NUMBER_OFFSET_Y = 20, 80
COLLISION_THRESHOLD = 10  # Collision Threshold
CONVEYOR_WIDTH, CONVEYOR_HEIGHT = 49, 12  # Convetor Tile's Dimensions

# Font
LEVEL_FONT = pg.font.SysFont('comicsans', 50)
TITLE_FONT = pg.font.SysFont('comicsans', 100)
SUBTITLE_FONT = pg.font.SysFont('comicsans', 50)
WIN_FONT = pg.font.SysFont('comicsans', 25)

# Game Events
TERRAIN_SPAWN = pg.USEREVENT + 1
HERO_DIE = pg.USEREVENT + 2
EMPTY_TILE_DESTROY = pg.USEREVENT + 3

# Spawn Frequence and Delay Time
TERRAIN_SPAWN_FREQ = 1000
DELAY_TIME = 3000
EMPTY_TILE_TRIGGER_TIME = 1000

# Image Path
BACKGROUND = 'assets/background/Gray.png'
TOWER_BG = 'assets/background/tower_BG.png'
SAW = 'assets/traps/saw.png'
WALL = 'assets/terrain/wall.png'
HEARTFULL = 'assets/other/heartfull.png'
HEARTEMPTY = 'assets/other/heartempty.png'
HUD_NUMBER = ['assets/other/hud_1.png',
              'assets/other/hud_2.png', 'assets/other/hud_3.png']
HERO_APPEAR = 'assets/maincharacters/appearing.png'
HERO_IDLE = {
    'MaskDude': 'assets/maincharacters/MaskDude/idle.png',
    'NinjaFrog': 'assets/maincharacters/NinjaFrog/idle.png',
    'PinkMan':  'assets/maincharacters/PinkMan/idle.png',
}
HERO_RUN = {
    'MaskDude': 'assets/maincharacters/MaskDude/run.png',
    'NinjaFrog': 'assets/maincharacters/NinjaFrog/run.png',
    'PinkMan':  'assets/maincharacters/PinkMan/run.png',
}
HERO_FALL = {
    'MaskDude': 'assets/maincharacters/MaskDude/fall.png',
    'NinjaFrog': 'assets/maincharacters/NinjaFrog/fall.png',
    'PinkMan':  'assets/maincharacters/PinkMan/fall.png',
}
HERO_HIT = {
    'MaskDude': 'assets/maincharacters/MaskDude/hit.png',
    'NinjaFrog': 'assets/maincharacters/NinjaFrog/hit.png',
    'PinkMan':  'assets/maincharacters/PinkMan/hit.png',
}
TERRAIN = {
    'common_tile': 'assets/terrain/common_tile.png',
    'spike_tile': 'assets/terrain/spike_tile.png',
    'heal_tile': 'assets/terrain/heal_tile.png',
    'empty_tile': 'assets/terrain/empty_tile.png',
    'conveyor_tile_left': 'assets/terrain/conveyor_tile.png',
    'conveyor_tile_right': 'assets/terrain/conveyor_tile.png'
}
TERRAIN_SPAWN_WEIGHTS = [40, 20, 10, 10, 10, 10]

# Sound Path
HEAL_SOUND = 'assets/sound/heal.wav'
STING_SOUND = 'assets/sound/sting.ogg'
MASKDUDE_SOUND = 'assets/sound/maskdude.ogg'
NINJAFROG_SOUND = 'assets/sound/ninjafrog.ogg'
PINKMAN_SOUND = 'assets/sound/pinkman.ogg'
BREAK_SOUND = 'assets/sound/break.flac'
BGM = 'assets/sound/Juhani Junkala.wav'
