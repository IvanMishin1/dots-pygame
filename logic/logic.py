from collections import deque

def capture(row, col, capturer_color, captured_color, gd):
    grid_size = len(gd.grid)
    a_pos = (row[0], col[0])

    enclosed = set()
    queue = deque([a_pos])
    enclosed.add(a_pos)

    # Find the enclosed area
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size and (nr, nc) not in enclosed and gd.grid[nr][nc] != capturer_color:
                enclosed.add((nr, nc))
                queue.append((nr, nc))

    # Update score for recaptured points
    for r, c in enclosed:
        if gd.grid[r][c] == capturer_color.lower():
            gd.grid[r][c] = capturer_color  # mark ownership removed
            gd.score[captured_color] -= 1

    # Make newly captured points inactive
    for i in range(len(row)):
        if gd.grid[row[i]][col[i]] == captured_color:
            gd.grid[row[i]][col[i]] = str(gd.grid[row[i]][col[i]]).lower()
            gd.score[capturer_color] += 1

    # Get wall coordinates
    wall = set()
    for r, c in enclosed:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size and gd.grid[nr][nc] == capturer_color:
                wall.add((nr, nc))
    wall = list(wall)

    if not wall:
        return

    # Sort the coordinates in a way to draw a polygon
    sorted_coords = moore_trace(wall)
    gd.captured_areas.append((capturer_color, sorted_coords))

def check_borders(capturer_color, captured_color, gd):
    # Create a copy of a grid for the fill
    #g = [row[:] for row in gd.grid]
    grid_size = len(gd.grid)
    visited_outside = set()

    # Create border points for fill
    for k in range(grid_size):
        for r, c in [(0, k), (grid_size - 1, k), (k, 0), (k, grid_size - 1)]:
            if gd.grid[r][c] != capturer_color:
                visited_outside.add((r,c))

    # Start the fill
    queue = deque()
    for i in range(grid_size):
        for j in range(grid_size):
            if (i,j) in visited_outside:
                queue.append((i, j))
    while queue:
        y, x = queue.popleft()
        # Check all 4 neighbors
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < grid_size and 0 <= nx < grid_size and (ny, nx) not in visited_outside and gd.grid[ny][nx] != capturer_color:
                visited_outside.add((ny,nx))
                queue.append((ny, nx))

    # Check for captures
    visited_inside = set()
    for i in range(grid_size):
        for j in range(grid_size):
            if (not (i,j) in visited_outside) and gd.grid[i][j] == captured_color and (i, j) not in visited_inside:
                region_rows = [i]
                region_cols = [j]
                visited_inside.add((i, j))
                queue = deque([(i, j)])
                while queue:
                    y, x = queue.popleft()
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < grid_size and 0 <= nx < grid_size and (ny,nx) not in visited_outside and (ny, nx) not in visited_inside and gd.grid[ny][nx] == captured_color:
                            visited_inside.add((ny, nx))
                            queue.append((ny, nx))
                            region_rows.append(ny)
                            region_cols.append(nx)
                # Send all captured coordinates INCLUDING blank spaces
                capture(region_rows, region_cols, capturer_color, captured_color,gd)

def moore_trace(wall):
    wall = set(wall)
    start = min(wall) # Top-left point

    # Clockwise directions
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    boundary = [start]
    current = start
    visited = {start}
    rev_dir_index = 0
    while True:
        found_next = False
        for i in range(len(dirs)):
            d = dirs[(rev_dir_index + i) % 8]
            next = (current[0] + d[0], current[1] + d[1])
            if next in wall:
                boundary.append(next)
                visited.add(next)
                current = next
                rev_dir_index = (dirs.index(d) + 5) % 8
                found_next = True
                break
        if not found_next:
            break
        if current == start and len(boundary) > 2:
            break
    return boundary