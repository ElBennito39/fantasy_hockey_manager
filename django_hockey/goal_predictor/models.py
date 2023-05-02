from django.db import models
from django.core.management.base import CommandError, BaseCommand


import datetime

# Create your models here.

## Function to get the current season
## Current_Season assignment from today's date
def get_current_season():
    
    today = datetime.date.today()

    if today.month >= 10:
        return f"{today.year}{today.year + 1}"
    else:
        return f"{today.year - 1}{today.year}"

## Create class Team where id, name are static and roster,schedule,stats,rankings change with season.
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    nhl_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    info = models.JSONField(default=dict)
    roster = models.JSONField(default=dict)
    schedule = models.JSONField(default=dict)
    stats = models.JSONField(default=dict)
    rankings = models.JSONField(default=dict)

    season = models.CharField(max_length=10,default=get_current_season())
    

    def __str__(self):
        return self.name



## Create class Player where id, name are static and rest dynamic
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    nhl_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)    
    position = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    info = models.JSONField(default=dict)

    season = models.CharField(max_length=10, default=get_current_season())

    def __str__(self):
        return self.name

##Create classes for api stat calls, so that each produces an associated table to Player with foreign key

#get player's log of games for a season
class PlayerGameLog(models.Model):
    # id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    time_on_ice = models.IntegerField()
    assists = models.IntegerField()
    goals = models.IntegerField()
    pim = models.IntegerField()
    shots = models.IntegerField()
    games = models.IntegerField()
    hits = models.IntegerField()
    power_play_goals = models.IntegerField()
    power_play_points = models.IntegerField()
    power_play_time_on_ice = models.IntegerField()
    even_time_on_ice = models.IntegerField()
    penalty_minutes = models.IntegerField()
    faceoff_pct = models.FloatField(null=True)
    shot_pct = models.FloatField(null=True)
    game_winning_goals = models.IntegerField()
    overtime_goals = models.IntegerField()
    shorthanded_goals = models.IntegerField()
    shorthanded_points = models.IntegerField()
    shorthanded_time_on_ice = models.IntegerField()
    blocked = models.IntegerField()
    plus_minus = models.IntegerField()
    points = models.IntegerField()
    shifts = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=50)
    opponent_id = models.IntegerField()
    opponent_name = models.CharField(max_length=50)
    game_id = models.IntegerField()
    game_link = models.URLField()
    date = models.DateField()
    is_home = models.BooleanField()
    is_win = models.BooleanField()
    is_ot = models.BooleanField()

    def __str__(self):
        return f'{self.player.name} - {self.team_name} vs. {self.opponent_name} on {self.date}'

#get player stats for a given season
class PlayerSeasonStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    games = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    plus_minus = models.IntegerField(default=0)
    pim = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shot_pct = models.FloatField(null=True)
    faceoff_pct = models.FloatField(null=True)
    hits = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)
    time_on_ice = models.IntegerField(default=0)
    power_play_goals = models.IntegerField(default=0)
    power_play_points = models.IntegerField(default=0)
    power_play_time_on_ice = models.IntegerField(default=0)
    even_time_on_ice = models.IntegerField(default=0)
    shifts = models.IntegerField(default=0)
    time_on_ice_per_game = models.IntegerField(default=0)
    even_time_on_ice_per_game = models.IntegerField(default=0)
    short_handed_time_on_ice_per_game = models.IntegerField(default=0)
    power_play_time_on_ice_per_game = models.IntegerField(default=0)
    game_winning_goals = models.IntegerField(default=0)
    overtime_goals = models.IntegerField(default=0)
    short_handed_goals = models.IntegerField(default=0)
    short_handed_points = models.IntegerField(default=0)
    short_handed_time_on_ice = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'player season stats'

    def __str__(self):
        return f'{self.player.name} - {self.season} Season Stats'

    


class PlayerDivSplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerMonSplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerWeekSplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerLeagueStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerSeasonPace(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerSitGoals(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerDaySplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerHomeSplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)


class PlayerWinSplits(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=8)
    data = models.JSONField(default=dict)

