# this handle all the game logic.

from ASSET.DICE import Dice
import SOUND
from PLAYER_COLLECTION import PlayerCollection


class Game:
    def __init__(self, players, board, rule, event_map):
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
            #player.board = board
            player.game = self

        self.player_collection = PlayerCollection(self.players)

        self.board = board
        for asset in self.board.map_key.values():
            asset.game = self
        self.rule = rule
        self.event_map = event_map

        self.round = 1
        self.current_player_index = 0
        self.dice = Dice()
        self.update_all_player_color()

        # change camera to view XX

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def update_all_player_color(self):
        handler, ext_event = self.event_map["colorize_players_by_team"]
        handler.kwargs = self.players,
        ext_event.Raise()

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
            if player.money > self.rule.max_money:
                SOUND.game_over()

                return True
        return False

    def update_round(self):

        self.update_player()
        self.update_NPC()
        self.update_UI()

        self.round += 1
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)

    def update_player(self):
        if self.current_player.remaining_hold > 0:
            SOUND.speak(self.current_player.name + " has " +
                        str(self.current_player.remaining_hold) + " hold")
            return

        self.current_player.game = self
        target = self.current_player.change_location()
        self.current_player.get_action_option(target)
        self.current_player.take_action()
  

    def update_NPC(self):
        """iterate through all npc action"""
        pass

    def update_UI(self):
        """update the WPF UI"""
        pass

    def post_game_summary(self):
        return "Last Player Index:{}, Player Name:{}\nRecent Dice:{}".format(self.current_player_index,
                                                                             self.players[self.current_player_index].name,
                                                                             self.dice.last_roll)
