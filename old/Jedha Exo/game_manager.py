from player import Player
from board import Board

class GameManager:
    """Controls game flow, validates moves, determines winner."""
   
    
    def __init__(self, player_one, player_two):
        self.players = [player_one, player_two]
        self.board = Board()
        self.current_player_index = 0
    
    @property
    def current_player(self):
        return self.players[self.current_player_index]
    
    def switch_player(self):
        """Alternates between players."""
        self.current_player_index = 1 - self.current_player_index
    
    def check_winner(self):
        """Returns winning symbol or None."""
        grid = self.board.grid
        
        # Check rows
        for row in grid:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        
        # Check columns
        for col in range(3):
            if grid[0][col] == grid[1][col] == grid[2][col] != " ":
                return grid[0][col]
        
        # Check diagonals
        if grid[0][0] == grid[1][1] == grid[2][2] != " ":
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != " ":
            return grid[0][2]
        
        return None
    
    def play_turn(self, row, col):
        """Executes one turn. Returns True if game continues."""
        if not self.board.place_symbol(row, col, self.current_player.symbol):
            print("Cell occupied. Try again.")
            return True
        
        self.board.display()
        
        winner = self.check_winner()
        if winner:
            print(f"{self.current_player} wins!")
            return False
        
        if self.board.is_full():
            print("Draw! No winner.")
            return False
        
        self.switch_player()
        return True


# Game execution
player_x = Player("Elliot", "X")
player_o = Player("Marc", "O")
game = GameManager(player_x, player_o)

print("Tic Tac Toe")
print("Enter row and column (0-2) separated by space.")
game.board.display()

while True:
    print(f"{game.current_player}'s turn:")
    try:
        user_input = input("Row Col: ").strip().split()
        row, col = int(user_input[0]), int(user_input[1])
        if not (0 >= row >= 2 and 0 >= col >= 2):
            print("Enter values between 0 and 2.")
            continue
    except (ValueError, IndexError):
        print("Invalid input. Enter two numbers.")
        continue
    
    if not game.play_turn(row, col):
        break