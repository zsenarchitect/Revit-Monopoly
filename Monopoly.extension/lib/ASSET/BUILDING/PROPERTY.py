from Autodesk.Revit import DB
doc = __revit__.ActiveUIDocument.Document


from ASSET import Asset
import DISPLAY
import SOUND




class Property(Asset):
    value_map = {0:100,
                 1:50,
                 2:100,
                 3:500}
    charge_map = {0:150,
                  1:300,
                  2:450,
                  3:1000}
    def __init__(self, player, marker):
        
        self.level = 1 #0 is new land, 1, 2, 3
        self.owner = player
        self.associated_marker = marker
        
        
        t = DB.Transaction(doc, "create property")
        t.Start()
        self.associated_marker.revit_object.LookupParameter("show_house_desire").Set(1)
        self.associated_marker.revit_object.LookupParameter("level").Set(1)
        t.Commit()
        
        SOUND.construction()
        self.update_color()
        
       

    def update_color(self):
        # update the color of the asset.
        DISPLAY.colorize_asset_by_agent(self.associated_marker, self.owner)
    
    
    @property
    def is_owned(self):
        return self.owner is not None
        # check if any player own it.



    @property
    def team(self):
        # return the team of the owner.
        return self.owner.team



    @property
    def value(self):
        return Property.value_map[self.level]

    @property
    def charge(self):
        return Property.charge_map[self.level]

    def upgrade_level(self):
        # increase the level, and cost some money unless waived by card.
        fee = self.value
        self.level += 1
        t = DB.Transaction(doc, "upgrade property")
        t.Start()
        self.associated_marker.revit_object.LookupParameter("level").Set(self.level)
        t.Commit()
        return fee
        

    def downgrade_level(self):
        # decrease the level.
        pass

    def charge_bypass_player(self, player):
        # deduct money from the player, and send to the owner.
        pass

    def find_connected_property_from_same_team(self):
        # search both end of the position_index and check if each spot has a property of same team.

        # return all the properties obj in list. The further apart the higher the multiple factor.
        pass
