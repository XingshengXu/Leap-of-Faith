from random import choices, randint
from sys import exit
import pygame as pg
from settings import *

pg.init()


def flip(images):
    """Flips a list of images horizontally."""
    return [pg.transform.flip(image, True, False) for image in images]


def load_image_sheets(img_path, width, height, needScale=False, customScale=False, size=None):
    """Splits an image into multiple sub-images (sprites) based on the given width and height, 
    and optionally scales them."""
    image = pg.image.load(img_path).convert_alpha()
    image_num = image.get_width() // width

    images = []
    for i in range(image_num):
        surface = pg.Surface((width, height), pg.SRCALPHA, depth=32)
        rect = pg.Rect(i * width, 0, width, height)
        surface.blit(image, (0, 0), rect)
        if needScale:
            surface = pg.transform.scale2x(surface)
        elif customScale:
            surface = pg.transform.scale(surface, size)
        images.append(surface)
    return images


def render_font(text, font, color, center):
    """Renders a given text using the specified font and color."""
    rendered_text = font.render(text, True, color)
    rendered_text_rect = rendered_text.get_rect(center=center)
    return rendered_text, rendered_text_rect


class Hero(pg.sprite.Sprite):
    """A class representing the Hero. 
    It represents a game character with various attributes, 
    such as health and direction, and actions, such as running, 
    falling, and dying, as well as handling animations for different 
    states like idle, running, and falling."""

    def __init__(self, heroType):
        super().__init__()
        self.animation_count = 0
        self.cutscene_played = False
        self.health = MAX_HEALTH
        self.direction = "left"
        self.run = False
        self.fall = False
        self.hit = False

        # Load Hero Appear Image
        self.hero_appear_img = load_image_sheets(
            HERO_APPEAR, CUTSCENE_WIDTH, CUTSCENE_HEIGHT, True)
        self.image = self.hero_appear_img[self.animation_count]
        self.rect = self.image.get_rect(
            midbottom=(HERO_X, HERO_Y))

        # Load Hero Idle Image
        self.hero_idle_right_img = load_image_sheets(
            HERO_IDLE[heroType], HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_idle_left_img = flip(self.hero_idle_right_img)

        # Load Hero Run Image
        self.hero_run_right_img = load_image_sheets(
            HERO_RUN[heroType], HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_run_left_img = flip(self.hero_run_right_img)

        # Load Hero Fall Image
        self.hero_fall_right_img = load_image_sheets(
            HERO_FALL[heroType], HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_fall_left_img = flip(self.hero_fall_right_img)

        # Load Hero Hit Image
        self.hero_hit_right_img = load_image_sheets(
            HERO_HIT[heroType], HERO_WIDTH, HERO_HEIGHT, True)
        self.hero_hit_left_img = flip(self.hero_hit_right_img)

    def hero_appear(self):
        if self.animation_count >= len(self.hero_appear_img):
            self.animation_count = 0
            self.cutscene_played = True
            self.image = self.hero_idle_left_img[int(
                self.animation_count)]
            self.rect = self.image.get_rect(
                midbottom=(HERO_X, HERO_Y))
        else:
            self.image = self.hero_appear_img[int(self.animation_count)]

    def hero_run(self):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.rect.left - MOVING_SPEED >= WALL_WIDTH:
            self.run = True
            self.direction = 'left'
            self.rect.x -= MOVING_SPEED
        elif key[pg.K_RIGHT] and self.rect.right + MOVING_SPEED <= WIDTH - WALL_WIDTH:
            self.run = True
            self.direction = 'right'
            self.rect.x += MOVING_SPEED
        else:
            self.run = False

    def hero_fall(self):
        if self.fall:
            self.rect.y += FALL_SPEED

    def hero_die(self):
        if (self.rect.top <= SAW_HEIGHT // 3) or (self.rect.top >= HEIGHT):
            self.health = 0
            pg.event.post(pg.event.Event(HERO_DIE))

    def animation(self):
        img_list = {
            ('idle', 'left'): self.hero_idle_left_img,
            ('idle', 'right'): self.hero_idle_right_img,
            ('run', 'left'): self.hero_run_left_img,
            ('run', 'right'): self.hero_run_right_img,
            ('fall', 'left'): self.hero_fall_left_img,
            ('fall', 'right'): self.hero_fall_right_img,
            ('hit', 'left'): self.hero_hit_left_img,
            ('hit', 'right'): self.hero_hit_right_img,
        }

        if self.hit:
            state = 'hit'
        elif self.fall:
            state = 'fall'
        elif self.run:
            state = 'run'
        else:
            state = 'idle'

        images = img_list[(state, self.direction)]
        if self.animation_count >= len(images):
            if state == 'hit':
                self.hit = False
            self.animation_count = 0
        self.image = images[int(self.animation_count)]

    def update(self):
        self.animation_count += 0.2
        if not self.cutscene_played:
            self.hero_appear()
        else:
            self.hero_die()
            self.hero_fall()
            self.hero_run()
            self.animation()


class Terrain(pg.sprite.Sprite):
    """A class representing the Terrain.
    Its main functions include initializing the terrain object 
    with its properties, updating its position and animation, 
    and destroying the object when it goes out of bounds."""

    def __init__(self, terrainType, pos):
        super().__init__()
        self.type = terrainType
        self.has_dealt_damage = False
        self.has_dealt_heal = False
        self.has_trigger = False
        self.animation_count = 0

        # Load Terrain Image
        if self.type in ['conveyor_tile_right', 'conveyor_tile_left']:
            self.conveyor_img = load_image_sheets(
                TERRAIN[self.type], CONVEYOR_WIDTH, CONVEYOR_HEIGHT,
                customScale=True, size=(TERRAIN_WIDTH, TERRAIN_HEIGHT))
            if self.type == 'conveyor_tile_left':
                self.conveyor_img = flip(self.conveyor_img)
            self.image = self.conveyor_img[self.animation_count]
        else:
            self.image = pg.transform.scale(pg.image.load(
                TERRAIN[self.type]).convert(), (TERRAIN_WIDTH, TERRAIN_HEIGHT))
        self.rect = self.image.get_rect(midtop=pos)

    def terrain_move(self):
        self.rect.y -= TERRAIN_SPEED

        if self.type in ('conveyor_tile_right', 'conveyor_tile_left'):
            if self.animation_count >= len(self.conveyor_img):
                self.animation_count = 0
            self.image = self.conveyor_img[int(self.animation_count)]

    def destroy(self):
        if self.rect.y <= -TERRAIN_HEIGHT:
            self.kill()

    def update(self):
        self.animation_count += 0.2
        self.terrain_move()
        self.destroy()


class Game:
    """Main game class for Leap of Faith.
    It is responsible for handling game mechanics, including initialization, 
    loading resources, updating game states, handling events, and rendering graphics. 
    The main loop of the game continuously executes, updating game states 
    and drawing elements on the screen."""

    def __init__(self):
        self.setup()
        self.load_resources()

    def setup(self):
        self.game_active = False
        self.clock = pg.time.Clock()
        self.saw_index = 0
        self.frame_counter = 0
        self.animation_count = 0
        self.wall_offset = 0
        self.level = TOP_LEVEL
        self.fall_dist = 0
        self.hero_prevPos = HERO_Y
        self.triggered_empty_tiles = []
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Leap of Faith: The 100-Floor Trials')
        pg.time.set_timer(TERRAIN_SPAWN, TERRAIN_SPAWN_FREQ)

    def load_resources(self):
        self.load_fonts()
        self.load_images()
        self.load_sounds()

    def load_fonts(self):
        self.game_mainName, self.game_mainName_rect = render_font(
            'Leap of Faith', TITLE_FONT, 'darkgoldenrod1', (WIDTH // 2, GAMENAME_HEIGHT))
        self.game_subName, self.game_subName_rect = render_font(
            'The 100-Floor Trials', SUBTITLE_FONT, 'darkgoldenrod1', (WIDTH // 2, GAMESUBNAME_HEIGHT))
        self.game_message, self.game_message_rect = render_font(
            'Choose a hero to play!', SUBTITLE_FONT, 'red', (WIDTH // 2, GAMEMESSAGE_HEIGHT))
        self.win_message, self.win_message_rect = render_font(
            "My hero, you've completed the leap of faith! Congratulations!", WIN_FONT, 'red', (WIDTH // 2, SCOREMESSAGE_HEIGHT))

    def load_images(self):

        # Load BackGround Images
        self.background = pg.image.load(BACKGROUND).convert()
        self.tower_BG = pg.transform.scale(
            pg.image.load(TOWER_BG).convert(), (WIDTH, HEIGHT))
        self.saw = load_image_sheets(SAW, SAW_WIDTH, SAW_HEIGHT)
        self.wall = pg.transform.scale(pg.image.load(
            WALL).convert(), (WALL_WIDTH, WALL_HEIGHT))

        # Load HUD
        self.hud_number = [pg.image.load(HUD_NUMBER[i]).convert_alpha()
                           for i in range(len(HUD_NUMBER))]
        self.hero_initImgs = [load_image_sheets(HERO_IDLE[hero_name],
                                                HERO_WIDTH, HERO_HEIGHT, True)
                              for hero_name in ['MaskDude', 'NinjaFrog', 'PinkMan']]
        self.heart_full = pg.image.load(HEARTFULL).convert_alpha()
        self.heart_empty = pg.image.load(HEARTEMPTY).convert_alpha()

    def load_sounds(self):
        pg.mixer.music.load(BGM)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        self.heal_sound = pg.mixer.Sound(HEAL_SOUND)
        self.sting_sound = pg.mixer.Sound(STING_SOUND)
        self.break_sound = pg.mixer.Sound(BREAK_SOUND)
        self.maskdude_sound = pg.mixer.Sound(MASKDUDE_SOUND)
        self.ninjafrog_sound = pg.mixer.Sound(NINJAFROG_SOUND)
        self.pinkman_sound = pg.mixer.Sound(PINKMAN_SOUND)

    def reset_game(self, hero_type):
        self.game_active = True
        self.frame_counter = 0
        self.saw_index = 0
        self.animation_count = 0
        self.level = TOP_LEVEL
        self.fall_dist = 0
        self.hero_prevPos = HERO_Y
        hero.empty()
        terrains.empty()
        hero.add(Hero(hero_type))
        terrains.add(Terrain('common_tile', (WIDTH // 2, HEIGHT)))
        pg.time.set_timer(TERRAIN_SPAWN, TERRAIN_SPAWN_FREQ)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if self.game_active:

                if event.type == HERO_DIE:
                    pg.time.delay(DELAY_TIME)
                    self.game_active = False

                if event.type == TERRAIN_SPAWN:
                    terrain_type = choices(
                        list(TERRAIN.keys()), TERRAIN_SPAWN_WEIGHTS)[0]
                    terrains.add(
                        Terrain(terrain_type, (randint(
                            TERRAIN_SPAWNLEFT, TERRAIN_SPAWNRIGHT), HEIGHT)))

                if event.type == EMPTY_TILE_DESTROY:
                    for terrain in terrains:
                        if terrain.type == 'empty_tile' and terrain.has_trigger:
                            terrain.kill()
                    pg.time.set_timer(EMPTY_TILE_DESTROY, 0)
            else:
                if event.type == pg.KEYDOWN:
                    hero_type = None
                    if event.key == pg.K_1:
                        hero_type = 'MaskDude'
                        self.maskdude_sound.play()
                    elif event.key == pg.K_2:
                        hero_type = 'NinjaFrog'
                        self.ninjafrog_sound.play()
                    elif event.key == pg.K_3:
                        hero_type = 'PinkMan'
                        self.pinkman_sound.play()
                    if hero_type is not None:
                        self.reset_game(hero_type)

    def draw_background(self):
        # Draw Background
        for x in range(0, WIDTH, BG_WIDTH):
            for y in range(0, HEIGHT, BG_HEIGHT):
                self.screen.blit(self.background, (x, y))

        # Draw Saws
        for i in range(NUM_SAW):
            x_pos = i * (SAW_SPACING + SAW_WIDTH)
            self.screen.blit(self.saw[self.saw_index],
                             (x_pos + WALL_WIDTH, -SAW_HEIGHT // 2))
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

    def display_health(self):
        heart_y_pos = SAW_HEIGHT // 2
        for i in range(MAX_HEALTH - 1, -1, -1):
            heart_x_pos = (i + 1) * self.heart_full.get_width() + \
                i * HEART_SPACING

            if i < hero.sprite.health:
                self.screen.blit(self.heart_full, (heart_x_pos, heart_y_pos))
            else:
                self.screen.blit(self.heart_empty, (heart_x_pos, heart_y_pos))

    def display_level(self):
        LEVEL_DISPLAY_OFFSET
        self.level = TOP_LEVEL - self.fall_dist // HEIGHT
        if self.level == 0:
            self.game_active = False
        score_text = LEVEL_FONT.render(
            f'Level: {self.level}', True, 'red')
        score_rect = score_text.get_rect(right=WIDTH-LEVEL_DISPLAY_OFFSET)
        self.screen.blit(score_text, score_rect)

    def display_pregame_hud(self):
        for i in range(len(self.hero_initImgs)):
            hero_img = self.hero_initImgs[i]
            if self.animation_count >= len(hero_img):
                self.animation_count = 0

            x_position = HERO_SPACING + (HERO_WIDTH * 2 + HERO_SPACING) * i
            y_position = HEIGHT // 2

            # Draw Heroes
            self.screen.blit(
                hero_img[int(self.animation_count)], (x_position, y_position))
            # Draw HUD Numbers
            self.screen.blit(
                self.hud_number[i], (x_position + HUD_NUMBER_OFFSET_X,
                                     y_position + HUD_NUMBER_OFFSET_Y))

    def display_pregame_messages(self):
        # Display Game Main Title and Subtitle
        self.screen.blit(self.game_mainName, self.game_mainName_rect)
        self.screen.blit(self.game_subName, self.game_subName_rect)

        # Display Game Start Message
        if self.level == 100:
            if self.frame_counter % FPS < 30:
                self.screen.blit(self.game_message, self.game_message_rect)
        # Display Winner Message
        elif self.level == 0:
            if self.frame_counter % FPS < 30:
                self.screen.blit(self.win_message, self.win_message_rect)
        # Display Level Score
        else:
            score_message, score_message_rect = render_font(
                f'Your Final Level: {self.level}', LEVEL_FONT, 'red',
                (WIDTH // 2, SCOREMESSAGE_HEIGHT))
            self.screen.blit(score_message, score_message_rect)

    def cal_damage(self):
        hero.sprite.hit = True
        hero.sprite.health -= 1
        self.sting_sound.play()
        self.display_health()
        pg.display.update()
        if hero.sprite.health <= 0:
            pg.event.post(pg.event.Event(HERO_DIE))

    def cal_heal(self):
        if hero.sprite.health < MAX_HEALTH:
            hero.sprite.health += 1
            self.heal_sound.play()
            self.display_health()
            pg.display.update()

    def cal_fallDist(self):
        if (dist := hero.sprite.rect.bottom - self.hero_prevPos) > 0:
            self.fall_dist += dist
        self.hero_prevPos = hero.sprite.rect.bottom

    def empty_tile_destroy(self):
        current_time = pg.time.get_ticks()
        for terrain, trigger_time in self.triggered_empty_tiles:
            if current_time - trigger_time >= EMPTY_TILE_TRIGGER_TIME:
                self.break_sound.play()
                self.triggered_empty_tiles.remove((terrain, trigger_time))
                terrain.kill()

    def collision(self, terrains):
        for terrain in terrains:
            if pg.sprite.collide_mask(hero.sprite, terrain):
                # Check if hero hits the top of the terrain
                if hero.sprite.rect.bottom <= terrain.rect.top + COLLISION_THRESHOLD:
                    hero.sprite.rect.bottom = terrain.rect.top
                    hero.sprite.fall = False
                    # If the terrain is a spike_tile and hasn't dealt damage yet, apply damage
                    if terrain.type == 'spike_tile' and not terrain.has_dealt_damage:
                        self.cal_damage()
                        terrain.has_dealt_damage = True
                    # If the terrain is a heal_tile and hasn't healed yet, apply healing
                    elif terrain.type == 'heal_tile' and not terrain.has_dealt_heal:
                        self.cal_heal()
                        terrain.has_dealt_heal = True
                    elif terrain.type == 'empty_tile' and not terrain.has_trigger:
                        self.triggered_empty_tiles.append(
                            (terrain, pg.time.get_ticks()))
                        terrain.has_trigger = True
                    elif terrain.type == 'conveyor_tile_left':
                        hero.sprite.rect.x -= CONVEYOR_SPEED
                    elif terrain.type == 'conveyor_tile_right':
                        hero.sprite.rect.x += CONVEYOR_SPEED

                # Check if hero hits the sides of the terrain
                else:
                    if hero.sprite.rect.left < terrain.rect.left:
                        hero.sprite.rect.right = terrain.rect.left
                    elif hero.sprite.rect.right > terrain.rect.right:
                        hero.sprite.rect.left = terrain.rect.right
                    hero.sprite.fall = True
                break
        else:
            # If no collision was detected, set the hero's fall state to True
            hero.sprite.fall = True

    def main_loop(self):
        """This is the game main loop."""
        while True:
            self.clock.tick(FPS)
            self.frame_counter += FRAME_INCREMENT
            self.animation_count += ANIMATION_INCREMENT

            # Handle Events
            self.handle_events()

            if self.game_active:
                # Display Game Background
                self.draw_background()
                # Draw Sprites
                terrains.draw(self.screen)
                hero.draw(self.screen)
                # Update Sprites
                terrains.update()
                hero.update()

                # Perform Collision Detection and Calculate Falling Distance
                if hero.sprite.cutscene_played:
                    self.collision(terrains)
                    self.cal_fallDist()
                    self.empty_tile_destroy()

                # Display HUD
                self.display_level()
                self.display_health()
            else:
                # Generate Pre-game Screen
                self.screen.blit(self.tower_BG, (0, 0))
                # Display HUD
                self.display_pregame_hud()
                self.display_pregame_messages()

            pg.display.update()


# Create Class Instances and Add Sprites
game = Game()

terrains = pg.sprite.Group()
terrains.add(Terrain('common_tile', (WIDTH // 2, HEIGHT)))

hero = pg.sprite.GroupSingle()

# Run Main Loop
game.main_loop()
