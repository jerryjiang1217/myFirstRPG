import random
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

import pygame
import myparameters
import pygame_menu
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_HEIGHT = myparameters.SCREEN_HEIGHT
SCREEN_WIDTH = myparameters.SCREEN_WIDTH
PLAY_HEIGHT = myparameters.PLAY_HEIGHT
PLAY_WIDTH = myparameters.PLAY_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.tag = 'player'
        self.surf = pygame.Surface((64, 64))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("asset/player_up.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(PLAY_WIDTH/2 , PLAY_HEIGHT/2))
        self.level_up_sound = pygame.mixer.Sound("asset/chime_up.wav")
        self.direction = 1
        self.speed = 5
        self.Strength=5
        self.Agility=5
        self.Vigor=5
        self.Intellect=5
        self.Wisdom=5
        self.HP = 50
        self.max_HP = 10*self.Vigor
        self.Mana = 50
        self.max_Mana = 10 * self.Wisdom
        self.STR_exp = 0
        self.STR_exp_required = 100*self.Strength
        self.AGI_exp = 0
        self.AGI_exp_required = 100 * self.Agility
        self.VIG_exp = 0
        self.VIG_exp_required = 100 * self.Vigor
        self.INT_exp = 0
        self.INT_exp_required = 100 * self.Intellect
        self.WIS_exp = 0
        self.WIS_exp_required = 100 * self.Wisdom
        self.move_x = 0
        self.move_y = 0
        self.equiped_weapon = 'Iron Sword'
        self.equiped_armor = 'Leather Armor'
        self.equiped_fire = 'firebolt'
        self.equiped_lighting = 'lightingbolt'
        self.equiped_ice = 'iceball'
        self.defense = 0
        self.equiped_armor_defense = 5
        self.current_weapon_cooldown = 333
        self.regen_counter =0
    def regen(self):
        if self.regen_counter>=120:
            if self.Mana< self.max_Mana:
                self.Mana += round(self.max_Mana*0.02)
            if self.HP < self.max_HP:
                self.HP += round(self.max_HP * 0.01+0.01)
            self.regen_counter=0
        self.regen_counter += 1
    def update(self, pressed_keys,slow_factor):
        if pressed_keys[K_UP] and pressed_keys[K_LEFT] == False and pressed_keys[K_RIGHT] == False:
            self.direction = 1  # up
            if self.direction == 1:
                self.move_y = -self.speed+slow_factor
                #self.rect.move_ip(0, -self.speed+slow_factor)
            self.surf = pygame.image.load("asset/player_up.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if pressed_keys[K_DOWN] and pressed_keys[K_LEFT] == False and pressed_keys[K_RIGHT] == False:
            self.direction = 2  # down
            if self.direction == 2:
                self.move_y =  +self.speed-slow_factor
                #self.rect.move_ip(0, self.speed-slow_factor)
            self.surf = pygame.image.load("asset/player_down.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if pressed_keys[K_LEFT] and pressed_keys[K_UP] == False and pressed_keys[K_DOWN] == False:
            self.direction = 3  # left
            if self.direction == 3:
                self.move_x =  -self.speed+slow_factor
                #self.rect.move_ip(-self.speed+slow_factor, 0)
            self.surf = pygame.image.load("asset/player_left.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if pressed_keys[K_RIGHT] and pressed_keys[K_UP] == False and pressed_keys[K_DOWN] == False:
            self.direction = 4  # right
            if self.direction == 4:
                self.move_x = + self.speed - slow_factor
                #self.rect.move_ip(self.speed-slow_factor, 0)
            self.surf = pygame.image.load("asset/player_right.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > PLAY_WIDTH:
            self.rect.right = PLAY_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= PLAY_HEIGHT:
            self.rect.bottom = PLAY_HEIGHT

class Tile(pygame.sprite.Sprite):
    def __init__(self, chosen_tile, x, y):
        super(Tile, self).__init__()
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.blit(chosen_tile, (0,0))

class Tileset:
    def __init__(self, file_path):
        super(Tileset, self).__init__()
        self.surf = pygame.Surface((32, 32))
        self.tiles = []
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect()
        self.load()

    def load(self):
        for x in range(0, self.rect.right, 32):
            for y in range(0, self.rect.bottom, 32):
                tile = pygame.Surface((32,32))
                tile.blit(self.image, (0,0), (y, x, 32,32))
                self.tiles.append(tile)

class Tilemap:
    def __init__(self, rel_path ,tileset_path, map_id, all_sprites, ob_tiles, slow_tiles , new_map_tiles,prev_map_tiles):
        super(Tilemap, self).__init__()
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path) as f:
            map_input = [[int(num) for num in line.split(',')] for line in f]
        self.size = (len(map_input[0])*32, len(map_input)*32)
        self.surf = pygame.Surface(self.size)
        self.surf.fill((50,60,70))
        self.rect = self.surf.get_rect()
        self.map = map_input
        self.map_id=map_id
        self.tileset=Tileset(tileset_path)
        self.tiles=self.tileset.tiles
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                new_tile = Tile(self.tiles[self.map[i][j]], j * 32, i * 32)
                #screen.blit(new_tile.surf, (j * 32 , i * 32))
                self.surf.blit(new_tile.surf, (j * 32, i * 32))
                if map_id == 'Tomb_entrance':
                    if self.map[i][j] <=1 or self.map[i][j] >=3 and self.map[i][j]<=13 :  # brick tile
                        ob_tiles.add(new_tile)
                        all_sprites.add(new_tile)
                    if self.map[i][j] == 14 or self.map[i][j] == 15:
                        new_map_tiles.add(new_tile)
                        all_sprites.add(new_tile)
                if map_id == 'Tomb_L1' or map_id == 'Tomb_L2' or map_id == 'Tomb_L3' or map_id == 'Tomb_L4':
                    if self.map[i][j] >=3:  # brick tile
                        ob_tiles.add(new_tile)
                        all_sprites.add(new_tile)
                    if self.map[i][j] == 1:
                        prev_map_tiles.add(new_tile)
                        all_sprites.add(new_tile)
                    if self.map[i][j] == 2:
                        new_map_tiles.add(new_tile)
                        all_sprites.add(new_tile)


                elif self.map[i][j] == 1:  # grass tile
                    slow_tiles.add(new_tile)
                    all_sprites.add(new_tile)

"""
Enemy
"""

class Skeleton(pygame.sprite.Sprite):
    def __init__(self,enemy_type, map_size):
        super(Skeleton, self).__init__()
        self.enemy_kill_sound= pygame.mixer.Sound("asset/floop2_x.wav")
        if enemy_type=='skeleton_normal':
            self.tag = 'skeleton_normal'
            self.speed = 3
            self.Strength = 5
            self.Agility = 2
            self.Vigor = 2
            self.Intellect = 0
            self.Wisdom = 0
            self.HP = 50
            self.max_HP = 50
            self.defense = 5
            self.direction = 2  # 1up 2down 3left 4right
            self.exp_points = 100
            self.img_x=40
            self.img_y=40
            self.img_surf = pygame.image.load(f"asset/{self.tag}_down.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if enemy_type=='skeleton_archer':
            self.tag = 'skeleton_archer'
            self.speed = 3
            self.Strength = 5
            self.Agility = 2
            self.Vigor = 2
            self.Intellect = 0
            self.Wisdom = 0
            self.HP = 75
            self.max_HP = 75
            self.defense = 5
            self.direction = 2  # 1up 2down 3left 4right
            self.exp_points = 200
            self.img_x=40
            self.img_y=40
            self.img_surf = pygame.image.load(f"asset/{self.tag}_down.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if enemy_type=='skeleton_warrior':
            self.tag = 'skeleton_warrior'
            self.speed = 5
            self.Strength = 5
            self.Agility = 2
            self.Vigor = 5
            self.Intellect = 0
            self.Wisdom = 0
            self.HP = 300
            self.max_HP = 300
            self.defense = 15
            self.direction = 2  # 1up 2down 3left 4right
            self.exp_points = 500
            self.img_x=60
            self.img_y=60
            self.img_surf = pygame.image.load(f"asset/{self.tag}_down.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if enemy_type=='skeleton_mage':
            self.tag = 'skeleton_mage'
            self.speed = 4
            self.Strength = 5
            self.Agility = 2
            self.Vigor = 3
            self.Intellect = 5
            self.Wisdom = 0
            self.HP = 200
            self.max_HP = 200
            self.defense = 10
            self.direction = 2  # 1up 2down 3left 4right
            self.exp_points = 400
            self.img_x=40
            self.img_y=40
            self.img_surf = pygame.image.load(f"asset/{self.tag}_down.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if enemy_type=='skeleton_boss':
            self.tag = 'skeleton_boss'
            self.speed = 3
            self.Strength = 50
            self.Agility = 20
            self.Vigor = 20
            self.Intellect = 0
            self.Wisdom = 0
            self.HP = 3000
            self.max_HP = 3000
            self.defense = 15
            self.direction = 2  # 1up 2down 3left 4right
            self.exp_points = 1500
            self.img_x=120
            self.img_y=120
            self.img_surf = pygame.image.load("asset/skeleton_boss_down.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.steps = 0
        self.max_step = random.randint(200,400)
        self.img_surf = pygame.Surface((self.img_x, self.img_y))
        #self.img_surf.fill((255, 255, 255))
        self.surf=pygame.Surface((self.img_x, self.img_y+10))
        self.HP_bar=Floating_bar(self.img_x)
        self.surf.blit(self.img_surf, (0,0))
        self.surf.blit(self.HP_bar.surf, (0,self.img_y+5))
        self.rect = self.img_surf.get_rect(
            center=(
                random.randint(40, map_size[0] - 40),
                random.randint(40, map_size[1] - 40),
            )
        )

    def enemy_fire(entity, enemy_bullets, all_sprites):
        if entity.tag == 'skeleton_archer':
            x = (entity.rect.left + entity.rect.right) / 2
            y = (entity.rect.top + entity.rect.bottom) / 2
            new_enemy_bullet = Bullet(x, y, entity.direction, entity.tag)
            enemy_bullets.add(new_enemy_bullet)
            all_sprites.add(new_enemy_bullet)
        if entity.tag == 'skeleton_mage':
            x = (entity.rect.left + entity.rect.right) / 2
            y = (entity.rect.top + entity.rect.bottom) / 2
            new_enemy_bullet = Bullet(x, y, entity.direction, entity.tag)
            enemy_bullets.add(new_enemy_bullet)
            all_sprites.add(new_enemy_bullet)

    def update(self, dir_int, player, collide = False):
        x_dist = abs(self.rect.centerx - player.rect.centerx)
        y_dist = abs(self.rect.centery - player.rect.centery)
        if collide == True and x_dist>y_dist:
            x_dist=0  # change direction when hit wall
        if collide == True and y_dist>x_dist:
            y_dist=0

        if self.rect.centerx>player.rect.centerx and x_dist>y_dist:
            dir_int=3
        elif self.rect.centerx<player.rect.centerx and x_dist>y_dist:
            dir_int=4
        elif self.rect.centery>player.rect.centery:
            dir_int=1
        elif self.rect.centery<player.rect.centery:
            dir_int=2
        if self.steps < self.max_step:
            if self.direction == 1:
                self.rect.move_ip(0, -self.speed)
            if self.direction == 2:
                self.rect.move_ip(0, self.speed)
            if self.direction == 3:
                self.rect.move_ip(-self.speed, 0)
            if self.direction == 4:
                self.rect.move_ip(self.speed, 0)
            self.steps = self.steps + self.speed

        elif self.steps >= self.max_step:
            self.direction = dir_int
            if self.direction == 0:
                self.rect.move_ip(0, 0)
            if self.direction == 1:
                self.rect.move_ip(0, -self.speed)
            if self.direction == 2:
                self.rect.move_ip(0, self.speed)
            if self.direction == 3:
                self.rect.move_ip(-self.speed, 0)
            if self.direction == 4:
                self.rect.move_ip(self.speed, 0)
            self.steps = 0

        if self.direction == 2:
            self.img_surf = pygame.image.load(f'asset/{self.tag}_down.png').convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if self.direction == 1:
            self.img_surf = pygame.image.load(f"asset/{self.tag}_up.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if self.direction == 4:
            self.img_surf = pygame.image.load(f"asset/{self.tag}_right.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        if self.direction == 3:
            self.img_surf = pygame.image.load(f"asset/{self.tag}_left.png").convert()
            self.img_surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf.blit(self.img_surf, (0, 0))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf.blit(self.HP_bar.surf, (0,self.img_y+5))
        self.HP_bar.update(self)
"""
weapon
"""

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction,user_size, sword_name):
        super(Sword, self).__init__()
        if direction == 1:
            self.surf = pygame.Surface((64, 10))
            self.surf = pygame.image.load("asset/sword_light_up.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 2:
            self.surf = pygame.Surface((64, 10))
            self.surf = pygame.image.load("asset/sword_light_down.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 3 :
            self.surf = pygame.Surface((10, 64))
            self.surf = pygame.image.load("asset/sword_light_left.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 4 :
            self.surf = pygame.Surface((10, 64))
            self.surf = pygame.image.load("asset/sowrd_light_right.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if direction == 1:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2, y - user_size[1]/2 -25))
        if direction == 2:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2, y + user_size[1]/2 + 15))
        if direction == 3:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2 - 25, y - user_size[1]/2))
        if direction == 4:
            self.rect = self.surf.get_rect(topleft=(x + user_size[0]/2 + 15, y - user_size[1]/2))
        self.lifecycle = 5
        self.life_counter=0
        self.direction = direction
        self.shoot_sound= pygame.mixer.Sound("asset/swing.flac")
        self.collide_sound = pygame.mixer.Sound("asset/swing.flac")
        if sword_name == 'Iron Sword':
            self.min_attack = 3
            self.max_attack = 6
            self.tag = 'Iron Sword'
        if sword_name == 'Steel Sword':
            self.min_attack = 8
            self.max_attack = 12
            self.tag = 'Steel Sword'


    def update(self):
        self.life_counter += 1
        if self.life_counter>=self.lifecycle:
            self.kill()

class Greatsword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction,user_size, sword_name):
        super(Greatsword, self).__init__()
        if direction == 1:
            self.surf = pygame.Surface((96, 32))
            self.surf = pygame.image.load("asset/greatsword_light_up.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 2:
            self.surf = pygame.Surface((96, 32))
            self.surf = pygame.image.load("asset/greatsword_light_down.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 3 :
            self.surf = pygame.Surface((32, 96))
            self.surf = pygame.image.load("asset/greatsword_light_left.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 4 :
            self.surf = pygame.Surface((32, 96))
            self.surf = pygame.image.load("asset/greatsword_light_right.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if direction == 1:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2, y - user_size[1]/2 -35))
        if direction == 2:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2, y + user_size[1]/2 + 25))
        if direction == 3:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0]/2 - 35, y - user_size[1]/2))
        if direction == 4:
            self.rect = self.surf.get_rect(topleft=(x + user_size[0]/2 + 25, y - user_size[1]/2))
        self.lifecycle = 5
        self.life_counter=0
        self.direction = direction
        self.shoot_sound= pygame.mixer.Sound("asset/swing.flac")
        self.collide_sound = pygame.mixer.Sound("asset/swing.flac")
        if sword_name == 'Claymore':
            self.min_attack = 12
            self.max_attack = 20
            self.defense =0
            self.tag = 'Claymore'

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, user_size, sword_name):
        super(Spear, self).__init__()
        if direction == 1:
            self.surf = pygame.Surface((16, 96))
            self.surf = pygame.image.load("asset/spear_light_up.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 2:
            self.surf = pygame.Surface((16, 96))
            self.surf = pygame.image.load("asset/spear_light_down.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 3:
            self.surf = pygame.Surface((96, 16))
            self.surf = pygame.image.load("asset/spear_light_left.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if direction == 4:
            self.surf = pygame.Surface((96, 16))
            self.surf = pygame.image.load("asset/spear_light_right.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        if direction == 1:
            self.rect = self.surf.get_rect(topleft=(x - 8, y - user_size[1] / 2 - 106))
        if direction == 2:
            self.rect = self.surf.get_rect(topleft=(x - 8, y + user_size[1] / 2 + 10))
        if direction == 3:
            self.rect = self.surf.get_rect(topleft=(x - user_size[0] / 2 - 106, y - 8))
        if direction == 4:
            self.rect = self.surf.get_rect(topleft=(x + user_size[0] / 2 + 10, y - 8))
        self.lifecycle = 5
        self.life_counter = 0
        self.direction = direction
        self.shoot_sound = pygame.mixer.Sound("asset/swing.flac")
        self.collide_sound = pygame.mixer.Sound("asset/swing.flac")
        if sword_name == 'Iron Spear':
            self.min_attack = 16
            self.max_attack = 24
            self.defense = 0
            self.tag = 'Iron Spear'

    def update(self):
        self.life_counter += 1
        if self.life_counter>=self.lifecycle:
            self.kill()

class Bar(pygame.sprite.Sprite):
    def __init__(self, bar_type, screen):
        super(Bar, self).__init__()
        self.surf = pygame.Surface((150, 10))
        if bar_type == 'HP':
            self.bar_len=150
            self.surf = pygame.Surface((self.bar_len, 10))
            self.surf.fill((255,0,0))
        if bar_type == 'Mana':
            self.bar_len = 150
            self.surf = pygame.Surface((self.bar_len, 10))
            self.surf.fill((0,0,255))
        if bar_type == 'STR' or bar_type == 'AGI' or bar_type == 'AGI' or bar_type == 'VIG' or bar_type == 'INT' or bar_type == 'WIS':
            self.bar_len = 50
            self.surf = pygame.Surface((100, 10))
            self.surf.fill((0, 255, 255))

        self.tag=bar_type

        #fill border
        self.surf.fill((255, 255, 255), (0, 0, self.bar_len, 1))
        self.surf.fill((255, 255, 255), (0, 9, self.bar_len, 1))
        self.surf.fill((255, 255, 255), (0, 0, 1, 10))
        self.surf.fill((255, 255, 255), (self.bar_len-1, 0, 1, 10))

        #blit to screen
        if bar_type == 'HP':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-180, 40))
        if bar_type == 'Mana':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-180, 80))
        if bar_type == 'STR':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 105))
        if bar_type == 'AGI':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 135))
        if bar_type == 'VIG':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 165))
        if bar_type == 'INT':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 195))
        if bar_type == 'WIS':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 225))

    def update(self, player, screen):
        self.surf.fill((0, 0, 0))
        if self.tag == 'HP':
            x=round(player.HP/player.max_HP*self.bar_len)
            self.surf.fill((255, 0, 0), (0,0,x,10))
        if self.tag == 'Mana':
            x=round(player.Mana/player.max_Mana*self.bar_len)
            self.surf.fill((0, 0, 255), (0,0,x,10))
        if self.tag == 'STR':
            x=round(player.STR_exp/player.STR_exp_required*self.bar_len)
            self.surf.fill((0, 255, 255), (0,0,x,10))
        if self.tag == 'AGI':
            x=round(player.AGI_exp/player.AGI_exp_required*self.bar_len)
            self.surf.fill((0, 255, 255), (0,0,x,10))
        if self.tag == 'VIG':
            x=round(player.VIG_exp/player.VIG_exp_required*self.bar_len)
            self.surf.fill((0, 255, 255), (0,0,x,10))
        if self.tag == 'INT':
            x=round(player.INT_exp/player.INT_exp_required*self.bar_len)
            self.surf.fill((0, 255, 255), (0,0,x,10))
        if self.tag == 'WIS':
            x=round(player.WIS_exp/player.WIS_exp_required*self.bar_len)
            self.surf.fill((0, 255, 255), (0,0,x,10))
        # fill border
        self.surf.fill((255, 255, 255), (0, 0, self.bar_len, 1))
        self.surf.fill((255, 255, 255), (0, 9, self.bar_len, 1))
        self.surf.fill((255, 255, 255), (0, 0, 1, 10))
        self.surf.fill((255, 255, 255), (self.bar_len-1, 0, 1, 10))
        if self.tag == 'HP':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-180, 40))
        if self.tag == 'Mana':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-180, 80))
        if self.tag == 'STR':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 105))
        if self.tag == 'AGI':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 135))
        if self.tag == 'VIG':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 165))
        if self.tag == 'INT':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 195))
        if self.tag == 'WIS':
            screen.blit(self.surf, (myparameters.SCREEN_WIDTH-100, 225))

class Floating_bar(pygame.sprite.Sprite):
    def __init__(self, width):
        super(Floating_bar, self).__init__()
        self.surf = pygame.Surface((width, 6))
        self.surf.fill((255,0,0))
        self.width=width
        #fill border
        self.surf.fill((255, 255, 255), (0, 0, self.width, 1))
        self.surf.fill((255, 255, 255), (0, 4 , self.width, 1))
        self.surf.fill((255, 255, 255), (0, 0, 1, 6))
        self.surf.fill((255, 255, 255), (self.width-1, 0, 1, 6))

        #blit to screen
        #screen.blit(self.surf, entity.rect.leftbottom)

    def update(self, entity):
        self.surf.fill((0, 0, 0))
        x=round(entity.HP/entity.max_HP*self.width)
        self.surf.fill((255, 0, 0), (0,0,x,6))
        # fill border
        self.surf.fill((255, 255, 255), (0, 0, self.width, 1))
        self.surf.fill((255, 255, 255), (0, 4, self.width, 1))
        self.surf.fill((255, 255, 255), (0, 0, 1, 6))
        self.surf.fill((255, 255, 255), (self.width - 1, 0, 1, 6))
        #screen.blit(self.surf, screen.blit(self.surf, entity.rect.leftbottom))

class Dmg_txt(pygame.sprite.Sprite):
    def __init__(self, content, x, y, screen):
        super(Dmg_txt, self).__init__()
        font = pygame.font.Font('asset/Roboto-Black.ttf', 18)
        self.text = font.render(content, True, (255, 0, 0), (0, 0, 0))
        self.text.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect=self.text.get_rect(center=(x, y))
        screen.blit(self.text, self.rect)
        self.timer = 0

    def update(self,screen):
        self.rect.move_ip(0,-1)
        if self.timer <= 30:
            screen.blit(self.text, self.rect)
        else:
            self.kill()
        self.timer +=1


"""
bullet
"""

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_type):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((1, 1))
        if bullet_type=='firebolt':
            self.surf = pygame.Surface((20, 20))
            self.surf = pygame.image.load("asset/firebolt.png").convert()
            self.tag = bullet_type
            self.speed = 20
            self.Mana_cost = 5
            self.mgk_dmg_fctr=5
            self.mgk_base_dmg = 25
        if bullet_type=='fireball':
            self.surf = pygame.Surface((40, 40))
            self.surf = pygame.image.load("asset/weapon_icon.png").convert()
            self.tag = bullet_type
            self.speed = 20
            self.Mana_cost = 20
            self.mgk_dmg_fctr=20
            self.mgk_base_dmg = 20
        if bullet_type=='lightingbolt':
            if direction == 1 or direction ==2:
                self.surf = pygame.Surface((30, 60))
                self.surf = pygame.image.load("asset/lightingbolt_down.png").convert()
            if direction == 3 or direction ==4:
                self.surf = pygame.Surface((60, 30))
                self.surf = pygame.image.load("asset/lightingbolt_left.png").convert()
            self.tag = bullet_type
            self.speed = 30
            self.Mana_cost = 10
            self.mgk_dmg_fctr = 1
            self.mgk_base_dmg = 10
            self.travel_distance = 0
            self.max_distance = 300
        if bullet_type=='iceball':
            self.surf = pygame.Surface((60, 60))
            self.surf = pygame.image.load("asset/iceball.png").convert()
            self.tag = bullet_type
            self.speed = 10
            self.Mana_cost = 8
            self.mgk_dmg_fctr=2
            self.mgk_base_dmg = 5
            self.lifecycle=10
        if bullet_type=='skeleton_archer':
            if direction == 1 :
                self.surf = pygame.Surface((10, 20))
                self.surf = pygame.image.load("asset/arrow_up.png").convert()
            if direction == 2 :
                self.surf = pygame.Surface((10, 20))
                self.surf = pygame.image.load("asset/arrow_down.png").convert()
            if direction == 3:
                self.surf = pygame.Surface((20, 10))
                self.surf = pygame.image.load("asset/arrow_left.png").convert()
            if direction == 4:
                self.surf = pygame.Surface((20, 10))
                self.surf = pygame.image.load("asset/arrow_right.png").convert()
            self.tag = bullet_type
            self.speed = 10
            self.attack = 15
        if bullet_type=='skeleton_mage':
            self.surf = pygame.Surface((20, 20))
            self.surf = pygame.image.load("asset/firebolt.png").convert()
            self.tag = bullet_type
            self.speed = 15
            self.attack = 30
        #self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect( center=(x,y,))
        self.bullet_direction = direction
        self.collide_sound = pygame.mixer.Sound("asset/explosion_x.wav")

    def update(self):
        if self.tag == 'iceball':
            self.rect.move_ip(random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed))
        elif self.bullet_direction == 1:
            self.rect.move_ip(0, -self.speed)
        elif self.bullet_direction == 2:
            self.rect.move_ip(0, self.speed)
        elif self.bullet_direction == 3:
            self.rect.move_ip(-self.speed, 0)
        elif self.bullet_direction == 4:
            self.rect.move_ip(self.speed, 0)
        elif self.rect.right > PLAY_WIDTH or self.rect.right < 0 or self.rect.top < 0 or self.rect.top > PLAY_HEIGHT:
            self.kill()

        if self.tag == 'lightingbolt':
            self.travel_distance += self.speed
            if self.travel_distance >= self.max_distance:
                self.kill()

"""
drop
"""
class Treasurebox(pygame.sprite.Sprite):
    def __init__(self, bonusbox_id, x, y):
        super(Treasurebox, self).__init__()
        self.tag=bonusbox_id
        if bonusbox_id == 0:
            self.surf = pygame.image.load("asset/treasurebox.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if bonusbox_id == 1:
            self.surf = pygame.image.load("asset/treasurebox.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if bonusbox_id == 2:
            self.surf = pygame.image.load("asset/treasurebox.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.bonus_sound = pygame.mixer.Sound("asset/chime.wav")

def enemy_drop(entity, treasureboxes, all_sprites):
    x = (entity.rect.left + entity.rect.right) / 2
    y = (entity.rect.top + entity.rect.bottom) / 2
    if entity.tag == 'skeleton_normal' or entity.tag == 'skeleton_archer':
        new_treasurebox=Treasurebox(0,x,y)
        treasureboxes.add(new_treasurebox)
        all_sprites.add(new_treasurebox)
    if entity.tag == 'skeleton_archer' :
        new_treasurebox=Treasurebox(1,x,y)
        treasureboxes.add(new_treasurebox)
        all_sprites.add(new_treasurebox)
    if entity.tag == 'skeleton_warrior' or entity.tag == 'skeleton_mage':
        new_treasurebox=Treasurebox(2,x,y)
        treasureboxes.add(new_treasurebox)
        all_sprites.add(new_treasurebox)

def loot_treasurebox(treasurebox):
    seed = random.randint(1, 100)
    if treasurebox.tag == 0:
        gold=random.randint(2, 10)
        myparameters.item_inventory['Gold'] += gold
        #notification(f'Gold +{gold}')
        if seed<=2:
            myparameters.weapon_inventory['Steel Sword'] = True
            notification(f'Got Steel Sword')
        if seed>90:
            myparameters.item_inventory['HP Potion'] += 1
            notification(f'Got HP Potion')
        if seed>80 and seed<=90:
            myparameters.item_inventory['Mana Potion'] += 1
            notification(f'Got Mana Potion')
    if treasurebox.tag == 1:
        gold=random.randint(5, 15)
        myparameters.item_inventory['Gold'] += gold
        #notification(f'Gold +{gold}')
        if seed<=5:
            myparameters.weapon_inventory['Steel Sword'] = True
            notification(f'Got Steel Sword')
        if seed>5 and seed<=10:
            myparameters.weapon_inventory['Iron Spear'] = True
            notification(f'Got Iron Spear')
        if seed>85:
            myparameters.item_inventory['HP Potion'] += 1
            notification(f'Got HP Potion')
        if seed>70 and seed<=85:
            myparameters.item_inventory['Mana Potion'] += 1
            notification(f'Got Mana Potion')
    if treasurebox.tag == 2:
        gold=random.randint(10, 30)
        myparameters.item_inventory['Gold'] += gold
        #notification(f'Gold +{gold}')
        if seed<=5:
            myparameters.weapon_inventory['Iron Armor'] = True
            notification(f'Got Iron Armor')
        if seed>5 and seed <=10:
            myparameters.weapon_inventory['Claymore'] = True
            notification(f'Got Claymore')
        if seed>85:
            myparameters.item_inventory['HP Potion'] += 1
            notification(f'Got HP Potion')
        if seed>70 and seed<=85:
            myparameters.item_inventory['Mana Potion'] += 1
            notification(f'Got Mana Potion')
    myparameters.item_inventory['HP Potion'] = min(myparameters.item_inventory['HP Potion'], 9)
    myparameters.item_inventory['Mana Potion'] = min (myparameters.item_inventory['Mana Potion'], 9)
"""
functions
"""

def calc_dmg(attacker, attacker_weapon, defenser, atk_type):
    if atk_type == 'Iron Sword' or atk_type == 'Steel Sword' or atk_type == 'Elven Sword':
        dmg=attacker.Strength/2+attacker.Agility/2 \
            +random.randint(attacker_weapon.min_attack,attacker_weapon.max_attack)\
            -defenser.defense
    elif atk_type == 'Claymore' or atk_type == 'Iron Spear':
        dmg=attacker.Strength+random.randint(attacker_weapon.min_attack,attacker_weapon.max_attack)\
            -defenser.defense
    elif atk_type == 'skeleton_archer' :
        dmg=attacker.attack-defenser.defense-defenser.equiped_armor_defense
    elif atk_type == 'skeleton_mage' :
        dmg=attacker.attack

    elif atk_type == 'firebolt' or atk_type == 'lightingbolt' or atk_type == 'iceball' or atk_type== 'skeleton_mage':
        dmg = attacker.Intellect * attacker_weapon.mgk_dmg_fctr + attacker_weapon.mgk_base_dmg

    return round(max(dmg, 1))

def calc_dmg_col(attacker,  defenser):
    dmg= (attacker.Vigor*5 - defenser.defense - defenser.equiped_armor_defense)
    print(defenser.equiped_armor_defense)
    return round(max(dmg, 1))

def calc_exp_gain(attacker, defenser, exp_type, kill_y_n,level_up_sound, dmg=0, mana_used=0):
    if exp_type == 'Iron Sword' or exp_type == 'Steel Sword':
        if kill_y_n == False:
            attacker.STR_exp = attacker.STR_exp + defenser.exp_points/20
            attacker.AGI_exp = attacker.AGI_exp + defenser.exp_points / 20
        if kill_y_n == True:
            attacker.STR_exp = attacker.STR_exp + defenser.exp_points/2
            attacker.AGI_exp = attacker.AGI_exp + defenser.exp_points / 2
        if attacker.STR_exp>=attacker.STR_exp_required:
            level_up_sound.play()
            attacker.Strength += 1
            attacker.STR_exp = 0
            attacker.STR_exp_required = attacker.Strength*100
        if attacker.AGI_exp>=attacker.AGI_exp_required:
            level_up_sound.play()
            attacker.Agility += 1
            attacker.AGI_exp = 0
            attacker.AGI_exp_required = attacker.Agility*100
    if exp_type == 'firebolt' or exp_type == 'lightingbolt' or exp_type == 'iceball':
        if kill_y_n == False:
            attacker.INT_exp = attacker.INT_exp + defenser.exp_points/10
        if kill_y_n == True:
            attacker.INT_exp = attacker.INT_exp + defenser.exp_points
        if attacker.INT_exp>=attacker.INT_exp_required:
            level_up_sound.play()
            attacker.Intellect += 1
            attacker.INT_exp = 0
            attacker.INT_exp_required = attacker.Intellect*100
    if exp_type == 'VIG':
        attacker.VIG_exp = attacker.VIG_exp + dmg*20
        if attacker.VIG_exp>=attacker.VIG_exp_required:
            level_up_sound.play()
            attacker.Vigor += 1
            attacker.VIG_exp = 0
            attacker.VIG_exp_required = attacker.Vigor*100
            attacker.max_HP=attacker.Vigor*10
            attacker.defense += 1
    if exp_type == 'WIS':
        attacker.WIS_exp = attacker.WIS_exp + mana_used*20
        if attacker.WIS_exp>=attacker.WIS_exp_required:
            level_up_sound.play()
            attacker.Wisdom += 1
            attacker.WIS_exp = 0
            attacker.WIS_exp_required = attacker.Wisdom*100
            attacker.max_Mana = attacker.Wisdom*10

def display_text(font_file, font_size, content,x, y, screen):
    font = pygame.font.Font(font_file, font_size)
    text = font.render(content, True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    screen.blit(text, textRect)

class Icon(pygame.sprite.Sprite):
    def __init__(self, icon_file,x, y, screen):
        super(Icon, self).__init__()
        self.surf = pygame.Surface((32, 32))
        self.surf = pygame.image.load(icon_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect=self.surf.get_rect(topleft = (x, y))
        screen.blit(self.surf, self.rect)

def move_ob(sprite, direction, speed, ob_tiles):
    if direction == 1:
        sprite.rect.move_ip(0, speed)
    if direction == 2:
        sprite.rect.move_ip(0, -speed)
    if direction == 3:
        sprite.rect.move_ip(speed, 0)
    if direction == 4:
        sprite.rect.move_ip(-speed, 0)
    if pygame.sprite.spritecollideany(sprite, ob_tiles):
        if direction == 1:
            sprite.rect.move_ip(0, -speed)
        if direction == 2:
            sprite.rect.move_ip(0, speed)
        if direction == 3:
            sprite.rect.move_ip(-speed, 0)
        if direction == 4:
            sprite.rect.move_ip(speed, 0)

def hit_bounce(sprite, direction, speed, ob_tiles):
    if direction == 1:
        sprite.rect.move_ip(0, -speed)
    if direction == 2:
        sprite.rect.move_ip(0, speed)
    if direction == 3:
        sprite.rect.move_ip(-speed, 0)
    if direction == 4:
        sprite.rect.move_ip(speed, 0)
    if pygame.sprite.spritecollideany(sprite, ob_tiles):
        if direction == 1:
            sprite.rect.move_ip(0, speed)
        if direction == 2:
            sprite.rect.move_ip(0, -speed)
        if direction == 3:
            sprite.rect.move_ip(speed, 0)
        if direction == 4:
            sprite.rect.move_ip(-speed, 0)

def paused(pause, screen):
    screen.fill((0,0,0))
    display_text('asset/Roboto-Black.ttf', 18, "PAUSED", 400, 400, screen)
    while pause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print("keydown",event.type, KEYDOWN)
                if event.key == pygame.K_p:
                    print("K_p", event.key, pygame.K_p)
                    pause = False
                    print(pause)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        # gameDisplay.fill(white)

        #button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        #button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        #pygame.time.clock.tick(15)

def notification(message):
    myparameters.notifications.append(message)

def use_potion(player,potion_type):
    if potion_type == 'HP Potion':
        if myparameters.item_inventory['HP Potion'] >0:
            player.HP = min(player.HP +round(player.max_HP*0.6), player.max_HP)
            myparameters.item_inventory['HP Potion'] -= 1
    if potion_type == 'Mana Potion':
        if myparameters.item_inventory['Mana Potion'] > 0:
            player.Mana = min(player.Mana + round(player.max_Mana*0.6), player.max_Mana)
            myparameters.item_inventory['Mana Potion'] -= 1

def load_new_map(map_path, tileset_path , map_id,all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles):
    all_sprites.empty()
    ob_tiles.empty()

    tilemap = Tilemap( map_path,tileset_path,map_id, all_sprites, ob_tiles, slow_tiles, new_map_tiles, prev_map_tiles)
    return tilemap

def respawn_enemy(tilemap, enemy_id,cnt, enemies, all_sprites, ob_tiles):
    while cnt>0:
        new_enemy = Skeleton(enemy_id, tilemap.size)
        if pygame.sprite.spritecollideany(new_enemy, ob_tiles):
            new_enemy.kill()
        else:
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            cnt -= 1