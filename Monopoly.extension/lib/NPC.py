# pylint: disable-next=global-statement
from PLAYER import Player





class NPC(Player):
    """inherate from the player object to handle action. But there will be no team or money"""
    def __init__(self, character):
        name = character
        team = "NPC"
        initial_money = 0
       
        is_NPC = True # pylint: disable=C0103 # disable snake naming style
        super().__init__(name, team, character, initial_money, is_NPC)