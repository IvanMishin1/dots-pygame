import pygame

def draw_grid(gd, local):
    for i in range(gd.GRID_SIZE + 1):
        p = int(local.padding + i * local.step)
        pygame.draw.line(local.screen, (0, 0, 0), (p, local.padding), (p, local.screen_size - local.padding), width=1)
        pygame.draw.line(local.screen, (0, 0, 0), (local.padding, p), (local.screen_size - local.padding, p), width=1)

def draw_captured(gd, local):
    if not gd.captured:
        return
    overlay = pygame.Surface(local.screen.get_size(), pygame.SRCALPHA)
    for color_key, poly in gd.captured:
        if not poly or len(poly) < 3:
            continue
        coords = [(int(local.padding + c * local.step), int(local.padding + r * local.step)) for r, c in poly]
        color = (0, 0, 255, 128) if color_key == "B" else (255, 0, 0, 128)
        pygame.draw.polygon(overlay, color, coords)
    local.screen.blit(overlay, (0, 0))

def draw_points(gd, local):
    for y in range(gd.GRID_SIZE + 1):
        for x in range(gd.GRID_SIZE + 1):
            if gd.grid[y][x] == "R":
                pygame.draw.circle(local.screen, local.color_red, (local.padding + x * local.step, local.padding + y * local.step), 7)
            elif gd.grid[y][x] == "r":
                pygame.draw.circle(local.screen, local.color_red, (local.padding + x * local.step, local.padding + y * local.step), 7)
            elif gd.grid[y][x] == "B":
                pygame.draw.circle(local.screen, local.color_blue, (local.padding + x * local.step, local.padding + y * local.step), 7)
            elif gd.grid[y][x] == "b":
                pygame.draw.circle(local.screen, local.color_blue, (local.padding + x * local.step, local.padding + y * local.step), 7)

def draw_last_move(gd, local):
    if not gd.last_move is None:
        if gd.last_move[2] == "B":
            color = local.color_blue
        else:
            color = local.color_red
        pygame.draw.circle(local.screen, color, (local.padding + gd.last_move[0] * local.step, local.padding + gd.last_move[1] * local.step), 9)

def draw_score(gd, local):
    text_surface = local.font.render(str(gd.score["B"]), True, local.color_blue)
    local.screen.blit(text_surface, text_surface.get_rect(center=(local.screen_size/2 - local.screen_size/6, local.padding/2)))
    text_surface = local.font.render(str(gd.score["R"]), True, local.color_red)
    local.screen.blit(text_surface, text_surface.get_rect(center=(local.screen_size/2 + local.screen_size/6, local.padding/2)))
