from API_serv import *

class Player:
  all = []

  current_player =''

  player_count = 0

  def __init__(self,ID, data):

    self.ID = ID
    self.data_from_player = data
    self.name = data[0]['fullName']

    Player.player_count +=1

    self.all.append(self)
    print("Player " + str(self) + " " + self.name + " Created")


    
    self.game_log = get_game_log(self.ID)

    self.season_stats = season_stat(self.ID)

    self.div_stats = div_split(self.ID)

    self.day_stats = day_split(self.ID)

    self.mon_stats = mon_split(self.ID)

    self.week_stats = week_split(self.ID)

    self.league_stats = league_stat(self.ID)

    self.season_pace = season_pace(self.ID)

    self.home_away_stats = home_away_split(self.ID)

    self.w_l_stats = win_loss_split(self.ID)

    self.sit_goals = sit_goals(self.ID)

    self.schedule = player_schedule(self.ID)

    
  def __str__(self):
    return( str(self.ID) )

  @classmethod
  def select_player(cls, name):
    all_players = Player.all
    for player in all_players:
      if player.data_from_player[0]['fullName'] == name:
        Player.current_player = player
        return player
