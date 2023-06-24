from ASSET import Asset


class Property(Asset):
    def is_owned(self):
        pass
        # check if any player own it.

    @property
    def owner(self):
        # return the owner of the asset
        pass

    @property
    def team(self):
        # return the team of the owner.
        pass

    @property
    def level(self):
        # level of the asset, from 1 to 3
        pass

    @property
    def charge(self):
        # the amount of charge is directedly linked to level.
        """
        level 0(someone is purchasing): $ 50
        level 1: $100
        level 2: $300
        level 3: $500"""

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
