import pygame as pg
pg.init()

"""
The settings module for the "Leap of Faith: The 100-Floor Trials" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""

# Game Dimensions
WIDTH, HEIGHT = 800, 640  # Game Window Display Dimensions
BG_WIDTH, BG_HEIGHT = 64, 64  # Background Tile Dimensions
SAW_WIDTH, SAW_HEIGHT = 38, 38  # Saw Dimensions
WALL_WIDTH, WALL_HEIGHT = 32, 64  # Wall Dimensions

# FPS, Gravity, and Moving Speed
FPS = 60
NUM_SAW = 8
NUM_WALL = 10
TERRAIN_SPEED = 5

# Image Path
BACKGROUND = 'assets/background/Brown.png'
SAW = 'assets/traps/saw.png'
WALL = 'assets/terrain/wall.png'
