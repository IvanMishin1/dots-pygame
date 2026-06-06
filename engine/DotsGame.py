from copy import deepcopy


from engine.logic import *

class DotsGame:
    def __init__(self, grid_size):
        # Game config
        self.blue_turn = True
        self.GRID_SIZE = grid_size

        # Game state
        self.score = {'B': 0, 'R': 0}
        self.grid = [[' ' for _ in range(self.GRID_SIZE + 1)] for _ in range(self.GRID_SIZE + 1)]
        self.captured = []
        self.last_move = None

    def get_legal_moves(self):
        legal_moves = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == " ":
                    legal_moves.append((x,y))
        return legal_moves

    def get_captured(self):
        return deepcopy(self.captured)

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

        if self.blue_turn:
            self.grid[y][x] = "B"
            self.last_move = (x, y, "B")
            check_borders("B", "R", self)
            check_borders("R", "B", self)
        else:
            self.grid[y][x] = "R"
            self.last_move = (x, y, "R")
            check_borders("R", "B", self)
            check_borders("B", "R", self)
        self.blue_turn = not self.blue_turn
        return self
