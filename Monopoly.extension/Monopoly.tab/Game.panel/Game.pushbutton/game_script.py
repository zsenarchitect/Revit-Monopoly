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


@ERROR_HANDLE.try_catch_error
def play(title):

    t = DB.Transaction(doc, title)
    t.Start()
    pass
    t.Commit()


# Create a subclass of IExternalEventHandler
class SimpleEventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
        self.kwargs = None
        self.OUT = None

    # Execute method run in Revit API environment.

    def Execute(self,  uiapp):
        try:
            try:
                # print "try to do event handler func"
                self.OUT = self.do_this(*self.kwargs)
            except:
                print("failed")
                print(traceback.format_exc())
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print("InvalidOperationException catched")

    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# A simple WPF form used to call the ExternalEvent
class game_ModelessForm(WPFWindow):

    def pre_actions(self):
        # if active doc is not "Monopoly Game Board" then open the game board fiel.

        self.simple_event_handler = SimpleEventHandler(play)
        self.ext_event = ExternalEvent.Create(self.simple_event_handler)

    @ERROR_HANDLE.try_catch_error
    def __init__(self):
        self.pre_actions()

        xaml_file_name = "game_UI_ModelessForm.xaml"
        WPFWindow.__init__(self, xaml_file_name)

        self.title_text.Text = "Monopoly"
        self.sub_text.Text = "Classic board game, in Revit!"
        self.Title = self.title_text.Text
        self.set_image_source(self.logo_img, "icon.png")
        self.init_data_grid()

        self.Show()

    @ERROR_HANDLE.try_catch_error
    def init_data_grid(self):
        # this will be replaced by idenpendent dropdown menu Each cell can edit the name, team.
        # the team can be Tean A or B, or indepedent.

        from AGENT.PLAYER import Player
        from AGENT.TEAM import Team

        names = ["Tom", "Jerry", "Timon", "Pumbaa"]
        teams = [Team(team_name="Solo")] * len(names)
        characters = ["Hat"] * len(names)
        self.players = [Player(name, team, character)
                        for name, team, character in zip(names, teams, characters)]
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
        # lock the file, saveas the revit file so not losing original stage.

        # validate the player info, make sure all field has valid input

        # once started, the data grid is display only, cannot edit again.

        # set game cycle as 1. Begin game loop.

        pass

    @ERROR_HANDLE.try_catch_error
    def main_loop(self):

        pass

        # loop thru all player action. Each call GAME_LOGIC.

        # increament the game cycle

        # update all UI window display

        # check if game is over by call is_game_over

    def is_game_over(self):
        # check if only one players/teams have positive asset.
        # call finish

        # check if manual kill the game
        # call finish

        # all seems ok, Then call main_loop again.

        pass

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
