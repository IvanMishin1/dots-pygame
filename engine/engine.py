import random

from collections import deque
import numpy as np

# Evaluates the current position based on the current score and the id of the player whose turn it is to move
def evaluate_pos(gd, player_letter):
    score = 0
    opponent_letter = next(p for p in gd.score if p != player_letter)
    score += gd.score[player_letter] - gd.score[opponent_letter]
    points = gd.player_moves[player_letter]
    arr = np.asarray(points, dtype=float)
    if arr.ndim == 2 and arr.shape[1] == 2 and arr.shape[0] >= 2:
        centroid = arr.mean(axis=0)
        distances = np.linalg.norm(arr - centroid, axis=1)
        variance = float(np.var(distances))
        score -= variance * 0.1

    return float(score)

def reasonable_moves(gd, max_dist=2):
    size = len(gd.grid)

    if gd.last_move is None:
        return gd.legal_moves

    near = set()
    dist = {}
    queue = deque()

    occupied = set()
    for moves in gd.player_moves.values():
        occupied.update(moves)

    for pos in occupied:
        dist[pos] = 0
        queue.append((pos, 0))

    while queue:
        (x, y), d = queue.popleft()
        if d < max_dist:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in dist:
                        dist[(nx, ny)] = d + 1
                        near.add((nx, ny))
                        queue.append(((nx, ny), d + 1))
    reasonable_moves = list(set(gd.legal_moves) & near)
    if gd.last_move is not None:
        reasonable_moves.sort(key=lambda p: (p[0] - gd.last_move[0]) ** 2 + (p[1] - gd.last_move[1]) ** 2)
    return reasonable_moves

def minimax(gd, depth, is_maximizing_player, player_letter, alpha, beta):
    moves = reasonable_moves(gd)

    if depth == 0 or not moves:
        return evaluate_pos(gd, player_letter)

    if is_maximizing_player:
        max_eval = float('-inf')
        for x, y in moves:
            next_gd = gd.make_copy()
            next_gd.make_move(x, y)
            evaluation = minimax(next_gd, depth - 1, False, player_letter, alpha, beta)
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for x, y in moves:
            next_gd = gd.make_copy()
            next_gd.make_move(x, y)
            evaluation = minimax(next_gd, depth - 1, True, player_letter, alpha, beta)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def find_move(gd, depth):
    player_letter = gd.player_letters[gd.player_turn]

    # Check if any moves exist
    moves = reasonable_moves(gd)

    if gd.last_move is None:
        return random.choice(moves)

    if not moves:
        return None

    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for x, y in moves:
        next_gd = gd.make_copy()
        next_gd.make_move(x, y)

        score = minimax(next_gd, depth - 1, False, player_letter, alpha, beta)

        if score > best_score:
            best_score = score
            best_move = (x, y)
        alpha = max(alpha, score)

    return best_move

