import requests
from .models import Team, get_current_season

BASE_URL='https://statsapi.web.nhl.com/api/v1'


ENDPOINT_DICT=  {
    'get_player' :      '/people/{}',
    'get_game_log' :    '/people/{}/stats?stats=gameLog&season={}',
    'season_stat' :     '/people/{}/stats?stats=statsSingleSeason&season={}',
    'div_split' :       '/people/{}/stats?stats=vsDivision&season={}',
    'mon_split' :       '/people/{}/stats?stats=byMonth&season={}',
    'week_split' :      '/people/{}/stats?stats=byDayOfWeek&season={}',
    'league_stat' :     '/people/{}/stats?stats=regularSeasonStatRankings&season={}',
    'season_pace' :     '/people/{}/stats?stats=onPaceRegularSeason&season={}',
    'sit_goals' :       '/people/{}/stats?stats=goalsByGameSituation&season={}',
    'day_split' :       '/people/{}/stats?stats=byDayOfWeek&season={}',
    'home_away_split' : '/people/{}/stats?stats=homeAndAway&season={}',
    'win_loss_split' :  '/people/{}/stats?stats=winLoss&season={}',
    'game_box' :        '/game/{}/boxscore',
    'game_live' :       '/game/{}/feed/live',
    'fetch_teams' :     '/teams?season={}',
    'team_schedule' :   '/schedule?season={}&teamId={}',
    'team_roster' :     '/teams/{}?expand=team.roster&season={}',
    }

def populate_teams():
    teams = fetch_teams()
    for team_data in teams:
       team = Team(id=team_data['id'],
                   name=team_data['name'],
                   info=team_data,
                   roster = get_team_roster(id),
                   schedule = get_team_schedule()
                   )
    return

def populate_players():
    return





#create a function that fetches the names of all the teams for a season
def fetch_teams(season):
    #can change later to a season variable that is global and set by user
    url = BASE_URL+ENDPOINT_DICT['fetch_teams'].format(season)
    response = requests.get(url)
    data = response.json()
    return data["teams"]

#create a function that calls the roster from the api for a Team instance
def get_team_roster(id,season):
    #will have to chagne at some point to take in the season expression
    season = get_current_season()
    url = BASE_URL + ENDPOINT_DICT['team_roster'].format(id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['roster']['roster']

#create a function that calls the team schedule from 
def get_team_schedule(id, season):
    #will have to chagne at some point to take in the season expression
    season = get_current_season()
    url = BASE_URL + ENDPOINT_DICT['team_schedule'].format(season, id)
    response = requests.get(url)
    data = response.json()
    return data['dates']

