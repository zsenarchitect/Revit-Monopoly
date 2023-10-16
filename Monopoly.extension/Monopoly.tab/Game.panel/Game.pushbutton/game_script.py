#!/usr/bin/python
# -*- coding: utf-8 -*-


__context__ = "zero-doc"
__doc__ = "main game window."
__title__ = "Play\nMonopoly"


# import System

from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# from System import EventHandler, Uri

import System
from Autodesk.Revit.Exceptions import InvalidOperationException
from pyrevit.forms import WPFWindow
from pyrevit import forms
from pyrevit import script
import threading
import datetime
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
from LOGIC import Game, reset_board
from ASSET.BOARD import Board
from RULE import Rule

import SOUND

import pprint


# A simple WPF form used to call the ExternalEvent
class game_ModelessForm(WPFWindow):

    @ERROR_HANDLE.try_catch_error
    def __init__(self):

        xaml_file_name = "game_UI_ModelessForm.xaml"
        WPFWindow.__init__(self, xaml_file_name)

        self.title_text.Text = "Monopoly"
        self.sub_text.Text = "Classic board game, in Revit!\nYou can edit Player Name and Team Name below.\nPlayer inside same team name will be assigned same color."
        self.Title = self.title_text.Text
        self.set_image_source(self.logo_img, "coin.png")
        self.set_image_source(self.main_logo, "title.png")

        self.init_data_grid()

        self.Show()

        self.register_event_handler()
        SOUND.speak("Welcome to the world of Monopoly, in Revit!")

    @ERROR_HANDLE.try_catch_error
    def register_event_handler(self, func_list=None):
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
            from DISPLAY import colorize_players_by_team
            from LOGIC import master_game_play


            func_list = [player_money_animation,
                         player_move_animation,
                         colorize_players_by_team,
                         master_game_play]

        from Autodesk.Revit.UI import ExternalEvent
        from EVENT_HANDLE import SimpleEventHandler, ExternalEvent

        self.event_map = dict()

        for func in func_list:
            setattr(self, "event_handler_{}".format(
                func.__name__), SimpleEventHandler(func))
            handler = getattr(self, "event_handler_{}".format(func.__name__))
            setattr(self, "ext_event_{}".format(func.__name__),
                    ExternalEvent.Create(handler))
            ext_event = getattr(self, "ext_event_{}".format(func.__name__))

            self.event_map[func.__name__] = (handler, ext_event)

        # pprint.pprint (self.event_map)

        """note to self
        make sure to not asdd error catch wraper, otherwise the event map will not capture the name correctly."""

    @ERROR_HANDLE.try_catch_error
    def init_data_grid(self):
        # this will be replaced by idenpendent dropdown menu Each cell can edit the name, team.
        # the team can be Tean A or B, or indepedent.

        names = ["Tom", "Jerry", "Timon", "Pumbaa"]

        teams = ["Team A", "Team A", "Team B", "Team B"]
        sample_characters = ["Boot", "Cheese", "Duck", "Hat"]
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
        self.open_auto_clicker()
        
        if not hasattr(self, "game"):
            # validate the player info, make sure all field has valid input
            team_dict = dict()
            self.real_players = []
            for template_player_info in self.main_data_grid.ItemsSource:
                if template_player_info.team_name not in team_dict:
                    new_team = Team(team_name=template_player_info.team_name,
                                    team_index=len(team_dict)+1)
                    team_dict[template_player_info.team_name] = new_team

                else:
                    new_team = team_dict[template_player_info.team_name]
                
                real_player = Player(new_team,
                                    template_player_info,
                                    self.event_map)
                self.real_players.append(real_player)

                

            self.main_data_grid.ItemsSource = self.real_players
            # self.textblock_display_detail.Text = str(self.real_players)
            # print (self.event_map)

            # lock the file, saveas the revit file so not losing original stage.
            players = self.real_players
            board = Board()
            rule = Rule(max_game_round=800,
                        max_money=8000,
                        is_simulated = self.checkbox_is_simulated)
            event_map = self.event_map
            self.game = Game(players, board, rule, event_map)

            self.bt_start_game.Content = " Next Round "

            SOUND.speak("Game Start! Let's make some money rain!")

        # once started, the data grid is display only, cannot edit again.
        # all game play handle in there.
        # result = self.game.play()# this is the old method but cannot sequence the event with good timing.
        # so changing to new method that wrap the entire round in one event. All things inside should happen in good sequence.
        handler, ext_event = self.event_map["master_game_play"]
        
        handler.kwargs = self.game, self
        ext_event.Raise()
        result = handler.OUT

        self.textblock_display_detail.Text = str(result)
        self.main_data_grid.ItemsSource = self.game.players
        
        self.main_data_grid.Visibility = System.Windows.Visibility.Collapsed
        
        self.start_clocked_update_grid()
        
    def start_clocked_update_grid(self):
        
        self.timer_count = 100
        self.timer = threading.Timer(1, self.on_timed_event)
        self.timer.start()
        # print 123
        
        
        
    def on_timed_event(self):
        # begin main action
        self.main_data_grid.ItemsSource = []
        # end of main action
        print 000
        print("The Elapsed event was raised at", datetime.datetime.now())
        self.timer_count -= 1
        if self.timer_count > 0:

            self.timer = threading.Timer(1, self.on_timed_event)
            self.timer.start()
        else:
            print -999
            self.timer.cancel()
                
    @ERROR_HANDLE.try_catch_error
    def close_Click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        self.Close()
        # print (str(self.real_players))

    def ranking_click(self, sender, e):
        all_views = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
        for view in all_views:
            if view.Name == "Player Ranking":
                __revit__.ActiveUIDocument.ActiveView = view
                return
    def main_view_click(self, sender, e):
        all_views = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
        for view in all_views:
            if view.Name == "$Camera_Main":
                __revit__.ActiveUIDocument.ActiveView = view
                return

    def mouse_down_main_panel(self, sender, args):
        # print "mouse down"
        sender.DragMove()

    def open_auto_clicker(self):
        import os
        exe = r"L:\4b_Applied Computing\01_Revit\04_Tools\08_EA Extensions\Project Settings\Exe\GENERAL_AUTO_CLICKER\GENERAL_AUTO_CLICKER.exe"
        os.startfile(exe)

def main():
    if not doc.Title.StartsWith("Monopoly Game Board"):
        import open_main_file as OMF
        OMF.open()
        
        return
    
    t = DB.Transaction(doc, "Reset")
    t.Start()
    reset_board()
    t.Commit()
    
    # Let's launch our beautiful and useful form !
    
    modeless_form = game_ModelessForm()

################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    main()