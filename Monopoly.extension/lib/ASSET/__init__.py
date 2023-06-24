

# foundation class for all thing in map that is not moveable.

class Asset(object):
    def __init__(self, revit_object):
        self.revit_object = revit_object

    def hide(self):
        # hide in view
        pass

    def show(self):
        # show in view
        pass

    def position_index(self):
        # return the index of the position on map.
        # this index is uesed for other to find it.
        pass

    def location(self):
        # return XYZ coordinates of the asset
        pass

    def is_occupied(self):
        # return True if there is a player or NPC on top.
        pass

    def get_occupied_characters(self):
        # return all the players or NPC on top.
        pass
