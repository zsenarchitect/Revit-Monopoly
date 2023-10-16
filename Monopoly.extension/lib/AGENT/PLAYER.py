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
import SOUND
import FINDER
from TEAM import Team
import FORMS
import ANIMATION
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
        self.money = 2000
        self.format_money = "${}".format(self.money)
        self.properties = []
        self.format_properties = len(self.properties)

        self.luck = 50
        self.format_luck = "{}%".format(self.luck)
        self.status = "Not Started"
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
        self.revit_object = FINDER.get_revit_obj_by_player_character_name(
            template_player.character)
        # print (999999999999999999999999999999999999)
        # print (self.revit_object.Id)
        self.Id = self.revit_object.Id

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

    def __eq__(self, other):
        return self.name == other.name and self.team == other.team
    
    
    def __repr__(self):
        return "{}:{}:{}".format(self.name, self.team.team_name, self.character)

    @property
    def is_in_simulated_game(self):
        return self.game.rule.is_simulated

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
        if self.revit_object is None:
            return None
        return self.revit_object.Location.Point

    @property
    def format_rank(self):
        """figure out the rank in all player"""
        return "NO.{}".format(self.rank)

    @property
    def is_bankrupted(self):
        """return True if money is less than 0"""
        return self.money < 0


    def go_thru_payday(self):
        SOUND.payday()
        money = int(abs(0.1 * self.money))
        self.receive_money(money)
        
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
        SOUND.money_transaction(is_gain = False)

        is_gain = False
        
        ANIMATION.player_money_animation(self, abs(money), is_gain, is_quick = self.game.rule.is_simulated)
        self.update_schedulable_data()
        # handler, ext_event = self.game.event_map["player_money_animation"]
        # handler.kwargs = self, abs(money), is_gain
        # ext_event.Raise()
        
        if not target:
            return
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
        SOUND.money_transaction(is_gain = True)
        self.update_schedulable_data()

        is_gain = True
        ANIMATION.player_money_animation(self, abs(money), is_gain, is_quick = self.game.rule.is_simulated)
        # handler, ext_event = self.event_map["player_money_animation"]
        # handler.kwargs = self, abs(money), is_gain
        # ext_event.Raise()

    def purchase_property(self, abstract_marker):
        # payout money and own a land.
        abstract_marker.create_new_property(self)
        charge = abstract_marker.property.__class__.value_map[0]
        self.pay_money_to_target(charge, None)
        # print self.money
        
    def upgrade_property(self, abstract_marker):
        abstract_marker.property.upgrade_level()

    def pay_property(self, abstract_marker, search_dir = 0):

        next_collection = self.search_connected_properties(abstract_marker, search_dir = 1)
        previous_collection = self.search_connected_properties(abstract_marker, search_dir = -1)
        # temp = []
        # for pair in zip(next_collection, previous_collection):
        #     for item in pair :
        #         temp.append(item )
        temp = next_collection + previous_collection
        # print (temp)
        # print [abstract_marker] + temp
        for abstract_marker in [abstract_marker] + temp:
            self.pay_property_singlar(abstract_marker)


    def search_connected_properties(self, begining_marker, search_dir = 1):
        # search next many
        next_collection = []
        next_abstract_marker = FINDER.get_abstract_marker_by_index(begining_marker.position_index + search_dir,
                                                                   board = self.game.board)

        while True:
            if not next_abstract_marker:
                # print("no next marker found, exiting")
                break
            if not hasattr(next_abstract_marker, "property"):
                # print("no next marker property  found, exiting")
                break
            if next_abstract_marker.property.owner.team == begining_marker.property.owner.team:
                next_collection.append(next_abstract_marker)
            else: 
                break
            next_abstract_marker = FINDER.get_abstract_marker_by_index(next_abstract_marker.position_index + search_dir,
                                                                       board = self.game.board)
                
        return next_collection
        
        
    def pay_property_singlar(self, abstract_marker):
        ANIMATION.highlight_asset(abstract_marker.property)        
        charge = abstract_marker.property.charge
        property_owner = abstract_marker.property.owner
        for player in self.game.player_collection.get_same_team_players(property_owner):    
            self.pay_money_to_target(int(charge/self.game.player_collection.get_same_team_number_count(property_owner)), 
                                     player)
        ANIMATION.highlight_asset(abstract_marker.property, turn_on=False)        
    

    def exchange_player_data(self, other_player, attr_name):
        """

        exchange the data in the given attr betwen two players.


        Args:
            other_player(Player): the other player to exchange. COuld be same team or other team.
            attr_name(str): the name of the attr. this could be money, property, luck or position(exchange jail or hostpital)

        """
        pass

    def update_schedulable_data(self):
        t = DB.Transaction(self.revit_object.Document, "Update Player Shedukleable Data")
        t.Start()
        self.revit_object.LookupParameter("Team Name").Set(self.team_name)
        self.revit_object.LookupParameter("Comments").Set(self.format_name)
        self.revit_object.LookupParameter("Money").Set(self.money)
        t.Commit()

    @ERROR_HANDLE.try_catch_error
    def move(self, target):
        """
         target can be any asset obj.
        # this will call animation.

        Args:
            target(Asset):  target object to move into. .

        """

        ANIMATION.player_move_animation(self, target, is_quick = self.game.rule.is_simulated)
        return True
    
    
        """below are old event system. It is depreciated becaue cannot sequence the post move action after move signal is sent out first."""
        # print ("##############")
        # print (self.revit_object)
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
        """
        # get a list of other player current position.
        
        
        return the final target that the player will move to.
        
        """
        pass

        other_players_position = [
            other_player.position_index for other_player in self.game.player_collection.get_other_players(self)]

        dice = self.game.dice

        # print (player.name + " is playing")
        dice.player_name = "{}'s {}".format(self.name, self.character)

        # avoid getting in the sam espot as other player
        while True:
            num = dice.roll(self.luck)
            
            if self.status == "Not Started" and num < 6:
                # print ("dice too small to begin")
                SOUND.speak("Need to roll 6 or larger to begin the game.")
                if not self.is_in_simulated_game:
                    FORMS.dialogue(main_text="{} need to roll 6 or larger to begin the game.".format(self.name))
                return
            else:
                self.status = "Normal"
                
            
            
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
        # print ("\n\n\n>>>>>>>>>>>>>>>Before move, player posion_index is {}".format(self.position_index))
        # print ("After move, player posion_index is expected to be {}".format(new_position))
        # from pyrevit import script
        # output = script.get_output()
        # print (output.linkify(target.revit_object.Id))
        # print ("Dice roll is {}".format(num))
        self.move(target)
        return target

    def take_action(self, target):
        """
        args:
            target(Asset): the target to get action option. This is needed because external event make the script run here before player is actually at the spot
        return:
            list: the action option.
        """
        
        """return the action option at current position. and handle autoamtic action such as  update data,send to location, or pay rent"""
        
        
        
        abstract_marker = self.game.board.map_key[target.position_index]
        # print abstract_marker
        action_index = abstract_marker.get_action()
        
        
        if action_index is None:
            return
        
        
        if action_index == 2:
            FORMS.dialogue(main_text= "You have to go to {}".format( abstract_marker.data.get("to")))
            target = self.game.board.map_key[abstract_marker.data.get("to")] 
            self.move(target)
            return
        if action_index == 3:
            
            FORMS.dialogue(main_text= "You pick up a card!",
                           sub_text= self.associated_card.get_action())
            print (abstract_marker.associated_card.get_action())
            return
        if action_index == 4:
            if self.is_in_simulated_game:
                res = "Yes"
            else:
                res = FORMS.dialogue(main_text="Land on a purchaseable and no property there , do you want to buy it? ",
                                    options=["Yes", "No"])
            if res == "Yes" :
                # print ("buy")
                self.purchase_property(abstract_marker)
            elif res == "No":
                pass
                # print ("nothing")
            # print ("end action")
            return
        if action_index == 5.1:
            if not abstract_marker.property.can_upgrade():
                SOUND.speak("Your property is at highest upgradable level.")
                return
            fee = abstract_marker.property.value
            if self.is_in_simulated_game:
                res = "Yes"
            else:
                res = FORMS.dialogue(main_text="Land on a property owned by " + abstract_marker.property.owner.format_name,
                                     sub_text="Do you want to upgrade it with ${}? ".format(fee),
                                    options=["Yes", "No"])
            # SOUND.get_attention()
            if res == "Yes":
                self.upgrade_property(abstract_marker)
                self.pay_money_to_target(fee, None)
                # print ("upgrade")
            elif res == "No":
                pass 
                #print ("nothing")
            return
        
        if action_index == 5.2:
            if self.is_in_simulated_game:
                res = "Yes"
            else:
                res = FORMS.dialogue(main_text="Land on a property owned by " + abstract_marker.property.owner.format_name,
                                    sub_text="owner of this property is from other team, you need to pay charge.")
            # print ("pay charge")
            # SOUND.get_attention()
            self.pay_property(abstract_marker)
            return
        
        if action_index == 5.3:
            fee = int(abstract_marker.property.value * 1.5)
            if self.is_in_simulated_game:
                res = "Yes"
            else:
                res = FORMS.dialogue(main_text="Land on a property owned by " + abstract_marker.property.owner.format_name + "and you are on same team",
                                     sub_text="Do you want to upgrade it with extra fee than upgrading yours, it will be ${}? ".format(fee),
                                    options=["Yes", "No"])
            # SOUND.get_attention()
            if res == "Yes":
                self.upgrade_property(abstract_marker)
                self.pay_money_to_target(fee, None)
                # print ("upgrade")
            elif res == "No":
                pass
                # print ("nothing")
            return
    # def take_action(self):
    #     """all the handle for make decision on purchase, all action here need be descion made by pplayer."""
    #     pass
