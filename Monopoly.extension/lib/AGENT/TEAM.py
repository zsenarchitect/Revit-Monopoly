"""handle all team action, solo player are also a team."""
from Autodesk.Revit import DB

class Team(object):
    def __init__(self, team_name):
         """This is the constructor method.
        
        Args:
            team_name(str): the name of team.
            
        """
         self.team_name = team_name
         self.team_members = []
         self.team_color = DB.Color(100, 200, 200)

    @property
    def is_solo(self):
        return self.team_name == "Solo"
    

    def change_team_color(self, color):
        """Change the color of team.
        
        Args:
            color(DB.Color): a color object.
            
        """
        self.team_color = color

    def change_team_name(self, team_name):
        """Change the name of team, this is for the card that make other team name stupid.
        
        Args:
            team_name(str): the name of team.
            
        """
        self.team_name = team_name

    def add_member(self, player):
        """Add a player to the team.
        
        Args:
            player(Player): a player object.
            
        """
        self.team_members.append(player)

    def remove_member(self, player):
        """Remove a player from the team.
        
        Args:
            player(Player): a player object.
            
        """
        self.team_members.remove(player)
    
    def is_solo_team(self):
        # return True if team has only one member.
        pass

    def is_team_lost(self):
        # return True if all team members is bankrupted.
        pass

    def exchange_team_data(self, other_team):
        pass
