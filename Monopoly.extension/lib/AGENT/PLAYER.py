"""player will have those attr.

name
is_NPC: for special charqacter.
team
money
proprty list[property objects]
luck

weapon
speed
direction: for which way to travel
orientation: for keep player facing the direction when traveling.
position(index on game board)
orientation
log



debate: store all those info in revit obj? or store in python?
I think it is more flexible to update game if store atr in python.
    """
import FINDER


class Player(object):
    """handle all player object, this has a child class called NPC"""

    def __init__(self, name, team_obj = None, character= None):
        self.name = name
        self.team = team_obj  # Team A, Team B or Solo

        # this is the name of the character: Cat, Hat, Bat, etc..
        self.character = character
        self.revit_obj = FINDER.get_character_object(character)

        self.money = 1000
        self.properties = []
        self.is_NPC = False  # pylint: disable=C0103 # disable snake naming style
        self.luck = 50

        self.position_index = -1  # -1 means have not start.
        self.velocity = 1  # this could be +4 or -3 to record speed and drecition on track

        self.remaining_hold = 0
        self.status = "normal"
        # jail: no money in/out, can use money to get out early, display as grey
        # hospital: can receive money, must pay fee per round.
        # kidnapped: no money in/out, can happen anywhere.
        # bankrupted: out of game. Property free to take.

    @property
    def orientation(self):
        return DB.XYZ(0, 0, 0)

    @property
    def location(self):
        marker = FINDER.get_marker(self.position_index)
        return marker.location

    @property
    def rank(self):
        # figure out the rank in all player
        return 1

    @property
    def is_bankrupted(self):
        # return True if money is 0. and properties did not sell.
        pass

    def pay_money_to_target(self, money, target):
        # target can be other players or building locations such as hospital
        # update moeny
        # also need to call animation.

        pass

    def receive_money(self, money):
        # update money
        pass

    def purchase_property(self, property):
        # payout money and own a land.
        pass


    def exchange_player_data(self, other_player, attr_name):
        # exchange the data in the given attr betwen two players.
        # this could be money, property, luck or position(exchange jail or hostpital)
        pass


    def move(self, target):
        # target can be any asset obj.
        # this will call animation.
        pass

    def change_team(self, new_team):
        # change the team of the player
        pass