from functools import reduce
import operator 
from API_serv import *
from Player import *
from Team import Team
#########################################################################################
# Services for local handling
#########################################################################################
### generate a list of all team IDs
#########################################################################################
### generate a list of all players (dictionaries)

def get_active_teams():
    # get all active teams
    teams = fetch_teams()

    for team in teams:
        # breakpoint()
        Team(team['id'],team)


    def fetch_team_id(team):
        return team['id']

    # map the team id and the teams data to the class variable
    return map(fetch_team_id, Team.all)


def get_active_players():
    #get all active team data
    all_teams = Team.all


    for team in all_teams:
        # breakpoint()
        i = 0
        for player in team.roster: 
            if i <1:
                player_id = player['person']['id']  
                Player(player_id,get_player(player_id))
                i += 1
                # breakpoint()
            else:
                pass
    
    def fetch_player_id(player):
        return player['id']
    
    #map the player id and the player data to class variable
    return map(fetch_player_id, Player.all)
