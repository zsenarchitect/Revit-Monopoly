class PlayerCollection:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, players = None):
        if players is not None:
            self.players = players

    # @classmethod
    # def update_players(cls, players):
    #     cls._instance.players = players

    @property
    def players(self):
        return PlayerCollection._instance.players

    
    def get_other_players(self, excluded_player):
        return [player for player in self.players if excluded_player.Id != player.Id]
    
    def get_same_team_players(self, my_player):
        return [player for player in self.players if player.team == my_player.team]
    
    
 
    def get_same_team_number_count(self, player):
        return len(self.get_same_team_players(player))