from logic.DotsGame import *
from copy import deepcopy
from collections import deque
import numpy as np


# Evaluates the current position based on the current score and the id of the player whose turn it is to move
def evaluate_pos(gd, player_letter):
    score = 0
    opponent_letter = next(p for p in gd.score if p != player_letter)
    score += gd.score[player_letter] - gd.score[opponent_letter]
    """
    points = gd.get_player_dots(player_letter)
    arr = np.asarray(points, dtype=float)
    if arr.ndim == 2 and arr.shape[1] == 2 and arr.shape[0] >= 2:
        centroid = arr.mean(axis=0)
        distances = np.linalg.norm(arr - centroid, axis=1)
        variance = float(np.var(distances))
        score -= variance * 0.1
    """
    return float(score)

def reasonable_moves(gd, max_dist=2):
    legal = gd.get_legal_moves()
    size = len(gd.grid)

    occupied = {
        (x, y)
        for y in range(size)
        for x in range(size)
        if gd.grid[y][x] != ' '
    }

    if not occupied:
        return legal

    near = set()
    dist = {}
    queue = deque()

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
    return list(set(legal) & near)

def minimax(gd, depth, is_maximizing_player, player_letter, alpha, beta):
    moves = reasonable_moves(gd)

    if depth == 0 or not moves:
        return evaluate_pos(gd, player_letter)

    if is_maximizing_player:
        max_eval = float('-inf')
        for x, y in moves:
            next_gd = deepcopy(gd)
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
            next_gd = deepcopy(gd)
            next_gd.make_move(x, y)
            evaluation = minimax(next_gd, depth - 1, True, player_letter, alpha, beta)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def find_move(gd, depth = 3):
    player_letter = gd.player_letters[gd.player_turn]

    # TODO: REMOVE THIS DEBUG
    if player_letter == "R":
        depth = 1
    else:
        depth = 6

    # Check if any moves exist
    moves = reasonable_moves(gd)
    if not moves:
        return None

    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for x, y in moves:
        next_gd = deepcopy(gd)
        next_gd.make_move(x, y)

        score = minimax(next_gd, depth - 1, False, player_letter, alpha, beta)

        if score > best_score:
            best_score = score
            best_move = (x, y)
        alpha = max(alpha, score)

    return best_move

