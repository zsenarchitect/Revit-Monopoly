# this handle all the game logic.
from Autodesk.Revit import DB
from ASSET.DICE import Dice
import SOUND
import NOTIFICATION
import FORMS
from PLAYER_COLLECTION import PlayerCollection
import System
doc = __revit__.ActiveUIDocument.Document


class Game:
    def __init__(self, players, board, rule, event_map):
        """setup game

        Args:
        players(list of Player): list of players.
        board(Board): board object
        rule(Rule): rules of the game, such as how long play, winning money, win by team or by player
        """
        self.players = players

        self.teams = []
        for player in self.players:
            if player.team not in self.teams:
                self.teams.append(player.team)

            # add board data here to each player so can access key may
            #player.board = board
            player.game = self

        self.player_collection = PlayerCollection(self.players)

        self.board = board
        for asset in self.board.map_key.values():
            asset.game = self
        self.rule = rule
        self.event_map = event_map

        self.round = 1
        self.current_player_index = 0
        self.dice = Dice()
        self.update_all_player_color()
        self.update_all_player_schedule_data()
        
        all_views = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
        for view in all_views:
            if view.Name == "$Camera_Main":
                self.main_view = view
                break


        # change camera to view XX
        self.dice.last_roll = -1

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def update_all_player_schedule_data(self):
        return
        handler, ext_event = self.event_map["update_schedulable_data"]
        for player in self.players:
            handler.kwargs = player,
            ext_event.Raise()

    def update_all_player_color(self):
        handler, ext_event = self.event_map["colorize_players_by_team"]
        handler.kwargs = self.players,
        ext_event.Raise()

    def play(self):
        __revit__.ActiveUIDocument.ActiveView = self.main_view
        if not self.is_game_over:
            
            self.update_round()

        return self.post_game_summary()

    @property
    def is_game_over(self):
        """
        :return: True if the game is over
        """
        if self.round > self.rule.max_game_round:
            SOUND.game_over()
            return True
        for player in self.players:
            if player.money > self.rule.max_money:
                SOUND.game_over()

                return True
        return False

    def update_round(self):

        self.update_player()
        self.update_NPC()
        self.update_UI()

        self.round += 1
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)
        
        # from pyrevit import forms
        # forms.toast("player index  = {}".format(self.current_player_index))

    def update_player(self):
        if self.current_player.remaining_hold > 0:
            
            self.current_player.update_holding()
            
            return
        
        elif self.current_player.remaining_hold == 0 and self.current_player.status != "Normal":
            
            if self.current_player.status != "Not Started":
                
                self.current_player.clear_holding()
                return
        
        

        self.current_player.game = self
        target = self.current_player.change_location()
        if not target:
            return
        self.current_player.take_action(target)
        
        self.player_collection.update_player_info(self.current_player)

  

    def update_NPC(self):
        """iterate through all npc action"""
        pass

    def update_UI(self):
        """update the WPF UI"""
        pass

    def post_game_summary(self):
        return "Last Player Index:{}, Player Name:{}\nRecent Dice:{}".format(self.current_player_index,
                                                                             self.players[self.current_player_index].name,
                                                                             self.dice.last_roll)


def master_game_play(game, UI_window):
    game.rule.is_simulated = UI_window.checkbox_is_simulated.IsChecked
    
    factor = 5 if UI_window.checkbox_full_auto.IsChecked else 1
    simulated_round = len(game.players) * factor if game.rule.is_simulated else len(game.players)
    for i in range(simulated_round):
        game.play()
        
    
def reset_board():
    
    import FINDER
    all_abstract_markers = [x for x in FINDER.get_all_generic_models() if hasattr(x, "Symbol") and x.Symbol.Family.Name == "AbstractMarker"]
    
    for marker in all_abstract_markers:
        marker.LookupParameter("show_house_desire").Set(0)
        marker.LookupParameter("level").Set(0)
        
        if marker.LookupParameter("show_card_desire").AsInteger() == 1 and marker.LookupParameter("can_purchase").AsInteger() == 0:
            marker.LookupParameter("Comments").Set(r'{"action":"card"}')
        
        
    highlighter_symbol = FINDER.get_revit_obj_by_type_name("Highlighter")
    
    highlighter_symbol.Document.ActiveView.HideElements (System.Collections.Generic.List[DB.ElementId]([highlighter_symbol.Id]))
        
    all_players = [x for x in  FINDER.get_all_generic_models() if hasattr(x, "Symbol") and x.Symbol.FamilyName == "PlayerModel"]
    for player in all_players:
        
        initial_pt = player.Location.Point
        final_pt = FINDER.get_revit_obj_by_index(-1).Location.Point
        vec = final_pt - initial_pt
        translation = DB.Transform.CreateTranslation(vec)
        DB.AdaptiveComponentInstanceUtils.MoveAdaptiveComponentInstance (player , translation, True)
        
        
        player.LookupParameter("Team Name").Set("Wait...")
        player.LookupParameter("Comments").Set("Wait...")
        player.LookupParameter("Money").Set(0)
        
 