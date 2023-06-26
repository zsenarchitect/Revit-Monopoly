# this handle all the game logic.

from ASSET.DICE import Dice
import SOUND

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

            # add board data here to each player so can access key may
            player.board = board
        self.board = board
        self.rule = rule
        self.round = 1
        self.current_player_index = 0
        self.dice = Dice()

        # change camera to view XX

        



    def play(self):
        if not self.is_game_over:
            self.update_round()

        return self.post_game_summary()

    @property
    def is_game_over(self):
        """
        :return: True if the game is over
        """
        if self.round > self.rule.max_game_round:
            SOUND.game_over()
            return True
        for player in self.players:
            if player.money >self.rule.max_money: 
                SOUND.game_over()
                
                return True
        return False

    def update_round(self):

        self.update_player()
        self.update_NPC()
        self.update_UI()

        self.round += 1
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def update_player(self):
        """iterate through  all players action"""

        player = self.players[self.current_player_index]

        # get a list of other player current position.
        other_players_position = [other_player.position_index for other_player in self.players if other_player != player]
           


        #print (player.name + " is playing")
        self.dice.player_name = player.name

        # avoid getting in the sam espot as other player
        while True:
            num = self.dice.roll(player.luck)
            new_position = player.position_index + num * player.velocity
            new_position = new_position % self.board.max_marker_index
            if new_position not in other_players_position:
                break
        
        """
        while True:
            current_position = player.position_index
            temp_next_position = (current_position + 1)% self.board.max_marker_index
            print (temp_next_position)
            target = self.board.map_key[temp_next_position]
            player.move(target)
            if player.position_index == new_position:
                break
        """
        target = self.board.map_key[new_position]
        player.move(target)

    def update_NPC(self):
        """iterate through all npc action"""
        pass

    def update_UI(self):
        """update the WPF UI"""
        pass

    def post_game_summary(self):
        return "Last Player Index:{}, Player Name:{}\nRecent Dice:{}\nNew Position:{}".format(self.current_player_index, self.players[self.current_player_index].name, self.dice.last_roll, self.players[self.current_player_index].position_index)
