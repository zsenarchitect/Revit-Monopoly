import logging
import ERROR_HANDLE
import os
logging.basicConfig(level=logging.INFO,
                    filename="{}\{}_log.txt".format(ERROR_HANDLE.LOG_FOLDER,
                                                    os.path.basename(__file__).rstrip(".py")),
                    filemode="w")




import FINDER


doc = __revit__.ActiveUIDocument.Document








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
        #print (self.__class__.__name__)
        #print (self.revit_object)


    def get_action(self):
        """return the action of the asset.
        """
        return self.revit_object.LookupParameter("Comments").AsString()
    

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
        return int(self.revit_object.LookupParameter("Mark").AsString())
    
    def update_position_index(self, index):
        """update the index of the position on map.
        # this index is uesed for other to find it
        """
        #print ("-------------changing mark" + str(index))
        id = self.revit_object.Id
        doc.GetElement(id).LookupParameter("Mark").Set(index)
        self.revit_object.LookupParameter("Mark").Set(index)

        #print (self.revit_object.LookupParameter("Mark").AsInteger())
        #print (self.revit_object)

    @property
    def location(self):
        """this is XYZ location of the obj
        
        """

        return self.revit_object.Location.Point
    
    
    @property
    def is_occupied(self):
        """return True if there is a player or NPC on top."""
        print ("\ncurrent_players position:")
        for player in self.game.players:
            print (player.character, player.position_index)
        return len(self.get_occupied_characters()) > 0

    def get_occupied_characters(self):
        """return all the players or NPC on top."""
        return [player for player in self.game.players if player.position_index == self.position_index]
