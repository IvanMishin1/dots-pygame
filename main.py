import pygame
from collections import deque

pygame.init()

screen_size = 512
grid_size = 9
padding = 70
step = (screen_size - 2 * padding) / grid_size
blueTurn = True

color_blue = (0,0,255)
color_red = (255,0,0)

score ={
    'B': 0,
    'R': 0,
}

grid = []
for _ in range(grid_size + 1):
    grid.append([])
    for _ in range(grid_size + 1):
        grid[-1].append(" ")

captured = []
screen = pygame.display.set_mode((screen_size,screen_size),pygame.SRCALPHA)
font = pygame.font.Font(pygame.font.get_default_font(), 40)

pygame.display.set_caption("Dots")

clock = pygame.time.Clock()

def draw_grid():
    for i in range(grid_size + 1):
        p = int(padding + i * step)
        pygame.draw.line(screen, (0, 0, 0), (p, padding), (p, screen_size - padding), width=1)
        pygame.draw.line(screen, (0, 0, 0), (padding, p), (screen_size - padding, p), width=1)

def draw_captured():
    for color_key, poly in captured:
        if len(poly) < 3:
            continue
        coords = [(padding + c * step, padding + r * step) for r, c in poly]

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        if color_key == "B":
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)

        pygame.draw.polygon(overlay, color, coords)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

def draw_points():
    for y in range(grid_size +1):
        for x in range(grid_size +1):
            if grid[y][x] == "R":
                pygame.draw.circle(screen, color_red, (padding + x * step, padding + y * step), 7)
            elif grid[y][x] == "r":
                pygame.draw.circle(screen, color_red, (padding + x * step, padding + y * step), 7)
            elif grid[y][x] == "B":
                pygame.draw.circle(screen, color_blue, (padding + x * step, padding + y * step), 7)
            elif grid[y][x] == "b":
                pygame.draw.circle(screen, color_blue, (padding + x * step, padding + y * step), 7)

def draw_score():
    global score
    text_surface = font.render(str(score["B"]), True, color_blue)
    screen.blit(text_surface, text_surface.get_rect(center=(screen_size/2 - screen_size/6, padding/2)))
    text_surface = font.render(str(score["R"]), True, color_red)
    screen.blit(text_surface, text_surface.get_rect(center=(screen_size/2 + screen_size/6, padding/2)))

def is_occupied(x,y):
    return grid[y][x] != " "

def capture(row, col, g, capturer_color, captured_color):
    global score
    rows = len(g)
    cols = len(g[0])
    a_pos = (row[0], col[0])

    enclosed = set()
    queue = deque([a_pos])
    enclosed.add(a_pos)

    # Find the enclosed area
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in enclosed and g[nr][nc] != capturer_color:
                enclosed.add((nr, nc))
                queue.append((nr, nc))

    # Update score for recaptured points
    for i in enclosed:
        if grid[i[0]][i[1]] == capturer_color.lower():
            score[captured_color] -= 1

    # Make newly captured points inactive
    for i in range(len(row)):
        if grid[row[i]][col[i]] == captured_color:
            grid[row[i]][col[i]] = str(grid[row[i]][col[i]]).lower()
            score[capturer_color] += 1

    print("ENCLOSED" + str(enclosed))

    # Get wall coordinates
    wall = set()
    for r, c in enclosed:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == capturer_color:
                wall.add((nr, nc))
    wall = list(wall)

    # Sort the coordinates in a way to draw a polygon
    sorted_coords = [wall[0]]
    for i in range(len(wall)):
        for j in [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(0,1),(1,0)]:
            neighbour = (sorted_coords[-1][0] + j[0],sorted_coords[-1][1] + j[1])
            if neighbour in sorted_coords:
                continue
            if neighbour in wall:
                sorted_coords.append(neighbour)
                break
        if len(sorted_coords) > 2 and sorted_coords[0] == sorted_coords[-1]:
            break

    print("WALL" + str(wall))
    print("SORTED WALL" + str(sorted_coords))
    captured.append((capturer_color, sorted_coords))

def check_borders(capturer_color, captured_color):
    # Create a copy of a grid for the fill
    g = [row[:] for row in grid]

    # Filter the grid
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] != capturer_color:
                g[i][j] = " "

    # Create border points for fill
    for k in range(len(g)):
        for r, c in [(0, k), (len(g) - 1, k), (k, 0), (k, len(g) - 1)]:
            if g[r][c] == " ":
                g[r][c] = "*"

    # Start the fill
    queue = deque()
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] == "*":
                queue.append((i, j))
    while queue:
        y, x = queue.popleft()
        # Check all 4 neighbors
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(g) and 0 <= nx < len(g[ny]) and g[ny][nx] == " ":
                g[ny][nx] = "*"
                queue.append((ny, nx))

    # Check for captures
    visited = set()
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] == " " and grid[i][j] == captured_color and (i, j) not in visited:
                region_rows = [i]
                region_cols = [j]
                visited.add((i, j))
                queue = deque([(i, j)])
                while queue:
                    y, x = queue.popleft()
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < len(g) and 0 <= nx < len(g[ny]) and g[ny][nx] == " " and (ny, nx) not in visited:
                            g[ny][nx] = "*"
                            visited.add((ny, nx))
                            queue.append((ny, nx))
                            region_rows.append(ny)
                            region_cols.append(nx)
                # Send all captured coordinates INCLUDING blanc spaces
                capture(region_rows, region_cols, g, capturer_color, captured_color)

    #for i in g:
    #    print(i)

def new_point(x,y):
    global blueTurn
    if blueTurn:
        grid[y][x] = "B"
    else:
        grid[y][x] = "R"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            gx = round((pos[0]- padding) / step)
            gy = round((pos[1]- padding) / step)

            if gx in range(0,grid_size + 1) and gy in range(0,grid_size + 1) and not is_occupied(gx,gy):
                print(gx,gy)
                new_point(gx,gy)
                if blueTurn:
                    check_borders("B","R")
                    check_borders("R","B")
                else:
                    check_borders("R","B")
                    check_borders("B","R")
                blueTurn = not blueTurn

    screen.fill("white")

    draw_grid()
    draw_points()
    draw_captured()
    draw_score()

    pygame.display.flip()
    clock.tick(60)
