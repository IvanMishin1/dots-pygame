from draw import *
from engine import engine
from logic.DotsGame import DotsGame
import asyncio
import pygame

GRID_SIZE = 5
PLAYER_COUNT = 2

class LocalSettings:
    def __init__(self, grid_size):
        # Game config
        self.screen_size = 512
        self.padding = 70

        # Derived values
        self.step = (self.screen_size - 2 * self.padding) / grid_size

        # Colors / UI
        self.colors = [(255, 0, 0),(0, 0, 255),(50, 168, 82),(0, 255, 255),(255, 0, 255),(255, 255, 0)]
        self.point_size = (self.screen_size - self.padding) / grid_size / 4
        self.new_point_size = self.point_size * 1.3

        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

        self.is_pvp = True

async def main(PLAYER_COUNT, GRID_SIZE):
    pygame.init()

    local = LocalSettings(GRID_SIZE)
    if PLAYER_COUNT == 1:
        local.is_pvp = False
        PLAYER_COUNT += 1

    state = DotsGame(GRID_SIZE, PLAYER_COUNT)
    pygame.display.set_caption("Dots")
    clock = pygame.time.Clock()


    suggested_move = None # TODO: THIS IS DEBUG


    while True:
        #move = engine.find_move(state, 2)
        #if not move is None:
        #    state.make_move(*engine.find_move(state, 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                gx = round((pos[0]- local.padding) / local.step)
                gy = round((pos[1]- local.padding) / local.step)

                if gx in range(0,GRID_SIZE + 1) and gy in range(0,GRID_SIZE + 1):
                    state = state.make_move(gx,gy)
                    if not local.is_pvp:
                        suggested_move = engine.find_move(state, 2)
                        state = state.make_move(*suggested_move)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = DotsGame(GRID_SIZE, PLAYER_COUNT)

        local.screen.fill("white")
        draw_grid(state, local)
        draw_points(state, local)
        draw_captured(state, local)
        draw_score(state, local)
        draw_last_move(state, local)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

#asyncio.run(main(PLAYER_COUNT, GRID_SIZE))