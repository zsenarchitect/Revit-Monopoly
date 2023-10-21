
import random
from ASSET import Asset


class Card(Asset):
    contents = [{"title":"Go to Jail for being too sexy","to":-10},
                {"title":"get hit by a flying baseball","to":-11},
                {"title":"kidnapped by UFO","hold":2},
                {"title":"spy reveal! Exchanging team", "exchange":"team"},
                {"title":"Theft of the year!Exchange money with richest player", "exchange":"richest_player"},
                {"title":"Invader! ", "exchange":"xxx"},
                {"title":"Thunder storm hit best building", "demolish":"xxx"},
                {"title":"rat found! building downgrade", "downgrade":"xxx"},
                {"title":"demolish the richest buikding in enermy team", "exchange":"xxx"},




                {"title":"Fined for missing tax season","money":-1000},
                {"title":"Finding wallet on the trash can","money":1000}]

    @classmethod
    def get_card(cls):
        return random.choice(cls.contents)
        

    @property
    def description(self):
        # return the description saved in self.revit_object.

        pass

    @property
    def money_change(self):
        # return the money change saved in self.revit_object.
        #  >0 to receive money for player
        # <0 to deduct money for player
        pass

    def send_money_to_team(self, player, team):
        # use self.money_change to figure out how much money
        pass

    def receive_money_from_team(self, player, team):
        # use self.money_change to figure out how much money
        pass

    def update_player_hold_cycle(self, player):
        # get the hold cycle saved in self.revit_object.
        # X means cannot move for X round.
        # the data is in player.remaining_hold
        pass

    def send_player_to_place(self, player):
        # send the involved player to place saved in self.revit_object.
        pass
