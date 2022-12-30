import pygame
import myparameters
import pygame_menu

SCREEN_HEIGHT = myparameters.SCREEN_HEIGHT
SCREEN_WIDTH = myparameters.SCREEN_WIDTH
PLAY_HEIGHT = myparameters.PLAY_HEIGHT
PLAY_WIDTH = myparameters.PLAY_WIDTH

pygame.init()
pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ABOUT = ['My First RPG',
         'Yanshui Jiang',
         'Email: jerryjiang1217@gmail.com']



# --------------------
# main menu function
# --------------------
def menu_init( player):
    #main level
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.6, theme=main_theme, title='Main Menu', width=PLAY_WIDTH * 0.6)
    about_menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.6,theme=main_theme,title='About',width=PLAY_WIDTH * 0.6)
    equip_menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.8,theme=main_theme,title='Equipments',width=PLAY_WIDTH * 0.8,
                                  columns=4, rows=2)
    spell_menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.8,theme=main_theme,title='Spells',width=PLAY_WIDTH * 0.8)

    #sublevel
    quit_menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4,theme=main_theme,title='Quit',width=PLAY_WIDTH * 0.4)
    quit_menu.add.label('Are You Sure?', align=pygame_menu.locals.ALIGN_LEFT, font_size=32)
    quit_menu.add.button('Yes',pygame_menu.events.EXIT)
    quit_menu.add.button('No', pygame_menu.events.BACK)

    def back_to_game():
        main_menu.disable()

    main_menu.add.button('Resume', back_to_game)
    main_menu.add.button('Equip', equip_menu)
    main_menu.add.button('Spell', spell_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', quit_menu)

# --------------------
# Equip Menu
# --------------------
    def change_weapon(input):
        player.equiped_weapon = input
        if player.equiped_weapon == 'Iron Sword' or player.equiped_weapon == 'Steel Sword':
            player.current_weapon_cooldown=333
        elif player.equiped_weapon == 'Claymore':
            player.current_weapon_cooldown=666
        elif player.equiped_weapon == 'Iron Spear':
            player.current_weapon_cooldown=800
        main_menu.disable()

    def change_armor(input):
        player.equiped_armor = input
        if player.equiped_armor == 'Leather Armor' :
            player.equiped_armor_defense = 5
        elif player.equiped_armor == 'Iron Armor' :
            player.equiped_armor_defense = 10
            print(f'menu: player armor : {player.equiped_armor_defense}')
        main_menu.disable()


    Iron_Sword_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4,theme=main_theme,title='Iron Sword',width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Damage: 3-6','Speed: 3']
    for m in Weapon_desc:
        Iron_Sword_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Iron_Sword_Menu.add.button('Equip', change_weapon, 'Iron Sword')

    Steel_Sword_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4, theme=main_theme, title='Steel Sword',
                                       width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Damage: 8-12', 'Speed: 3']
    for m in Weapon_desc:
        Steel_Sword_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Steel_Sword_Menu.add.button('Equip', change_weapon,'Steel Sword')

    #claymore
    Claymore_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4, theme=main_theme, title='Claymore',
                                        width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Damage: 12-20', 'Speed: 1.5']
    for m in Weapon_desc:
        Claymore_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Claymore_Menu.add.button('Equip', change_weapon, 'Claymore')

    # iron spear
    Iron_Spear_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4, theme=main_theme, title='Iron Spear',
                                     width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Damage: 16-24', 'Speed: 1.25']
    for m in Weapon_desc:
        Iron_Spear_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Iron_Spear_Menu.add.button('Equip', change_weapon, 'Iron Spear')

    # leather armor
    Leather_Armor_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4, theme=main_theme, title='Leather Armor',
                                     width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Defense: 10']
    for m in Weapon_desc:
        Leather_Armor_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Leather_Armor_Menu.add.button('Equip', change_armor, 'Leather Armor')

    #iron armor
    Iron_Armor_Menu = pygame_menu.Menu(height=PLAY_HEIGHT * 0.4, theme=main_theme, title='Iron Armor',
                                       width=PLAY_WIDTH * 0.4)
    Weapon_desc = ['Defense: 10']
    for m in Weapon_desc:
        Iron_Armor_Menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    Iron_Armor_Menu.add.button('Equip', change_armor, 'Iron Armor')

    #equip menu list
    weapon_menu = {
        'Iron Sword': Iron_Sword_Menu,
        'Steel Sword': Steel_Sword_Menu,
        'Claymore': Claymore_Menu,
        'Iron Spear': Iron_Spear_Menu,
        'Leather Armor': Leather_Armor_Menu,
        'Iron Armor': Iron_Armor_Menu
    }

    weapon_menu_col = {
        'Iron Sword': 1,
        'Steel Sword': 1,
        'Claymore': 2,
        'Iron Spear': 3,
        'Leather Armor': 4,
        'Iron Armor': 4
    }


    for item in myparameters.weapon_inventory:
        if myparameters.weapon_inventory[item]:
            equip_menu.add.button(item, weapon_menu[item])
    pygame.display.flip()
    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)


    return main_menu

# --------------------
# other function
# --------------------





