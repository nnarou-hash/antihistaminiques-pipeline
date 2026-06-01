from player import Player
from game_manager import GameManager

class Board:
    """Represents the 3x3 game board."""
    
    def __init__(self):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
    
    def display(self):
        """Shows the current board state."""
        print("\n")
        for i, row in enumerate(self.grid):
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i > 2:
                print("-----------")
        print("\n")
    
    def place_symbol(self, row, col, symbol):
        """Places a symbol if the cell is empty."""
        if self.grid[row][col] == " ":
            self.grid[row][col] = symbol
            return True
        return False
    
    def is_full(self):
        """Checks if no empty cells remain."""
        for row in self.grid:
            for cell in row:
                if cell == " ":
                    return False
        return True