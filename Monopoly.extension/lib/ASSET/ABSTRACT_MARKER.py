# this handle the marker in the borad
# this is to help player move around and get the infomation they need
# for 


from ASSET import Asset
import ERROR_HANDLE
import json


class AbstractMarker(Asset):


    @ERROR_HANDLE.try_catch_error
    def get_action(self):
        
        """return all kind of action
        case 1: special tile, cannot do anything here.
            |-case 2: hard code go to, this is for hospital and jails with direct send.
            |-case 3: card tile
        case 4: empty tile with lot, no one build
        case 5: empty tile with lot, someone build(self, or others)
        """

        # case 1
        
        if self.revit_object.LookupParameter("can_purchase").AsInteger() == 0:
            # nothing to do here
            print ("case 1: Nothing to do here")
            # return 1
        
        
            # case 2
            if self.data.get("to", None):
                print ("case 2: go somehwere")
                print ("Go to " + self.data.get("to"))
                
                return 2
            

            # case 3
            if self.has_card_associated:
                print ("case 3: use card")
                print (self.associated_card.get_action())
                return 3
        
        
        # if reach here, it means the spot is purchaseable, so lets check if it has a property or not.
        has_property = hasattr(self, "property")
        
        
        # case 4
        if not has_property:
            print ("case 4: Land on a purchaseable and no property there , do you want to buy it? ")
            return 4
        
        # case 5
        else:
            # this is not a free land
            print ("case 5: Land on NOT purchaseable ")
            print (self.property)
            print  ("Land on a property owned by " + self.owner)
            if self.owner == self.get_occupied_characters:
                print ("you own this property, want to upgrade?")
                return 5.1
            if self.ower.team != self.occupying_player.team:
                print (" owner of this property is from other team, you need to pay charge.")
                return 5.2
                

 
    @property
    def data(self):
        comments = self.revit_object.LookupParameter("Comments").AsString()
        if comments:
            return json.loads(comments)
        else:
            return {}

    @property
    def has_card_associated(self):
        return self.associated_card is not None

    @property
    def associated_card(self):
        """find closest card object who is VERY close to this marker. 
        Do not use index to search becasue when designing the board thing can be moved around."""
        return None
    
    def create_new_property(self, player):
        """create property object for this marker"""
        from BUILDING.PROPERTY import Property
        self.property = Property(player, self)

