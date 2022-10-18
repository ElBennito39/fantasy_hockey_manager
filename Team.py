from API_serv import *
class Team:
  all = []

  current_team =''

  def __init__(self,ID,data):
    self.ID = ID
    self.data_from_teams = data
    self.name = data['name']

    # self.schedule = team_schedule(ID)
    self.roster = team_roster(ID)

    # self.details = http_get_team_details(ID)

    self.all.append(self)
    print("Team " + str(self) + ' "' + self.name + '" Created')

  ##print or return?
  def __str__(self):
    return( str(self.ID) )

  @classmethod
  def select_team(cls, name):
    all_teams = Team.all
    for team in all_teams:
      if team.data_from_teams['name'] == name:
        Team.current_team = team
        return team
        # can use team.data_from_teams, to produce team information
        # can use team.roster, to produce roster information
        # however, can't use just 'team'