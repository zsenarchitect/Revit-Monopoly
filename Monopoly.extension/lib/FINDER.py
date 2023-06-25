# use this to find revit obj by spec. or find game obj by spec
#import logging
# logging.basicConfig(level=logging.DEBUG,
#                     filename="FINDER_log.txt",
#                     filemode="w")
import ERROR_HANDLE


from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document



def get_all_generic_models():
    """get all the generic model
    
    Returns:
        list: all the generic model
    
    """
    all_gms = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
    return all_gms

@ERROR_HANDLE.try_catch_error
def get_revit_obj_by_player_character_name(character_name):
    """get the revit obj by the player character name
    
    Args:
        character_name (str): the name of the player character
    
    Returns:
        DB.Element: the revit obj
    
    """
    all_gms = get_all_generic_models()
    for gm in all_gms:
  
        if gm.Name == "PlayerModel":
            if gm.LookupParameter("Type Name").AsString() == character_name:
                return gm
        
    #logging.warning("no such revit obj found")
    
    return None

@ERROR_HANDLE.try_catch_error
def get_revit_obj_by_family_name(name):
    """get the revit obj by the name
    
    Args:
        name (str): the name of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    
    all_gms = get_all_generic_models()
    for gm in all_gms:
        #print (gm.Name)
        if gm.Name == name:
            return gm
        
    #logging.warning("no such revit obj found")
    
    return None


@ERROR_HANDLE.try_catch_error
def get_revit_obj_by_index(index):
    """get the revit obj by the position index, the index can be lookup in the board map
    
    Args:
        index (int): the index of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    pass



@ERROR_HANDLE.try_catch_error
def get_abstract_marker_by_index(index):
    """get the abstract marker by the position index, the index can be lookup in the board map
    
    Args:
        index (int): the index of the obj
    
    Returns:
        AbstractMarker: the abstract marker
    
    """
    pass