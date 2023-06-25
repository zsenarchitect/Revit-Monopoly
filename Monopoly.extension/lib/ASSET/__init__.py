import logging
import ERROR_HANDLE
import os
logging.basicConfig(level=logging.INFO,
                    filename="{}\{}_log.txt".format(ERROR_HANDLE.LOG_FOLDER,
                                                    os.path.basename(__file__).rstrip(".py")),
                    filemode="w")




import FINDER
# foundation class for all thing in map that is not moveable.

class Asset(object):
    def __init__(self, revit_object = None):
        """COnstructor for base class Asset, that is something that is not moveable.
        Args:
            revit_object (optional: DB.Element): the revit object, if do not provide infomation then use class name to find revit oject
        """
        if revit_object is None:
            revit_object = FINDER.get_revit_obj_by_type_name(self.__class__.__name__)
        
        
        self.revit_object = revit_object
        logging.info (self.__class__.__name__)
        logging.info (self.revit_object)

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

        return self.revit_object.Location.Point
    
    

    def is_occupied(self):
        """return True if there is a player or NPC on top."""
        pass

    def get_occupied_characters(self):
        """return all the players or NPC on top."""
        pass
