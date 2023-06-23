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
position(index on game board)
orientation
log

    
    """
import FINDER


class Player(object):
    """handle all player object, this has a child class called NPC"""
    def __init__(self, name, team, character, initial_money, is_NPC):
        self.name = name
        self.team = team  # Team A, Team B or Solo
        self.character = character  # this is the name of the character
        self.revit_obj = FINDER.get_character_object(character)

        self.money = initial_money
        self.propertie = []
        self.is_NPC = is_NPC# pylint: disable=C0103 # disable snake naming style
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
