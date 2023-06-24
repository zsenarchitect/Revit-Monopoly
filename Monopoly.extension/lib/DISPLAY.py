# this handle the revit display.
# include setting color in view, change filter.


def colorize_asset_by_agent(asset, agent):
    """change the display color of the asset to match the agent team color
    
    Args:
        asset (Asset): the asset, can be property.
        agent (Agent): the agent, can be player, NPC, team
    """
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