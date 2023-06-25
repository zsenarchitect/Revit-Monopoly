


class Rule:
    def __init__(self, max_game_length, max_money):
        """setupt game rule
        
        Args:
            max_game_length (int): if reach max game length the game has to stop
            max_money (int): max money, if team reach this money the game has to stop. Solo team return its owner as winnner
        
        """
        self.max_game_length = max_game_length
        self.max_money = max_money
        pass