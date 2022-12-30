# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os

import pygame_menu

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import pygame
import random
import myclasses
import myparameters
import mycollides
import mymenus



pygame.init()



"""
initialize screen
"""

clock = pygame.time.Clock()

SCREEN_HEIGHT=myparameters.SCREEN_HEIGHT
SCREEN_WIDTH=myparameters.SCREEN_WIDTH
PLAY_HEIGHT=myparameters.PLAY_HEIGHT
PLAY_WIDTH=myparameters.PLAY_WIDTH

global screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen_offset_x = 0
screen_offset_y = 0

pygame.display.set_caption('RPG')

"""
initialize sound
"""
pygame.mixer.init()

pygame.mixer.music.load("asset/DayTime.mid")
pygame.mixer.music.play(loops=-1)

collision_sound = pygame.mixer.Sound("asset/hurt.wav")
hit_sound = pygame.mixer.Sound("asset/hit_slice_flesh.mp3")
#bonus_sound = pygame.mixer.Sound("asset/chime.wav")
swing_sound = pygame.mixer.Sound("asset/swing.flac")





"""
initializing map, player and enemy
"""

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
user_weapons = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
dmg_txts = pygame.sprite.Group()
treasureboxes = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
ob_tiles= pygame.sprite.Group()
slow_tiles= pygame.sprite.Group()
new_map_tiles = pygame.sprite.Group()
prev_map_tiles = pygame.sprite.Group()

tilemap = myclasses.Tilemap("asset/map_assets/tomb_1.csv", "asset/map_assets/mytileset_png.png", 'Tomb_entrance',
                            all_sprites, ob_tiles, slow_tiles,new_map_tiles, prev_map_tiles)
#tilemap = myclasses.Tilemap("asset/map_assets/tomb_L3.csv", "asset/map_assets/tileset_tomb_inside.png", 'Tomb_L3',
#                            all_sprites, ob_tiles, slow_tiles,new_map_tiles, prev_map_tiles)
myclasses.respawn_enemy(tilemap,'skeleton_normal', 10, enemies, all_sprites, ob_tiles)

global player
player = myclasses.Player()




"""
initialize menu
"""

"""
events
"""


ENEMYFIRE = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMYFIRE, 5000)
LOADMAP = pygame.USEREVENT + 3
LOADMAP_type = 'New'
col_timer = 0
weapon_hit_cnter =1
hit_timer = 0
last_tick=pygame.time.get_ticks()
enemy_cnt = 5
boss_cnt = 1
slow_factor=0
"""
main loop
"""
running = True
weapon_out = False
fire_magic_out = False
lighting_magic_out = False
ice_magic_out = False
pause= False
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = mymenus.menu_init(player)
                menu.enable()
                menu.mainloop(screen)
            elif event.key == pygame.K_SPACE:
                weapon_out = True

            elif event.key == pygame.K_a:
                fire_magic_out = True
            elif event.key == pygame.K_s:
                lighting_magic_out = True
            elif event.key == pygame.K_d:
                ice_magic_out = True
            elif event.key == pygame.K_z:
                myclasses.use_potion(player, 'HP Potion')
            elif event.key == pygame.K_x:
                myclasses.use_potion(player, 'Mana Potion')
            elif event.key == pygame.K_p:
                #pause = True
                #myclasses.paused(pause, screen)
                print(f'player cord: {player.rect.center}',f'screen cord: {screen_offset_x,screen_offset_y}')
        elif event.type == pygame.KEYUP:
            weapon_hit_cnter = 1
        elif event.type == ENEMYFIRE:  # create the enemy_bulllet periodically
            for entity in enemies:
                if entity.rect.centerx - player.rect.centerx <= PLAY_WIDTH / 2 or entity.rect.centery - player.rect.centery <= PLAY_HEIGHT / 2:
                    entity.enemy_fire(enemy_bullets,all_sprites)

        elif event.type == LOADMAP:  # create the enemy_bulllet periodically
            all_sprites.empty()
            ob_tiles.empty()
            new_map_tiles.empty()
            enemies.empty()
            screen.fill((0,0,0))
            screen_offset_x = 0
            screen_offset_y = 0
            if (LOADMAP_type == 'New' and tilemap.map_id=='Tomb_entrance') or (LOADMAP_type == 'Prev' and tilemap.map_id=='Tomb_L2'):
                new_tilemap=myclasses.load_new_map( "asset/map_assets/tomb_L1.csv", "asset/map_assets/tileset_tomb_inside.png" ,
                                            'Tomb_L1', all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles)
                tilemap=new_tilemap
                myclasses.respawn_enemy(tilemap, 'skeleton_normal', 20, enemies, all_sprites, ob_tiles)
                myclasses.respawn_enemy(tilemap, 'skeleton_archer', 20, enemies, all_sprites, ob_tiles)
                player.rect.center=(PLAY_WIDTH/2, PLAY_HEIGHT/2)
                if LOADMAP_type== 'Prev':
                    screen_offset_x = -1815
                    screen_offset_y = -2675
                for entity in all_sprites:
                    entity.rect.move_ip(screen_offset_x,screen_offset_y)
            elif LOADMAP_type == 'Prev' and tilemap.map_id=='Tomb_L1':
                new_tilemap=myclasses.load_new_map( "asset/map_assets/tomb_1.csv", "asset/map_assets/mytileset_png.png" ,
                                            'Tomb_entrance', all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles)
                tilemap=new_tilemap
                myclasses.respawn_enemy(tilemap, 'skeleton_normal', 10, enemies, all_sprites, ob_tiles)
                player.rect.center = (PLAY_WIDTH / 2, PLAY_HEIGHT / 2)
                screen_offset_x = -400
                screen_offset_y = -400
                for entity in all_sprites:
                    entity.rect.move_ip(-400,-400)
            elif (LOADMAP_type == 'New' and tilemap.map_id=='Tomb_L1') or (LOADMAP_type == 'Prev' and tilemap.map_id=='Tomb_L3') :
                new_tilemap=myclasses.load_new_map( "asset/map_assets/tomb_L2.csv", "asset/map_assets/tileset_tomb_inside.png" ,
                                            'Tomb_L2', all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles)
                tilemap=new_tilemap
                print(tilemap.map_id)
                myclasses.respawn_enemy(tilemap, 'skeleton_archer', 20, enemies, all_sprites, ob_tiles)
                myclasses.respawn_enemy(tilemap, 'skeleton_warrior', 20, enemies, all_sprites, ob_tiles)
                player.rect.center = (PLAY_WIDTH / 2, PLAY_HEIGHT / 2)
                if LOADMAP_type == 'Prev':
                    screen_offset_x = -1740
                    screen_offset_y = -3080
                for entity in all_sprites:
                    entity.rect.move_ip(screen_offset_x,screen_offset_y)

            elif (LOADMAP_type == 'New' and tilemap.map_id=='Tomb_L2') or (LOADMAP_type == 'Prev' and tilemap.map_id=='Tomb_L4') :
                new_tilemap=myclasses.load_new_map( "asset/map_assets/tomb_L3.csv", "asset/map_assets/tileset_tomb_inside.png" ,
                                            'Tomb_L3', all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles)
                tilemap=new_tilemap
                print(tilemap.map_id)
                myclasses.respawn_enemy(tilemap, 'skeleton_warrior', 20, enemies, all_sprites, ob_tiles)
                myclasses.respawn_enemy(tilemap, 'skeleton_mage', 20, enemies, all_sprites, ob_tiles)
                player.rect.center = (PLAY_WIDTH / 2, PLAY_HEIGHT / 2)
                if LOADMAP_type== 'Prev':
                    screen_offset_x = -3590
                    screen_offset_y = -590
                for entity in all_sprites:
                    entity.rect.move_ip(screen_offset_x,screen_offset_y)

            elif LOADMAP_type == 'New' and tilemap.map_id=='Tomb_L3':
                new_tilemap=myclasses.load_new_map( "asset/map_assets/tomb_L4.csv", "asset/map_assets/tileset_tomb_inside.png" ,
                                            'Tomb_L4', all_sprites, ob_tiles, slow_tiles,new_map_tiles,prev_map_tiles)
                tilemap=new_tilemap
                print(tilemap.map_id)
                myclasses.respawn_enemy(tilemap, 'skeleton_boss', 1, enemies, all_sprites, ob_tiles)
                myclasses.respawn_enemy(tilemap, 'skeleton_mage', 20, enemies, all_sprites, ob_tiles)
                player.rect.center = (PLAY_WIDTH / 2, PLAY_HEIGHT / 2)
                screen_offset_x = 0
                screen_offset_y = 0
                for entity in all_sprites:
                    entity.rect.move_ip(-screen_offset_x,-screen_offset_y)



        elif event.type == pygame.QUIT:
            running = False


    """
    screen blit for map
    """

    #moe player and blit map and change enemy relatively

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, slow_factor)
    (mapx,mapy)=tilemap.size
    #print(screen_offset_x, screen_offset_y)
    if pressed_keys[pygame.K_DOWN]== True or pressed_keys[pygame.K_UP] == True or pressed_keys[pygame.K_LEFT]== True or \
            pressed_keys[pygame.K_RIGHT] == True:
        if screen_offset_x-player.move_x < 0 and screen_offset_x-player.move_x>= -(mapx-PLAY_WIDTH) \
                and player.rect.left>=PLAY_WIDTH/4 and player.rect.right<=PLAY_WIDTH*3/4:  # when screen moves
            screen_offset_x = screen_offset_x - player.move_x
            for entity in all_sprites:
                entity.rect.move_ip(-player.move_x,0)
            if pygame.sprite.spritecollideany(player, ob_tiles):
                screen_offset_x = screen_offset_x + player.move_x
                for entity in all_sprites:
                    entity.rect.move_ip(+player.move_x,0)

        else:  # when screen not moving
            player.rect.move_ip(player.move_x, 0)
            if pygame.sprite.spritecollideany(player, ob_tiles):
                player.rect.move_ip(-player.move_x, 0)

        if screen_offset_y-player.move_y < 0 and screen_offset_y-player.move_y >= -(mapy-PLAY_HEIGHT) \
                and player.rect.top>=PLAY_HEIGHT/4 and player.rect.bottom<=PLAY_HEIGHT*3/4:
            screen_offset_y = screen_offset_y - player.move_y
            for entity in all_sprites:
                entity.rect.move_ip(0,- player.move_y)
            if pygame.sprite.spritecollideany(player, ob_tiles):
                #print("direction y collide ob1`")
                screen_offset_y = screen_offset_y + player.move_y
                for entity in all_sprites:
                    entity.rect.move_ip(0,+ player.move_y)
        else:
            player.rect.move_ip(0, + player.move_y)
            if pygame.sprite.spritecollideany(player, ob_tiles):
                #print("direction y collide ob2`")
                player.rect.move_ip(0, - player.move_y)

    player.move_x = 0
    player.move_y = 0
    #print(screen_offset_x)
    screen.blit(tilemap.surf, (screen_offset_x, screen_offset_y))


    """
    player action
    """


    player.regen()
    if weapon_out==True:
        now = pygame.time.get_ticks()
        if now - last_tick>=player.current_weapon_cooldown:
            if player.equiped_weapon=='Iron Sword' or player.equiped_weapon=='Steel Sword':
                new_sword = myclasses.Sword(player.rect.centerx, player.rect.centery, player.direction , player.rect.size, player.equiped_weapon)
                new_sword.shoot_sound.play()
                user_weapons.add(new_sword)
                all_sprites.add(new_sword)
            if player.equiped_weapon=='Claymore' or player.equiped_weapon=='Claymore2':
                new_sword = myclasses.Greatsword(player.rect.centerx, player.rect.centery, player.direction , player.rect.size, player.equiped_weapon)
                user_weapons.add(new_sword)
                all_sprites.add(new_sword)
                new_sword.shoot_sound.play()
            if player.equiped_weapon=='Iron Spear' or player.equiped_weapon=='Iron Spear2':
                new_sword = myclasses.Spear(player.rect.centerx, player.rect.centery, player.direction , player.rect.size, player.equiped_weapon)
                user_weapons.add(new_sword)
                all_sprites.add(new_sword)
                new_sword.shoot_sound.play()
            weapon_out = False
            last_tick=now

    if fire_magic_out == True or lighting_magic_out == True or ice_magic_out == True:
        now = pygame.time.get_ticks()
        if now - last_tick>=1000:
            if fire_magic_out == True:
                new_bullet = myclasses.Bullet(player.rect.centerx, player.rect.centery, player.direction, 'firebolt')
            if lighting_magic_out == True:
                new_bullet = myclasses.Bullet(player.rect.centerx, player.rect.centery, player.direction, 'lightingbolt')
            if ice_magic_out == True:
                new_bullet = myclasses.Bullet(player.rect.centerx, player.rect.centery, player.direction, 'iceball')
            if player.Mana - new_bullet.Mana_cost >=0:
                player_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
                fire_magic_out = False
                lighting_magic_out = False
                ice_magic_out = False
                player.Mana = player.Mana - new_bullet.Mana_cost
                myclasses.calc_exp_gain(player,enemies,'WIS',False,player.level_up_sound,mana_used=new_bullet.Mana_cost )
                last_tick=now
            else:
                new_bullet.kill()
    #player action updates
    user_weapons.update()
    player_bullets.update()


    """
    enemy action
    """
    for entity in enemies:
        if entity.rect.centerx - player.rect.centerx <= PLAY_WIDTH / 2 or entity.rect.centery - player.rect.centery <= PLAY_HEIGHT / 2:
            entity.update(random.randint(0, 4),player)

    enemy_bullets.update()

    """
    collide
    """
    # collide with enemy
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        if col_timer == 0:
            collision_sound.play()
            entity = pygame.sprite.spritecollideany(player, enemies)
            dmg= myclasses.calc_dmg_col(entity, player)
            myclasses.calc_exp_gain(player, entity, 'VIG', False, player.level_up_sound, dmg)
            player.HP = player.HP - dmg
            myclasses.move_ob(player,player.direction,player.speed*2,ob_tiles)
    col_timer += 1
    if col_timer >= 30:
        col_timer = 0
    # weapon hit enemy

    mycollides.weapon_enemy_collide(user_weapons,enemies,player,screen,dmg_txts, treasureboxes, all_sprites,ob_tiles)

    # player bullet hit enemy
    mycollides.weapon_enemy_collide(player_bullets, enemies, player, screen, dmg_txts, treasureboxes, all_sprites,
                                    ob_tiles)
    #player loot
    mycollides.player_treasurebox_collide(player, treasureboxes)

    #player hit by enemy bullet
    mycollides.player_enemy_bullet_collide(player, enemy_bullets, collision_sound,ob_tiles)

    #enter new map
    if pygame.sprite.spritecollideany(player, new_map_tiles):
        LOADMAP_type = 'New'
        LOADMAP_event=pygame.event.Event(LOADMAP)
        pygame.event.post(LOADMAP_event)

    if pygame.sprite.spritecollideany(player, prev_map_tiles):
        LOADMAP_type = 'Prev'
        LOADMAP_event=pygame.event.Event(LOADMAP)
        pygame.event.post(LOADMAP_event)

    #enemy with enemy
    mycollides.enemy_enemy_collide(enemies,ob_tiles)

    # enemy with ob tiles
    for entity in enemies:
        if entity.rect.centerx-player.rect.centerx<=PLAY_WIDTH/2 or entity.rect.centery-player.rect.centery<=PLAY_HEIGHT/2:
            mycollides.enemy_terrain_collide(entity,player, ob_tiles, slow_tiles)


    # bullet hits wall:
    pygame.sprite.groupcollide(enemy_bullets,ob_tiles,True,False)
    pygame.sprite.groupcollide(player_bullets, ob_tiles, True, False)

    if player.HP <= 0:
        print("player died")
        player.kill()
        running = False

    #blit screen


    dmg_txts.update(screen)

    for entity in all_sprites:
        #screen.blit(entity.surf, (entity.rect.left+screen_offset_x, entity.rect.top+screen_offset_y))
        screen.blit(entity.surf, (entity.rect.left , entity.rect.top ))

    screen.fill((0, 0, 0), (PLAY_WIDTH, 0, mapy - PLAY_WIDTH, PLAY_HEIGHT))
    #display player status
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"/ {player.max_HP}", myparameters.SCREEN_WIDTH - 80, 20, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"HP     : {player.HP}", myparameters.SCREEN_WIDTH-180, 20, screen)
    HP_bar=myclasses.Bar('HP', screen)
    HP_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"/ {player.max_Mana}", myparameters.SCREEN_WIDTH - 80, 55, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"Mana: {player.Mana}", myparameters.SCREEN_WIDTH - 180, 55, screen)
    Mana_bar = myclasses.Bar('Mana', screen)
    Mana_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"STR: {player.Strength}", myparameters.SCREEN_WIDTH-180, 100, screen)
    STR_bar = myclasses.Bar('STR', screen)
    STR_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"AGI: {player.Agility}", myparameters.SCREEN_WIDTH-180, 130, screen)
    AGI_bar = myclasses.Bar('AGI', screen)
    AGI_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"VIG: {player.Vigor}", myparameters.SCREEN_WIDTH-180, 160, screen)
    VIG_bar = myclasses.Bar('VIG', screen)
    VIG_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"INT: {player.Intellect}", myparameters.SCREEN_WIDTH-180, 190, screen)
    INT_bar = myclasses.Bar('INT', screen)
    INT_bar.update(player, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 18, f"WIS: {player.Wisdom}", myparameters.SCREEN_WIDTH - 180, 220, screen)
    WIS_bar = myclasses.Bar('WIS', screen)
    WIS_bar.update(player, screen)

    myclasses.Icon('asset/weapon_icon.png',myparameters.SCREEN_WIDTH - 180, 250,screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{player.equiped_weapon}", myparameters.SCREEN_WIDTH - 140, 260,screen)
    myclasses.Icon('asset/armor_icon.png', myparameters.SCREEN_WIDTH - 180, 290, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{player.equiped_armor}",myparameters.SCREEN_WIDTH - 140, 300,screen)

    myclasses.Icon('asset/fire_icon.png', myparameters.SCREEN_WIDTH - 180, 330, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{player.equiped_fire}", myparameters.SCREEN_WIDTH - 140, 340, screen)
    myclasses.Icon('asset/lighting_icon.png', myparameters.SCREEN_WIDTH - 180, 370, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{player.equiped_lighting}", myparameters.SCREEN_WIDTH - 140, 380, screen)
    myclasses.Icon('asset/ice_icon.png', myparameters.SCREEN_WIDTH - 180, 410, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{player.equiped_ice}", myparameters.SCREEN_WIDTH - 140, 420, screen)

    myclasses.Icon('asset/Hpotion.png', myparameters.SCREEN_WIDTH - 180, 470, screen)
    myclasses.Icon('asset/Mpotion.png', myparameters.SCREEN_WIDTH - 130, 470, screen)
    myclasses.Icon('asset/coin.png', myparameters.SCREEN_WIDTH - 80, 470, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"X{myparameters.item_inventory['HP Potion']}",
                           myparameters.SCREEN_WIDTH - 155, 470, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"X{myparameters.item_inventory['Mana Potion']}",
                           myparameters.SCREEN_WIDTH - 105, 470, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"X{myparameters.item_inventory['Gold']}",
                           myparameters.SCREEN_WIDTH - 55, 470, screen)

    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{myparameters.notifications[-3]}",
                           myparameters.SCREEN_WIDTH - 150, 520,screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{myparameters.notifications[-2]}",
                           myparameters.SCREEN_WIDTH - 150, 540, screen)
    myclasses.display_text('asset/Roboto-Black.ttf', 14, f"{myparameters.notifications[-1]}",
                           myparameters.SCREEN_WIDTH - 150, 560, screen)


    screen.blit(player.surf, player.rect)
    clock.tick(30)

    pygame.display.flip()