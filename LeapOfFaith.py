from os import listdir
from random import choice, randint, random
from sys import exit
import pygame as pg
from settings import *

pg.init()


def load_image_sheets(img_path, width, height):
    image = pg.image.load(img_path)
    sprite_num = image.get_width() // width

    sprites = []
    for i in range(sprite_num):
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        rect = pg.Rect(i * width, 0, width, height)
        surface.blit(image, (0, 0), rect)
        sprites.append(pg.transform.scale2x(surface))
    return sprites


def load_images(img_path, need_alpha=False, need_scale=False, size=None):
    if need_alpha:
        image = pg.image.load(img_path).convert()
    else:
        image = pg.image.load(img_path).convert_alpha()
    if need_scale and size is not None:
        image = pg.transform.scale(image, size)
    return image


class Game:

    def __init__(self):
        self.game_active = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        pg.display.set_caption('Leap of Faith: The 100-Floor Trials')
        self.saw_index = 0
        self.saw_spacing = (WIDTH - WALL_WIDTH * 2 -
                            NUM_SAW * SAW_WIDTH * 2) / (NUM_SAW - 1)
        self.wall_y = 0

        # Load Background Image
        self.background = load_images(BACKGROUND)
        self.saw = load_image_sheets(SAW, SAW_WIDTH, SAW_HEIGHT)
        self.wall = load_images(WALL, False, True, (WALL_WIDTH, WALL_HEIGHT))

    def handle_events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def draw_background(self):
        # Draw Background
        for x in range(0, WIDTH, BG_WIDTH):
            for y in range(0, HEIGHT, BG_HEIGHT):
                self.screen.blit(self.background, (x, y))

        # Draw Saws
        for i in range(NUM_SAW):
            x_pos = i * (self.saw_spacing + SAW_WIDTH * 2)
            self.screen.blit(
                self.saw[self.saw_index], (x_pos + WALL_WIDTH, -SAW_HEIGHT))
        self.saw_index = (self.saw_index + 1) % len(self.saw)

        # Draw Wall
        for j in range(NUM_WALL + 1):
            y_pos = self.wall_y + j * WALL_HEIGHT
            left_wall_x = 0
            right_wall_x = WIDTH - WALL_WIDTH
            self.screen.blit(self.wall, (left_wall_x, y_pos))
            self.screen.blit(self.wall, (right_wall_x, y_pos))

        # Update wall position and reset it when disappears
        self.wall_y -= TERRAIN_SPEED
        if self.wall_y <= -WALL_HEIGHT:
            self.wall_y = 0

    def main_loop(self):
        while True:
            self.clock.tick(FPS)

            # Handle Events
            self.handle_events()

            # Display Game Backgrounds and Objects
            self.draw_background()
            pg.display.update()


# Create Class Instances and Add Sprites
game = Game()

# Run Main Loop
game.main_loop()
