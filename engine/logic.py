from collections import deque

def capture(row, col, g, capturer_color, captured_color, gd):
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
        if gd.grid[i[0]][i[1]] == capturer_color.lower():
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
            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == capturer_color:
                wall.add((nr, nc))
    wall = list(wall)

    if not wall:
        return

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
    gd.captured.append((capturer_color, sorted_coords))

def check_borders(capturer_color, captured_color, gd):
    # Create a copy of a grid for the fill
    g = [row[:] for row in gd.grid]

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
            if g[i][j] == " " and gd.grid[i][j] == captured_color and (i, j) not in visited:
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
                # Send all captured coordinates INCLUDING blank spaces
                capture(region_rows, region_cols, g, capturer_color, captured_color,gd)
