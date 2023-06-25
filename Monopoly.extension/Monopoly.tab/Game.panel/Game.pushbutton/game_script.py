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
from AGENT.PLAYER import Player
from AGENT.TEAM import Team
from LOGIC import Game
from ASSET.BOARD import Board
from RULE import Rule







# A simple WPF form used to call the ExternalEvent
class game_ModelessForm(WPFWindow):

    @ERROR_HANDLE.try_catch_error
    def __init__(self):
        

        xaml_file_name = "game_UI_ModelessForm.xaml"
        WPFWindow.__init__(self, xaml_file_name)

        self.title_text.Text = "Monopoly"
        self.sub_text.Text = "Classic board game, in Revit!"
        self.Title = self.title_text.Text
        self.set_image_source(self.logo_img, "icon.png")
        print(123)
        self.init_data_grid()

        self.Show()

    @ERROR_HANDLE.try_catch_error
    def init_data_grid(self):
        # this will be replaced by idenpendent dropdown menu Each cell can edit the name, team.
        # the team can be Tean A or B, or indepedent.
        print("init_data_grid")

        names = ["Tom", "Jerry", "Timon", "Pumbaa"]
        print(names)
        teams = [Team(team_name="Solo")] * len(names)
        sample_characters = ["Hat", "Boot", "Cheese", "Toilet"]
        characters = sample_characters[0: len(names)]
        self.players = [Player(name, team, character)
                        for name, team, character in zip(names, teams, characters)]

        self.textblock_display_detail.Text = str(self.players)
        self.main_data_grid.ItemsSource = self.players

    @ERROR_HANDLE.try_catch_error
    def preview_selection_changed(self, sender, args):
        return
        obj = self.main_data_grid.SelectedItem
        if not obj:
            self.textblock_display_detail.Text = ""
            return

    @ERROR_HANDLE.try_catch_error
    def game_start_click(self, sender, args):
        # validate the player info, make sure all field has valid input


        # lock the file, saveas the revit file so not losing original stage.
        players = self.players
        board = Board()
        rule = Rule(max_game_round=30, max_money=3000)
        self.game = Game( players, board, rule)

        # once started, the data grid is display only, cannot edit again.
        # all game play handle in there.
        result = self.game.play()
        


        


    @ERROR_HANDLE.try_catch_error
    def close_Click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        self.Close()

    def mouse_down_main_panel(self, sender, args):
        # print "mouse down"
        sender.DragMove()


################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    # Let's launch our beautiful and useful form !

    modeless_form = game_ModelessForm()
