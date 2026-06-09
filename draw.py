import pygame

def draw_grid(gd, local):
    for i in range(gd.grid_size + 1):
        p = int(local.padding + i * local.step)
        pygame.draw.line(local.screen, (0, 0, 0), (p, local.padding), (p, local.screen_size - local.padding), width=1)
        pygame.draw.line(local.screen, (0, 0, 0), (local.padding, p), (local.screen_size - local.padding, p), width=1)

def draw_captured(gd, local):
    if not gd.captured_areas:
        return
    overlay = pygame.Surface(local.screen.get_size(), pygame.SRCALPHA)
    for color_key, poly in gd.captured_areas:
        if not poly or len(poly) < 3:
            continue
        coords = [(int(local.padding + c * local.step), int(local.padding + r * local.step)) for r, c in poly]
        color = local.colors[gd.player_letters.index(color_key)]
        color = (color[0],color[1], color[2], 128)
        pygame.draw.polygon(overlay, color, coords)
    local.screen.blit(overlay, (0, 0))

def draw_points(gd, local):
    for y in range(gd.grid_size + 1):
        for x in range(gd.grid_size + 1):
            if gd.grid[y][x].upper() in gd.player_letters:
                pygame.draw.circle(local.screen, local.colors[gd.player_letters.index(gd.grid[y][x].upper())],(local.padding + x * local.step, local.padding + y * local.step), local.point_size)

def draw_last_move(gd, local):
    if not gd.last_move is None:
        color = local.colors[gd.player_letters.index(gd.last_move[2])]
        pygame.draw.circle(local.screen, color, (local.padding + gd.last_move[0] * local.step, local.padding + gd.last_move[1] * local.step), local.new_point_size)

def draw_score(gd, local):
    for i in range(gd.player_count):
        text_surface = local.font.render(str(gd.score[gd.player_letters[i]]), True, local.colors[i])
        local.screen.blit(text_surface, text_surface.get_rect(center=((local.screen_size - 2*local.padding)/(gd.player_count -1)  * i + local.padding, local.padding/2)))

