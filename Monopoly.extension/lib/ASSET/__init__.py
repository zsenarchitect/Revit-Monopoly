

# foundation class for all thing in map that is not moveable.

class Asset(object):
    def __init__(self, revit_object):
        """COnstructor for base class Asset, that is something that is not moveable.
        Args:
            revit_object (object): the revit object
        """
        self.revit_object = revit_object

    def hide(self, animated = False):
        """hide asset in view.
        
        Args:
            animated (bool): if True, the hiding process will be animated.
        """
        if animated:
            # call DISPLAY.gradually_disappear_element(self.revit_object)
            pass

        # call DISPLAY.hide_element(self.revit_object)
        pass

    def show(self, animated = False):
        """show asset in view.
        
        Args:
            animated (bool): if True, the showing process will be animated.
        """
        if animated:
            # call DISPLAY.gradually_appear_element(self.revit_object)
            pass

        # call DISPLAY.show_element(self.revit_object)
        pass


    @property
    def position_index(self):
        """return the index of the position on map.
        # this index is uesed for other to find it
        """
        pass

    @property
    def location(self):
        """this is XYZ location of the obj
        
        """

        pass

    def is_occupied(self):
        """return True if there is a player or NPC on top."""
        pass

    def get_occupied_characters(self):
        """return all the players or NPC on top."""
        pass
