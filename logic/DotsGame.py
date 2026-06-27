from copy import deepcopy
from logic.logic import *

class DotsGame:
    def __init__(self, grid_size, player_count):
        # Game config
        self.player_count = player_count
        self.player_turn = 0
        self.grid_size = grid_size

        # Game state
        self.player_letters = ["R","B","G","C","M","Y"]
        self.score = {self.player_letters[n]: 0 for n in range(self.player_count)}
        self.grid = [[' ' for _ in range(self.grid_size + 1)] for _ in range(self.grid_size + 1)]
        self.captured_areas = []
        self.last_move = None

        # Helper variables
        self.legal_moves = [(x,y) for y in range(grid_size + 1) for x in range(grid_size + 1)]
        self.player_moves = {self.player_letters[n]: [] for n in range(self.player_count)}

    def get_captured(self):
        return self.captured_areas.copy()

    def get_legal_moves(self):
        return self.legal_moves.copy()

    def make_move(self, x, y):
        if not (x,y) in self.legal_moves:
            print((x,y), "not in", self.legal_moves)
            print("Illegal Move", x,y)
            return self

        self.grid[y][x] = self.player_letters[self.player_turn]
        self.last_move = (x, y, self.player_letters[self.player_turn])
        self.player_moves[self.player_letters[self.player_turn]].append((x,y))
        self.legal_moves.remove((x,y))


        # Regular captures
        for i in range(self.player_count):
            if i != self.player_turn:
                check_borders(self.player_letters[self.player_turn], self.player_letters[i], self)

        # Auto-captures
        for i in range(self.player_count):
            if i != self.player_turn:
                check_borders(self.player_letters[i], self.player_letters[self.player_turn], self)

        if self.player_turn == self.player_count - 1 :
            self.player_turn = 0
        else:
            self.player_turn += 1
        return self

    def make_copy(self):
        cp = DotsGame.__new__(DotsGame)

        cp.player_count = self.player_count
        cp.player_turn = self.player_turn
        cp.grid_size = self.grid_size

        cp.player_letters = self.player_letters[:]  # list copy
        cp.score = self.score.copy()  # dict copy
        cp.grid = [row[:] for row in self.grid]  # 2D list copy
        cp.captured_areas = deepcopy(self.captured_areas)
        cp.last_move = self.last_move  # tuple/None, immutable

        cp.legal_moves = self.legal_moves.copy()
        cp.player_moves = {k: v.copy() for k, v in self.player_moves.items()}
        return cp