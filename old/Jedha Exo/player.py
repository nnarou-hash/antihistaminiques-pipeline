class Player:
    """Represents a player with name and symbol."""
    
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
