from os import listdir
from random import choice, randint, random
from sys import exit
import pygame as pg
from settings import *

pg.init()


def flip(images):
    return [pg.transform.flip(image, True, False) for image in images]


def load_image_sheets(img_path, width, height, need_scale=False):
    image = pg.image.load(img_path).convert_alpha()
    image_num = image.get_width() // width

    images = []
    for i in range(image_num):
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        rect = pg.Rect(i * width, 0, width, height)
        surface.blit(image, (0, 0), rect)
        if need_scale:
            surface = pg.transform.scale2x(surface)
        images.append(surface)
    return images


class Hero(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_count = 0
        self.cutscene_played = False
        self.direction = "left"
        self.idle = True

        # Load Hero Appear Image
        self.hero_appear_img = load_image_sheets(
            HERO_APPEAR, CUTSCENE_WIDTH, CUTSCENE_HEIGHT, True)
        self.image = self.hero_appear_img[self.animation_count]
        self.rect = self.image.get_rect(
            midbottom=(WIDTH // 2, HEIGHT + WALL_HEIGHT))

        # Load Hero Idle Image
        self.hero_idle_right_img = load_image_sheets(
            MASKDUDE_IDLE, HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_idle_left_img = flip(self.hero_idle_right_img)

        # Load Hero Run Image
        self.hero_run_right_img = load_image_sheets(
            MASKDUDE_RUN, HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_run_left_img = flip(self.hero_run_right_img)

    def hero_appear(self):
        if self.animation_count >= len(self.hero_appear_img):
            self.animation_count = 0
            self.cutscene_played = True
            self.image = self.hero_idle_left_img[int(
                self.animation_count)]
            self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT))
        else:
            self.image = self.hero_appear_img[int(self.animation_count)]

    def hero_run(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.idle = False
            self.direction = 'left'
            self.rect.x -= MOVING_SPEED
        elif key[pg.K_RIGHT]:
            self.idle = False
            self.direction = 'right'
            self.rect.x += MOVING_SPEED
        else:
            self.idle = True
            self.animation_count = 0

    def animation(self):
        img_list = {
            ('idle', 'left'): self.hero_idle_left_img,
            ('idle', 'right'): self.hero_idle_right_img,
            ('run', 'left'): self.hero_run_left_img,
            ('run', 'right'): self.hero_run_right_img,
        }

        if self.idle:
            state = 'idle'
        else:
            state = 'run'
        images = img_list[(state, self.direction)]
        if self.animation_count >= len(images):
            self.animation_count = 0
        self.image = images[int(self.animation_count)]

    def update(self):
        self.animation_count += 0.2
        if not self.cutscene_played:
            self.hero_appear()
        else:
            self.hero_run()
            self.animation()


class Game:

    def __init__(self):
        self.game_active = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        pg.display.set_caption('Leap of Faith: The 100-Floor Trials')
        self.saw_index = 0
        self.frame_counter = 0
        self.saw_spacing = (WIDTH - WALL_WIDTH * 2 -
                            NUM_SAW * SAW_WIDTH) / (NUM_SAW - 1)
        self.wall_offset = 0

        # Load Background Image
        self.background = pg.image.load(BACKGROUND).convert()
        self.saw = load_image_sheets(SAW, SAW_WIDTH, SAW_HEIGHT)
        self.wall = pg.transform.scale(pg.image.load(
            WALL).convert(), (WALL_WIDTH, WALL_HEIGHT))

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
            x_pos = i * (self.saw_spacing + SAW_WIDTH)
            self.screen.blit(
                self.saw[self.saw_index], (x_pos + WALL_WIDTH, -SAW_HEIGHT // 2))
        if self.frame_counter % SAW_SPEED == 0:
            self.saw_index = (self.saw_index + 1) % len(self.saw)

        # Draw Wall
        for j in range(NUM_WALL + 1):
            y_pos = self.wall_offset + j * WALL_HEIGHT
            left_wall_x = 0
            right_wall_x = WIDTH - WALL_WIDTH
            self.screen.blit(self.wall, (left_wall_x, y_pos))
            self.screen.blit(self.wall, (right_wall_x, y_pos))

        # Update wall position and reset it when disappears
        self.wall_offset -= TERRAIN_SPEED
        if self.wall_offset <= -WALL_HEIGHT:
            self.wall_offset = 0

    def main_loop(self):
        while True:
            self.clock.tick(FPS)
            self.frame_counter += 1

            # Handle Events
            self.handle_events()

            # Display Game Backgrounds and Objects
            self.draw_background()

            hero.draw(self.screen)

            # Update Sprites
            hero.update()

            pg.display.update()


# Create Class Instances and Add Sprites
game = Game()

hero = pg.sprite.GroupSingle()
hero.add(Hero())

# Run Main Loop
game.main_loop()
