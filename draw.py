import pygame

def draw_grid(gd):
    for i in range(gd.grid_size + 1):
        p = int(gd.padding + i * gd.step)
        pygame.draw.line(gd.screen, (0, 0, 0), (p, gd.padding), (p, gd.screen_size - gd.padding), width=1)
        pygame.draw.line(gd.screen, (0, 0, 0), (gd.padding, p), (gd.screen_size - gd.padding, p), width=1)

def draw_captured(gd):
    if not gd.captured:
        return
    overlay = pygame.Surface(gd.screen.get_size(), pygame.SRCALPHA)
    for color_key, poly in gd.captured:
        if not poly or len(poly) < 3:
            continue
        coords = [(int(gd.padding + c * gd.step), int(gd.padding + r * gd.step)) for r, c in poly]
        color = (0, 0, 255, 128) if color_key == "B" else (255, 0, 0, 128)
        pygame.draw.polygon(overlay, color, coords)
    gd.screen.blit(overlay, (0, 0))

def draw_points(gd):
    for y in range(gd.grid_size +1):
        for x in range(gd.grid_size +1):
            if gd.grid[y][x] == "R":
                pygame.draw.circle(gd.screen, gd.color_red, (gd.padding + x * gd.step, gd.padding + y * gd.step), 7)
            elif gd.grid[y][x] == "r":
                pygame.draw.circle(gd.screen, gd.color_red, (gd.padding + x * gd.step, gd.padding + y * gd.step), 7)
            elif gd.grid[y][x] == "B":
                pygame.draw.circle(gd.screen, gd.color_blue, (gd.padding + x * gd.step, gd.padding + y * gd.step), 7)
            elif gd.grid[y][x] == "b":
                pygame.draw.circle(gd.screen, gd.color_blue, (gd.padding + x * gd.step, gd.padding + y * gd.step), 7)

def draw_last_move(gd):
    if not gd.last_move is None:
        pygame.draw.circle(gd.screen, gd.last_move[2], (gd.padding + gd.last_move[0] * gd.step, gd.padding + gd.last_move[1] * gd.step), 9)

def draw_score(gd):
    text_surface = gd.font.render(str(gd.score["B"]), True, gd.color_blue)
    gd.screen.blit(text_surface, text_surface.get_rect(center=(gd.screen_size/2 - gd.screen_size/6, gd.padding/2)))
    text_surface = gd.font.render(str(gd.score["R"]), True, gd.color_red)
    gd.screen.blit(text_surface, text_surface.get_rect(center=(gd.screen_size/2 + gd.screen_size/6, gd.padding/2)))
