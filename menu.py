import asyncio
import sys
import os
import pygame
import pygame_menu
from main import main

pygame.init()
surface = pygame.display.set_mode((520, 400))
pygame.display.set_caption("Dots")

# Handle asset path for pyinstaller
if getattr(sys, 'frozen', False):
    asset_dir = os.path.join(sys._MEIPASS, 'assets')
else:
    asset_dir = 'assets'

player_count = 1
grid_size = 20

def set_player_count(selected_item, selected_index):
    global player_count
    player_count = selected_index

def set_grid_size(selected_item, selected_index):
    global grid_size
    grid_size = selected_index

def play():
    asyncio.run(main(player_count, grid_size))

main_menu = pygame_menu.Menu('Dots', 520, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

options_menu = pygame_menu.Menu('Options', 520, 400,
                                theme=pygame_menu.themes.THEME_BLUE)

guide_menu = pygame_menu.Menu('Guide', 520, 400,
                                theme=pygame_menu.themes.THEME_BLUE)

main_menu.add.button("Play", options_menu)
main_menu.add.button("Guide", guide_menu)
main_menu.add.button('Quit', pygame_menu.events.EXIT)


options_menu.add.selector('Player count : ', [('1 (PvM)', 1), ('2 (PvP)', 2), ('3 (PvP)', 3), ('4 (PvP)', 4)], onchange=set_player_count)
options_menu.add.selector('Grid size : ', [('20*20 (Classic)', 20), ('25*25 (Large)', 25), ('15*15 (Small)', 15)], onchange=set_grid_size)

options_menu.add.button('Start Game', play)
options_menu.add.button("Back", pygame_menu.events.BACK)

guide_menu.add.image(image_path=os.path.join(asset_dir, 'guide.png'), scale_smooth=True)
guide_menu.add.button("Back", pygame_menu.events.BACK)

main_menu.mainloop(surface)
