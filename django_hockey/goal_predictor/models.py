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
    name = models.CharField(max_length=100)
    info = models.JSONField(default=dict)
    roster = models.JSONField(default=dict)
    schedule = models.JSONField(default=dict)
    stats = models.JSONField(default=dict)
    rankings = models.JSONField(default=dict)

    season = models.CharField(max_length=10,default=get_current_season())
    

    def __str__(self):
        return self.name

    # def get_roster(self):
    #     roster_data = http_get_roster(self.id)
    #     self.roster = parse_roster_data(roster_data)
    #     self.save()


## Create class Player where id, name are static and rest dynamic
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    info = models.JSONField(default=dict)
    
    position = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    game_log = models.JSONField(default=dict)
    season_stats = models.JSONField(default=dict)
    day_stats = models.JSONField(default=dict)
    week_stats = models.JSONField(default=dict)
    mon_stats = models.JSONField(default=dict)
    div_stats = models.JSONField(default=dict)
    league_stats = models.JSONField(default=dict)
    home_away_stats = models.JSONField(default=dict)
    w_l_stats = models.JSONField(default=dict)
    sit_goals = models.JSONField(default=dict)
    season_pace = models.JSONField(default=dict)

    schedule = models.JSONField(default=dict)

    season = models.CharField(max_length=10, default=get_current_season)

    def __str__(self):
        return self.name

    # def get_stats(self):
    #     stats_data = http_get_player(self.id)
    #     self.stats = parse_player_stats(stats_data)
    #     self.save()

