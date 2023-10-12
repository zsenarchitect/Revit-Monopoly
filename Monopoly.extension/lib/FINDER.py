# use this to find revit obj by spec. or find game obj by spec
import logging
import ERROR_HANDLE
import os
logging.basicConfig(level=logging.INFO,
                    filename="{}\{}_log.txt".format(ERROR_HANDLE.LOG_FOLDER,
                                                    os.path.basename(__file__).rstrip(".py")),
                    filemode="w")



from Autodesk.Revit import DB
try:
    doc = __revit__.ActiveUIDocument.Document
except:
    pass


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
  
        if gm.Name == character_name:
            return gm
        
    logging.warning("no such revit obj found")
    
    return None

@ERROR_HANDLE.try_catch_error
def get_revit_obj_by_type_name(name):
    """get the revit obj by the name
    
    Args:
        name (str): the name of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    
    all_gms = get_all_generic_models()
    for gm in all_gms:
        logging.info(gm.Name)
        if gm.Name == name:
            return gm
        
    logging.warning("no such revit obj found")
    
    return None


@ERROR_HANDLE.try_catch_error
def get_revit_obj_by_index(index):
    """get the revit obj by the position index, the index can be lookup in the board map
    
    Args:
        index (int): the index of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    all_gms = get_all_generic_models()
    for gm in all_gms:
        #print gm.LookupParameter("Mark").AsString()
        if gm.LookupParameter("Mark").AsString() == str(index):
            return gm



@ERROR_HANDLE.try_catch_error
def get_abstract_marker_by_index(index):
    """get the abstract marker by the position index, the index can be lookup in the board map
    
    Args:
        index (int): the index of the obj
    
    Returns:
        AbstractMarker: the abstract marker
    
    """
    all_gms = get_all_generic_models()
    for gm in all_gms:
        if not gm.LookupParameter("Mark"):
            print (gm.Id)
            continue
        if gm.LookupParameter("Mark").AsString() == str(index):
            print ("find ")
            return gm


@ERROR_HANDLE.try_catch_error
def get_material_by_name(name):
    """get the material by the name
    
    Args:
        name (str): the name of the material
    
    Returns:
        DB.Material: the material
    
    """
    all_materials = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
    for material in all_materials:
        if material.Name == name:
            return material
    return None