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




import FINDER
from TEAM import Team
from ANIMATION import player_money_animation, player_move_animation
import ERROR_HANDLE
from EVENT_HANDLE import SimpleEventHandler

class TemplatePlayer(object):
    """this classe is only used to help fill the pre-game data form."""

    @ERROR_HANDLE.try_catch_error
    def __init__(self, name, team, character):

        self.format_name = name
        self.team_name = team.team_name
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
    def __init__(self, team, template_player):
        """This is the constructor method.
        
        Args:
            name(str): the name of player.
            team(Team): the team_obj. Not the name of the team.
            character(str): the name of the character such as Cat, Hat, Bat. This is for FINDER to find the family in revit.
        """
        self.name = template_player.format_name
        self.team = team



        

        # this is the name of the character: Cat, Hat, Bat, etc..
        self.character = template_player.character
        self.revit_obj = FINDER.get_revit_obj_by_player_character_name(template_player.character)

        self.money = template_player.money
        self.properties = template_player.properties
        self.is_NPC = False  # pylint: disable=C0103 # disable snake naming style
        self.luck = template_player.luck

        self.position_index = -1  # -1 means have not start.
        self.velocity = 1  # this could be +4 or -3 to record speed and drecition on track

        self.remaining_hold = 0
        self.status = template_player.status
        self.rank = template_player.rank

        # jail: no money in/out, can use money to get out early, display as grey
        # hospital: can receive money, must pay fee per round.
        # kidnapped: no money in/out, can happen anywhere.
        # bankrupted: out of game. Property free to take.


        func_list = [player_money_animation, player_move_animation]
        self.register_event_handler(func_list)


    
    @ERROR_HANDLE.try_catch_error
    def register_event_handler(self, func_list):
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
            setattr(self, "event_handler_{}".format(func.__name__), SimpleEventHandler(func))
            handler = getattr(self, "event_handler_{}".format(func.__name__))

            # ext_event_attr = getattr(self, "ext_event_{}".format(func.__name__))
            # ext_event_attr = ExternalEvent.Create(handler)
            # continue
            setattr(self, "ext_event_{}".format(func.__name__), ExternalEvent.Create(handler))



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
        self.event_handler_player_money_animation.kwargs = self, abs(money), is_gain
        self.ext_event_player_money_animation.Raise()

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
        self.event_handler_player_money_animation.kwargs = self, abs(money), is_gain
        self.ext_event_player_money_animation.Raise()

        
        

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


    def move(self, target):
        """
         target can be any asset obj.
        # this will call animation.

        Args:
            target(Asset object): the target to move.
        
        """
        pass

    def change_team(self, new_team):
        """change the team of player.
        
        Args:
            new_team(Team): the new team to change to.
        
        """
        self.team = new_team