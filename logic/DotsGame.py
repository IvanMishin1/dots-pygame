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

    def get_legal_moves(self):
        legal_moves = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == " ":
                    legal_moves.append((x,y))
        return legal_moves

    def get_captured(self):
        return deepcopy(self.captured_areas)

    def is_legal_move(self,x,y):
        if not (0 <= x <= len(self.grid) and 0 <= y <= len(self.grid)):
            return False
        if not self.grid[y][x] == " ":
            return False
        return True

    def make_move(self, x, y):
        if not self.is_legal_move(x,y):
            print("Illegal Move", x,y)
            return self

        self.grid[y][x] = self.player_letters[self.player_turn]
        self.last_move = (x, y, self.player_letters[self.player_turn])

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

    def get_player_dots(self, player):
        points = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == player:
                    points.append((x,y))
        return points