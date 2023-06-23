# use this to find revit obj by spec. or find game obj by spec
from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document


def get_revit_obj(name):
    all_gms = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_GenericModel).WhereElementIsNotType().ToElements()
    for gm in all_gms:
        if gm.Name == name:
            return gm
