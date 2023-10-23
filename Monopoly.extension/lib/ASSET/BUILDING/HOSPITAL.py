from ASSET import Asset


class Hospital(Asset):
    def is_term_finished(self):
        # check if player inside should be released
        pass


    
    def get_holding_charge(self, player):
        if player.profession == "Doctor":
            return 0
        return 300

    @property
    def holding_round(self):
        return 3