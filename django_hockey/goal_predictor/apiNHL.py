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
    'team_stats' :      '/teams/{}?expand=team.stats&season={}',
    }

def populate_teams(season = get_current_season()):
    teams = fetch_teams(season=season)
    team_instances =[]
    for team_data in teams:
       team_id = team_data['id']
       team = Team(
                   nhl_id=team_id,
                   name=team_data['name'],
                   info=team_data,
                   roster = get_team_roster(team_id, season=season),
                   schedule = get_team_schedule(team_id, season=season),
                   stats =  get_team_stats(team_id, season=season),
                   rankings = get_team_rankings(team_id, season=season),
                   season = season
                   )
       team_instances.append(team)
    #    breakpoint()
    #    team.save(commit=False)
    Team.objects.bulk_create(team_instances)

def populate_players():
    return





#create a function that fetches the names of all the teams for a season
def fetch_teams(season = get_current_season()):
    #can change later to set by user
    url = BASE_URL+ENDPOINT_DICT['fetch_teams'].format(season)
    response = requests.get(url)
    data = response.json()
    return data["teams"]

#create a function that calls the roster from the api for a Team instance
def get_team_roster(id,season = get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_roster'].format(id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['roster']['roster']

#create a function that calls the team schedule from the api for a Team instance
def get_team_schedule(id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_schedule'].format(season, id)
    response = requests.get(url)
    data = response.json()
    return data['dates']

#create a function that calls the team stats from the api for a Team instance
def get_team_stats(id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_stats'].format(id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['teamStats'][0]['splits'][0]['stat']

#create a function that calls the team stat ranking from the api for a Team instance
def get_team_rankings(id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_stats'].format(id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['teamStats'][0]['splits'][1]['stat']