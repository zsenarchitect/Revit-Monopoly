
import random
from ASSET import Asset


class Card(Asset):
    contents = [{"title":"Go to Jail for being too sexy","action":"to", "value":-10},
                {"title":"get hit by a flying baseball","action":"to","value":-11},
                {"title":"kidnapped by UFO","action":"hold", "value":2},
                {"title":"spy reveal! Exchanging team", "action":"exchange", "value": "team"},
                {"title":"Theft of the year!Exchange money with richest player", "action":"exchange", "value":"richest_player"},
                {"title":"Invader! ", "action":"exchange",},
                {"title":"Thunder storm hit best building", "action":"demolish",},
                {"title":"rat found! building downgrade", "action":"downgrade"},
                {"title":"Free building upgrade for all your properties", "action":"upgrade", "value":"self all"},
                {"title":"bigest credit card! Force purchurse any building", "action":"force_buy"},
                {"title":"demolish the richest buikding in enermy team", "action":"demolish"},


                {"title":"Tax season! All other team player play 20% tax","action":"other_team_tax","value":0.2},
                {"title":"Winning lottery","action":"money","value":500},
                {"title":"Winning lottery","action":"money","value":500},
                {"title":"Winning lottery","action":"money","value":500},
                {"title":"Winning big lottery!","action":"money","value":2000},
                {"title":"Fined for missing tax season","action":"money","value":-1000},
                {"title":"Finding wallet on the trash can","action":"money","value":1000}]

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
