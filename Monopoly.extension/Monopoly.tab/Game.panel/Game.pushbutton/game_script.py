#!/usr/bin/python
# -*- coding: utf-8 -*-


__context__ = "zero-doc"
__doc__ = "main game window."
__title__ = "Play\nMonopoly"


# import System

from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# from System import EventHandler, Uri


from Autodesk.Revit.Exceptions import InvalidOperationException
from pyrevit.forms import WPFWindow
from pyrevit import forms
from pyrevit import script


from Autodesk.Revit import DB  # fastest DB
from Autodesk.Revit import UI
try:
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
except:
    print
    "nnned to allow open revit doc when zero doc."

__persistentengine__ = True

import ERROR_HANDLE
from AGENT.PLAYER import Player, TemplatePlayer
from AGENT.TEAM import Team
from LOGIC import Game
from ASSET.BOARD import Board
from RULE import Rule

import SOUND





# A simple WPF form used to call the ExternalEvent
class game_ModelessForm(WPFWindow):

    @ERROR_HANDLE.try_catch_error
    def __init__(self):


        


        xaml_file_name = "game_UI_ModelessForm.xaml"
        WPFWindow.__init__(self, xaml_file_name)

        self.title_text.Text = "Monopoly"
        self.sub_text.Text = "Classic board game, in Revit!\nYou can edit Player Name and Team Name below.\nUse 'Solo' to be independent."
        self.Title = self.title_text.Text
        self.set_image_source(self.logo_img, "icon.png")
        self.set_image_source(self.main_logo, "title.png")
 
        self.init_data_grid()

        self.Show()

        self.register_event_handler()
        SOUND.speak("Welcome to the world of Monopoly, in Revit?")



    @ERROR_HANDLE.try_catch_error
    def register_event_handler(self, func_list = None):
        """register the event handler to the player.
        Args:

            example: func_list = [player_money_animation, player_move_animation]

        """

        """
        Note to self:
        after many tri, cannot create extra event handler at this step.
        Next idea is to create a all the ext event in UI init stage as usual. Then pass the collection to Players or Asset when make instance at game beginging.
        
        
        """
        if func_list is None:
            from ANIMATION import player_money_animation, player_move_animation
            func_list = [player_money_animation, player_move_animation]
            
        
        from Autodesk.Revit.UI import ExternalEvent
        from EVENT_HANDLE import SimpleEventHandler
        


        self.event_map = dict()

        for func in func_list:
            setattr(self, "event_handler_{}".format(func.__name__), SimpleEventHandler(func))
            handler = getattr(self, "event_handler_{}".format(func.__name__))
            setattr(self, "ext_event_{}".format(func.__name__), ExternalEvent.Create(handler))
            ext_event = getattr(self, "ext_event_{}".format(func.__name__))

            self.event_map[func.__name__] = (handler, ext_event)

    @ERROR_HANDLE.try_catch_error
    def init_data_grid(self):
        # this will be replaced by idenpendent dropdown menu Each cell can edit the name, team.
        # the team can be Tean A or B, or indepedent.

        names = ["Tom", "Jerry", "Timon", "Pumbaa"]
 
        teams = [Team(team_name="Solo")] * len(names)
        sample_characters = [ "Boot", "Cheese", "Duck","Hat"]
        characters = sample_characters[0: len(names)]
        template_players = [TemplatePlayer(name, team, character)
                            for name, team, character in zip(names, teams, characters)]

        
        self.main_data_grid.ItemsSource = template_players

    @ERROR_HANDLE.try_catch_error
    def preview_selection_changed(self, sender, args):
        return
        obj = self.main_data_grid.SelectedItem
        if not obj:
            self.textblock_display_detail.Text = ""
            return

    @ERROR_HANDLE.try_catch_error
    def game_start_click(self, sender, args):
        if not hasattr(self, "game"):
            # validate the player info, make sure all field has valid input
            team_dict = dict()
            self.real_players = []
            for template_player_info in self.main_data_grid.ItemsSource:
                if template_player_info.team_name not in team_dict:
                    new_team = Team(team_name=template_player_info.team_name)
                    team_dict[template_player_info.team_name] = new_team

                else: 
                    new_team = team_dict[template_player_info.team_name]
                self.real_players.append(Player(new_team, template_player_info, self.event_map))
                    
            self.main_data_grid.ItemsSource = self.real_players
            #self.textblock_display_detail.Text = str(self.real_players)
            #print (self.event_map)


            # lock the file, saveas the revit file so not losing original stage.
            players = self.real_players
            board = Board()
            rule = Rule(max_game_round=40, max_money=1200)
            self.game = Game( players, board, rule)

            self.bt_start_game.Content = "Next Player"
            
            SOUND.speak("Game Start! Let's make some money rain!")

        # once started, the data grid is display only, cannot edit again.
        # all game play handle in there.
        result = self.game.play()


        self.textblock_display_detail.Text = str(result)


        


    @ERROR_HANDLE.try_catch_error
    def close_Click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        self.Close()
        #print (str(self.real_players))

    def mouse_down_main_panel(self, sender, args):
        # print "mouse down"
        sender.DragMove()


################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    # Let's launch our beautiful and useful form !

    modeless_form = game_ModelessForm()
