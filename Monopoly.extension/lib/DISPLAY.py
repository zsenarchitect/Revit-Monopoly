# this handle the revit display.
# include setting color in view, change filter.
from Autodesk.Revit import DB
try:
    doc = __revit__.ActiveUIDocument.Document
except:
    pass
import ERROR_HANDLE

#@ERROR_HANDLE.try_catch_error--------------> do not add wrapper, otherwise the event register will fail.
def colorize_players_by_team(players):
    """change the display color of the player to match the team color
    
    Args:
        player (Player): the player, can be player, NPC, team
      
    """
    t = DB.Transaction(doc, 'colorize_player_by_team')
    t.Start()
    for player in players:
        material = player.team.team_material
        player.revit_object.LookupParameter('accent_color').Set(material.Id)
    t.Commit()
    pass

# @ERROR_HANDLE.try_catch_error
def colorize_asset_by_agent(asset, agent):
    """change the display color of the asset to match the agent team color
    
    Args:
        asset (Asset): the asset, can be property.
        agent (Agent): the agent, can be player, NPC, team
    """
    t = DB.Transaction(doc, 'colorize_player_by_agent')
    t.Start()
    material = agent.team.team_material
    asset.revit_object.LookupParameter('accent_color').Set(material.Id)
    t.Commit()
    pass

def show_element(element):
    """show the element in revit
    
    Args:
        element (Asset | Agent | DB.Element): the element to be shown
    """
    pass

def hide_element(element):
    """hide the element in revit
    
    Args:
        element (Asset | Agent | DB.Element): the element to be hidden
    """
    pass