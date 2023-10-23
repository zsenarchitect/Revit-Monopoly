from ASSET import Asset


class Jail(Asset):
    def is_term_finished(self):
        # check if player inside should be released
        pass


    
    @property
    def holding_round(self):
        return 5
    
    
    @property
    def holding_text(self):
        return "still in jail."
    
    @property
    def exit_to(self):
        return 13