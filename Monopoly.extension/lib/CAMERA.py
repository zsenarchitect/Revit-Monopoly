from Autodesk.Revit import DB, UI



def zoom_to_elements(element_or_elements):
    """might need to zoom to play, or player + an asset, or all players in team
    Args:
        element_or_elements (element | list): one or many elements to zoom to
    """

    if not isinstance(element_or_elements, list):
        elements = [element_or_elements]


    # get the active view
    view = __revit__.ActiveUIDocument.ActiveView
    # get the bounding box of the elements
    bb = DB.BoundingBoxXYZ()
    for el in elements:
        bb.Union(el.get_BoundingBox(view))
    # zoom to the bounding box
    view.ZoomToFit(bb)