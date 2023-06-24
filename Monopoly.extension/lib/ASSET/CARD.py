

from ASSET import Asset


class Card(Asset):
    pass

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
