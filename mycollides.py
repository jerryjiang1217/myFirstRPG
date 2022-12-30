import random
import pygame
import myparameters
import myclasses


SCREEN_HEIGHT = myparameters.SCREEN_HEIGHT
SCREEN_WIDTH = myparameters.SCREEN_WIDTH
PLAY_HEIGHT = myparameters.PLAY_HEIGHT
PLAY_WIDTH = myparameters.PLAY_WIDTH


def weapon_enemy_collide(user_weapons, enemies, player, screen,dmg_txts, treasureboxes, all_sprites, ob_tiles):
    for entity in user_weapons:
        if pygame.sprite.spritecollideany(entity, enemies):
            entity.collide_sound.play()
            collided = pygame.sprite.spritecollideany(entity, enemies)
            entity.rect.size = (1, 1)
            dmg = myclasses.calc_dmg(player, entity, collided, entity.tag)
            collided.HP = collided.HP - dmg
            myclasses.calc_exp_gain(player, collided, entity.tag, False, player.level_up_sound)
            if collided.HP <= 0:
                collided.enemy_kill_sound.play()
                myclasses.calc_exp_gain(player, collided, entity.tag, True, player.level_up_sound)
                myclasses.enemy_drop(collided, treasureboxes, all_sprites)
                collided.kill()

            new_dmg_txt = myclasses.Dmg_txt(f"-{dmg}", collided.rect.left, collided.rect.bottom, screen)
            dmg_txts.add(new_dmg_txt)
            if entity.tag == 'Iron Sword' or entity.tag == 'Steel Sword' or entity.tag == 'Claymore':
                myclasses.hit_bounce(collided, player.direction, 20, ob_tiles)
            if entity.tag=='firebolt':
                entity.kill()
            if entity.tag=='iceball':
                entity.lifecycle -= 1
                if entity.lifecycle == 0:
                    entity.kill()

def player_treasurebox_collide(player,treasureboxes):
    if pygame.sprite.spritecollideany(player, treasureboxes):
        entity=pygame.sprite.spritecollideany(player, treasureboxes)
        entity.bonus_sound.play()
        myclasses.loot_treasurebox(entity)
        entity.kill()

def player_enemy_bullet_collide(player, enemy_bullets,collision_sound, ob_tiles):
    if pygame.sprite.spritecollideany(player, enemy_bullets):
        entity=pygame.sprite.spritecollideany(player, enemy_bullets)
        dmg = myclasses.calc_dmg(entity, None, player,  entity.tag)
        myclasses.calc_exp_gain(player, entity, 'VIG', False, player.level_up_sound, dmg)
        player.HP -= dmg
        myclasses.move_ob(player, player.direction, player.speed, ob_tiles)
        entity.kill()
        collision_sound.play()

# with differnt terrain
def enemy_terrain_collide(mover, player, ob_sprites, slow_tiles):
    if pygame.sprite.spritecollideany(mover, ob_sprites):
        myclasses.move_ob(mover, mover.direction, mover.speed, ob_sprites)
        x_dist = abs(mover.rect.centerx - player.rect.centerx)
        y_dist = abs(mover.rect.centery - player.rect.centery)

        if x_dist > y_dist and mover.rect.centery > player.rect.centery:
            mover.direction = 1
        elif x_dist > y_dist and mover.rect.centery < player.rect.centery:
            mover.direction = 2
        elif x_dist < y_dist and mover.rect.centerx > player.rect.centerx:
            mover.direction = 3
        elif x_dist < y_dist and mover.rect.centerx < player.rect.centerx:
            mover.direction = 4

        #mover.update(random.randint(1,4),player, collide=True) # enemy change direction when hit wall

# enemies with enemies
def enemy_enemy_collide(enemies, ob_tiles):
    for entity in enemies:
        if pygame.sprite.spritecollideany(entity, enemies):
            collided=pygame.sprite.spritecollideany(entity, enemies)
            if collided != entity:
               myclasses.move_ob(entity, entity.direction, entity.speed, ob_tiles)
