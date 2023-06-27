from ASSET import Asset


class Property(Asset):
    value_map = {0:100,
                 1:200,
                 2:300,
                 3:500}
    charge_map = {0:150,
                  1:300,
                  2:450,
                  3:1000}
    def __init__(self):
        
        self.level = 0 #0 is new land, 1, 2, 3
        self.owner = None


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
        pass

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
