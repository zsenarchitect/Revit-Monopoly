# this handle all the game logic.


class Game:
    def __init__(self, players, board, rule):
        """setup game

        Args:
        players(list of Player): list of players.
        board(Board): board object
        rule(Rule): rules of the game, such as how long play, winning money, win by team or by player
        """
        self.players = players

        self.teams = []
        for player in self.players:
            if player.team not in self.teams:
                self.teams.append(player.team)
        self.board = board
        self.rule = rule
        self.round = 1
        pass

    def play(self):
        while not self.is_game_over:
            self.update_round()

        self.post_game_summary()

    @property
    def is_game_over(self):
        """
        :return: True if the game is over
        """
        pass

    def update_round(self):

        self.update_players()
        self.update_NPC()
        self.update_UI()

    def update_players(self):
        """iterate through  all players action"""
        pass

    def update_NPC(self):
        """iterate through all npc action"""
        pass

    def update_UI(self):
        """update the WPF UI"""
        pass

    def post_game_summary(self):
        return "Game over, thank you for playing"
