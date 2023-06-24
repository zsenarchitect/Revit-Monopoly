# use this to find revit obj by spec. or find game obj by spec
from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document


def get_revit_obj_by_name(name):
    """get the revit obj by the name
    
    Args:
        name (str): the name of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    
    all_gms = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_GenericModel).WhereElementIsNotType().ToElements()
    for gm in all_gms:
        if gm.Name == name:
            return gm

def get_revit_obj_by_index(index):
    """get the revit obj by the position index, the index can be lookup in the board map
    
    Args:
        index (int): the index of the obj
    
    Returns:
        DB.Element: the revit obj
    
    """
    pass