# this handle the marker in the borad
# this is to help player move around and get the infomation they need
# for 


from ASSET import Asset
import json

class AbstractMarker(Asset):

    pass

    def get_action(self):
        return
        """return all kind of action
        case 1: empty tile
        case 2: empty tile with lot, no one build
        case 3: empty tile with lot, someone build(self, or others)
        case 4: card tile
        case 5: hard code go to, this is for hospital and jails with direct send."""

        # case 5
        if self.data.get("to", None):
            print "Go to " + self.data.get("to")

        # case 4
        if self.has_card_associated:
            print self.associated_card.get_action()
        
        # case 1
        if self.revit_obj.LookupParameter("can_purchase").AsInteger() == 0:
            # nothing to do here
            return

        # case 2
        if not self.owner:
            
            return "Land on a purchaseable , do you want to buy it? "
        # case 3
        else:
            # this is not a free land
            print self.property
            print  "Land on a property owned by " + owner
            if self.owner == self.get_occupied_characters:
                print "you own this property, want to upgrade?"
            if self.ower.team != self.occupying_player.team:
                print " owner of this property is from other team, you need to pay charge."

 
    @property
    def data(self):
        comments = self.revit_obj.LookupParameter("Comments").AsString()
        return json.loads(comments)

    @property
    def has_card_associated(self):
        return self.associated_card is not None

    @property
    def associated_card(self):
        """find closest card object who is VERY close to this marker. 
        Do not use index to search becasue when designing the board thing can be moved around."""
        return None