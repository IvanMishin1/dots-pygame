from draw import *
from logic import *
from dataclasses import dataclass

pygame.init()

@dataclass
class GameData:
    blueTurn: bool = True
    screen_size: int = 512
    grid_size: int = 20
    padding: int = 70
    step = (screen_size - 2 * padding) / grid_size
    color_blue = (0,0,255)
    color_red = (255,0,0)
    score= {
        'B': 0,
        'R': 0,
    }
    grid = []
    screen = pygame.display.set_mode((screen_size, screen_size))
    font = pygame.font.Font(pygame.font.get_default_font(), 40)
    captured = []
    last_move = None

gd = GameData()

for _ in range(gd.grid_size + 1):
    gd.grid.append([])
    for _ in range(gd.grid_size + 1):
        gd.grid[-1].append(" ")

pygame.display.set_caption("Dots")
clock = pygame.time.Clock()

while True:
    gd.screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            gx = round((pos[0]- gd.padding) / gd.step)
            gy = round((pos[1]- gd.padding) / gd.step)

            if gx in range(0,gd.grid_size + 1) and gy in range(0,gd.grid_size + 1) and not gd.grid[gy][gx] != " ":
                new_point(gx,gy, gd)
                if gd.blueTurn:
                    check_borders("B","R", gd)
                    check_borders("R","B", gd)
                    gd.last_move = (gx,gy,gd.color_blue)
                else:
                    check_borders("R","B", gd)
                    check_borders("B","R", gd)
                    gd.last_move = (gx,gy,gd.color_red)
                gd.blueTurn = not gd.blueTurn

    draw_grid(gd)
    draw_points(gd)
    draw_captured(gd)
    draw_score(gd)
    draw_last_move(gd)

    pygame.display.flip()
    clock.tick(60)
