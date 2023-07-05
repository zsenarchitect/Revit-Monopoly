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
from Autodesk.Revit import DB


import time

import FINDER
from TEAM import Team
from ANIMATION import player_money_animation, player_move_animation
import ERROR_HANDLE
from EVENT_HANDLE import SimpleEventHandler

from PLAYER_COLLECTION import PlayerCollection


class TemplatePlayer(object):
    """this classe is only used to help fill the pre-game data form."""

    @ERROR_HANDLE.try_catch_error
    def __init__(self, name, team_name, character):

        self.format_name = name
        self.team_name = team_name
        self.character = character
        self.money = 1000
        self.format_money = "${}".format(self.money)
        self.properties = []
        self.format_properties = len(self.properties)

        self.luck = 50
        self.format_luck = "{}%".format(self.luck)
        self.status = "Normal"
        self.rank = 1
        self.format_rank = "NO.{}".format(self.rank)


class Player(object):
    """handle all player object, this has a child class called NPC

    attrs: xxxxxxxxxxxxxxxxxxxxxxx
    """

    @ERROR_HANDLE.try_catch_error
    def __init__(self, team, template_player, event_map):
        """This is the constructor method.

        Args:
            name(str): the name of player.
            template_player(TemplatePlayer): the template_player object from the datagrid with user edit
            event_map(dict): dict of all the registered event, key = func_name, value = (handler, event)

        """
        self.event_map = event_map

        self.name = template_player.format_name
        self.team = team
        self.update_color()

        # this is the name of the character: Cat, Hat, Bat, etc..
        self.character = template_player.character
        self.revit_obj = FINDER.get_revit_obj_by_player_character_name(
            template_player.character)
        # print (999999999999999999999999999999999999)
        # print (self.revit_obj.Id)
        self.Id = self.revit_obj.Id

        self.money = template_player.money
        self.properties = template_player.properties
        self.is_NPC = False  # pylint: disable=C0103 # disable snake naming style
        self.luck = template_player.luck

        self.position_index = 0  # 0 means have not start.
        self.velocity = 1  # this could be +4 or -3 to record speed and drecition on track

        self.remaining_hold = 0
        self.status = template_player.status
        self.rank = template_player.rank

        # jail: no money in/out, can use money to get out early, display as grey
        # hospital: can receive money, must pay fee per round.
        # kidnapped: no money in/out, can happen anywhere.
        # bankrupted: out of game. Property free to take.

    @ERROR_HANDLE.try_catch_error
    def NOT_IN_USE_register_event_handler(self, func_list):
        """register the event handler to the player.
        Args:

            example: func_list = [player_money_animation, player_move_animation]

        """

        """
        Note to self:
        after many tri, cannot create extra event handler at this step.
        Next idea is to create a all the ext event in UI init stage as usual. Then pass the collection to Players or Asset when make instance at game beginging.
        
        
        """

        from Autodesk.Revit.UI import ExternalEvent

        self.simple_event_handler = SimpleEventHandler(player_money_animation)
        self.ext_event = ExternalEvent.Create(self.simple_event_handler)

        return

        for func in func_list:
            setattr(self, "event_handler_{}".format(
                func.__name__), SimpleEventHandler(func))
            handler = getattr(self, "event_handler_{}".format(func.__name__))

            # ext_event_attr = getattr(self, "ext_event_{}".format(func.__name__))
            # ext_event_attr = ExternalEvent.Create(handler)
            # continue
            setattr(self, "ext_event_{}".format(func.__name__),
                    ExternalEvent.Create(handler))

    def __repr__(self):
        return "{}:{}:{}".format(self.name, self.team.team_name, self.character)

    @property
    def format_name(self):
        return self.name

    @property
    def format_money(self):
        return "${}".format(self.money)

    @property
    def format_properties(self):
        return len(self.properties)

    @property
    def format_luck(self):
        return "{}%".format(self.luck)

    @property
    def team_name(self):
        return self.team.team_name

    def is_same_team(self, other_player):
        """check if the two players are in the same team.
        Args:
            other_player(Player): the other player to check.
        Returns:
            bool: True if they are in the same team or either one is in solo team
        """
        if self.team.is_solo or other_player.team.is_solo:
            return False
        return self.team == other_player.team

    @property
    def orientation(self):
        return DB.XYZ(0, 0, 0)

    @property
    def location(self):
        """this is the XYZ location"""
        """
        marker = FINDER.get_abstract_marker_by_index(self.position_index)
        if not marker:
            return None
        
        """
        if self.revit_obj is None:
            return None
        return self.revit_obj.Location.Point

    @property
    def format_rank(self):
        """figure out the rank in all player"""
        return "NO.{}".format(self.rank)

    @property
    def is_bankrupted(self):
        """return True if money is less than 0"""
        return self.money < 0

    @ERROR_HANDLE.try_catch_error
    def pay_money_to_target(self, money, target):
        """This is the constructor method.
        target can be other players or building locations such as hospital
        update moeny
        also need to call animation.

        Args:
            money(abs.int): the money to pay.
            target(Player or BuildingLocation object): the target to pay.
        """
        self.money -= abs(money)

        is_gain = False

        handler, ext_event = self.game.event_map["player_money_animation"]
        handler.kwargs = self, abs(money), is_gain
        ext_event.Raise()

        if isinstance(target, Player):
            target.receive_money(money)
        else:
            target.owner.receive_money(money)

    @ERROR_HANDLE.try_catch_error
    def receive_money(self, money):
        """ This is the constructor method.
        update money
        also need to call animation.

        Args:
            money(abs.int): the money to come in.
        """
        self.money += abs(money)

        is_gain = True
        handler, ext_event = self.event_map["player_money_animation"]
        handler.kwargs = self, abs(money), is_gain
        ext_event.Raise()

    def purchase_property(self, property):
        # payout money and own a land.
        pass

    def exchange_player_data(self, other_player, attr_name):
        """

        exchange the data in the given attr betwen two players.


        Args:
            other_player(Player): the other player to exchange. COuld be same team or other team.
            attr_name(str): the name of the attr. this could be money, property, luck or position(exchange jail or hostpital)

        """
        pass

    @ERROR_HANDLE.try_catch_error
    def move(self, target):
        """
         target can be any asset obj.
        # this will call animation.

        Args:
            target(Asset):  target object to move into. .

        """
        # print ("##############")
        # print (self.revit_obj)
        handler, ext_event = self.event_map["player_move_animation"]
        handler.kwargs = self, target
        ext_event.Raise()
        # self.position_index = target.position_index

        # for i in range(10):
        #     time.sleep(0.1)
        #     if handler.OUT:
        #         break

        return True

    @ERROR_HANDLE.try_catch_error
    def update_color(self):
        handler, ext_event = self.event_map["colorize_players_by_team"]
        handler.kwargs = [self],
        ext_event.Raise()

    @ERROR_HANDLE.try_catch_error
    def change_team(self, new_team):
        """change the team of player.

        Args:
            new_team(Team): the new team to change to.

        """
        self.team = new_team
        self.update_color()

    def change_location(self):
        # get a list of other player current position.

        other_players_position = [
            other_player.position_index for other_player in self.game.player_collection.get_other_players(self)]

        dice = self.game.dice

        # print (player.name + " is playing")
        dice.player_name = self.name

        # avoid getting in the sam espot as other player
        while True:
            num = dice.roll(self.luck)
            new_position = self.position_index + num * self.velocity
            new_position = new_position % (self.game.board.max_marker_index + 1)
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
        target = self.game.board.map_key[new_position]
        print ("\n\n\n>>>>>>>>>>>>>>>Before move, player posion_index is {}".format(self.position_index))
        print ("After move, player posion_index is expected to be {}".format(new_position))
        print ("Dice roll is {}".format(num))
        self.move(target)

    def get_action_option(self):
        """return the action option at current position. and handle autoamtic action such as  update data,send to location, or pay rent"""
        abstract_marker = self.game.board.map_key[self.position_index]
        print(abstract_marker.get_action())

    def take_action(self):
        """all the handle for make decision on purchase, all action here need be descion made by pplayer."""
        pass
