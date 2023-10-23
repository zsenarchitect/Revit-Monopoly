from ASSET import Asset


class Jail(Asset):
    def is_term_finished(self):
        # check if player inside should be released
        pass


    
    @property
    def holding_round(self):
        return 3