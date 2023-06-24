"""handle all team action, solo player are also a team."""


class Team(object):
    def __init__(self, team_name, team_members):
        pass

    def is_solo_team(self):
        # return True if team has only one member.
        pass

    def is_team_lost(self):
        # return True if all team members is bankrupted.
        pass

    def exchange_team_data(self, other_team):
        pass
