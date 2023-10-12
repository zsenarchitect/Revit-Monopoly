import os
def open():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    parent_folder = os.path.dirname(parent_folder)
    parent_folder = os.path.dirname(parent_folder)
    parent_folder = os.path.dirname(parent_folder)
    
    file = parent_folder + '\\revit_content\\Monopoly Game Board_2022.rvt'
    
    # print file
    from Autodesk.Revit import UI
    __revit__.OpenAndActivateDocument (file)
    