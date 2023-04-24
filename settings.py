import pygame as pg
pg.init()

"""
The settings module for the "Leap of Faith: The 100-Floor Trials" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""

# Game Dimensions
WIDTH, HEIGHT = 800, 640  # Game Window Display Dimensions
GAMENAME_HEIGHT = HEIGHT // 5  # Game Name Height
GAMEMESSAGE_HEIGHT = HEIGHT // 1.25  # Game Message Height
BG_WIDTH, BG_HEIGHT = 64, 64  # Background Tile Dimensions
SAW_WIDTH, SAW_HEIGHT = 38, 38  # Saw Dimensions
WALL_WIDTH, WALL_HEIGHT = 32, 64  # Wall Dimensions
TERRAIN_WIDTH, TERRAIN_HEIGHT = 160, 32  # Terrain Dimensions
# Cutscene of hero's appearing and disappearing Dimensions
CUTSCENE_WIDTH, CUTSCENE_HEIGHT = 96, 96
HERO_X, HERO_Y = WIDTH // 2, 500  # Hero Appear Position
HERO_WIDTH, HERO_HEIGHT = 32, 32  # Hero Dimensions
COLLISION_THRESHOLD = 10  # Collision Threshold

# FPS, Number of Objects, Gravity, and Moving Speed
FPS = 60
NUM_SAW = 16
NUM_WALL = 10
TERRAIN_SPEED = 2
SAW_SPEED = 3
MOVING_SPEED = 6
FALL_SPEED = 6
MAX_HEALTH = 3

# Font
LEVEL_FONT = pg.font.SysFont('comicsans', 50)
TITLE_FONT = pg.font.SysFont('comicsans', 100)

# Game Events
TERRAIN_SPAWN = pg.USEREVENT + 1
HERO_DIE = pg.USEREVENT + 2

# Spawn Frequence and Delay Time
TERRAIN_SPAWN_FREQ = 800
DELAY_TIME = 3000

# Image Path
BACKGROUND = 'assets/background/Gray.png'
SAW = 'assets/traps/saw.png'
WALL = 'assets/terrain/wall.png'
HEARTFULL = 'assets/other/heartfull.png'
HEARTEMPTY = 'assets/other/heartempty.png'
HERO_APPEAR = 'assets/maincharacters/appearing.png'
MASKDUDE_IDLE = 'assets/maincharacters/MaskDude/idle.png'
NINJAFROG_IDLE = 'assets/maincharacters/NinjaFrog/idle.png'
PINKMAN_IDLE = 'assets/maincharacters/PinkMan/idle.png'
MASKDUDE_RUN = 'assets/maincharacters/MaskDude/run.png'
NINJAFROG_RUN = 'assets/maincharacters/NinjaFrog/run.png'
PINKMAN_RUN = 'assets/maincharacters/PinkMan/run.png'
MASKDUDE_FALL = 'assets/maincharacters/MaskDude/fall.png'
NINJAFROG_FALL = 'assets/maincharacters/NinjaFrog/fall.png'
PINKMAN_FALL = 'assets/maincharacters/PinkMan/fall.png'
MASKDUDE_HIT = 'assets/maincharacters/MaskDude/hit.png'
NINJAFROG_HIT = 'assets/maincharacters/NinjaFrog/hit.png'
PINKMAN_HIT = 'assets/maincharacters/PinkMan/hit.png'

TERRAIN = {
    'common_tile': 'assets/terrain/common_tile.png',
    'spike_tile': 'assets/terrain/spike_tile.png',
    'heal_tile': 'assets/terrain/heal_tile1.png',
}
TERRAIN_WEIGHTS = [50, 20, 30]

# Sound Path
HEAL_SOUND = 'assets/sound/heal.wav'
STING_SOUND = 'assets/sound/sting.ogg'
