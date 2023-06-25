# this handle all the game logic.


from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# from System import EventHandler, Uri


from Autodesk.Revit.Exceptions import InvalidOperationException
import traceback

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


class Game:
    def __init__(self, players, board, rule):
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
        self.board = board
        self.rule = rule
        self.round = 1


        self.register_event_handler()
        pass

    def register_event_handler(self):
        
        self.simple_event_handler = SimpleEventHandler(play)
        self.ext_event = ExternalEvent.Create(self.simple_event_handler)




    def play(self):
        while not self.is_game_over:
            self.update_round()

        return self.post_game_summary()

    @property
    def is_game_over(self):
        """
        :return: True if the game is over
        """
        pass

    def update_round(self):

        self.update_players()
        self.update_NPC()
        self.update_UI()

    def update_players(self):
        """iterate through  all players action"""
        pass

    def update_NPC(self):
        """iterate through all npc action"""
        pass

    def update_UI(self):
        """update the WPF UI"""
        pass

    def post_game_summary(self):
        return "Game over, thank you for playing"
