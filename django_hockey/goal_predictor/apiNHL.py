import requests
from .models import *
import datetime

BASE_URL='https://statsapi.web.nhl.com/api/v1'


ENDPOINT_DICT=  {
    'player_info' :      '/people/{}',
    'player_game_log' :    '/people/{}/stats?stats=gameLog&season={}',
    'player_season_stats' : '/people/{}/stats?stats=statsSingleSeason&season={}',
    'player_div_splits' :   '/people/{}/stats?stats=vsDivision&season={}',
    'player_mon_splits' :   '/people/{}/stats?stats=byMonth&season={}',
    'player_week_splits' :  '/people/{}/stats?stats=byDayOfWeek&season={}',
    'player_league_stats' : '/people/{}/stats?stats=regularSeasonStatRankings&season={}',
    'player_season_pace' :  '/people/{}/stats?stats=onPaceRegularSeason&season={}',
    'player_sit_goals' :    '/people/{}/stats?stats=goalsByGameSituation&season={}',
    'player_day_splits' :   '/people/{}/stats?stats=byDayOfWeek&season={}',
    'player_home_split' :   '/people/{}/stats?stats=homeAndAway&season={}',
    'player_win_split' :    '/people/{}/stats?stats=winLoss&season={}',
    'game_box' :            '/game/{}/boxscore',
    'game_live' :           '/game/{}/feed/live',
    'fetch_teams' :         '/teams?season={}',
    'team_schedule' :       '/schedule?season={}&teamId={}',
    'team_roster' :         '/teams/{}?expand=team.roster&season={}',
    'team_stats' :          '/teams/{}?expand=team.stats&season={}',
    }

##function to populate Teams from the NHL api
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

#helper functions:

#create a function that fetches the names of all the teams for a season
def fetch_teams(season = get_current_season()):
    #can change later to set by user
    url = BASE_URL+ENDPOINT_DICT['fetch_teams'].format(season)
    response = requests.get(url)
    data = response.json()
    return data["teams"]

#create a function that calls the roster from the api for a Team instance
def get_team_roster(team_id,season = get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_roster'].format(team_id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['roster']['roster']

#create a function that calls the team schedule from the api for a Team instance
def get_team_schedule(team_id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_schedule'].format(season, team_id)
    response = requests.get(url)
    data = response.json()
    return data['dates']

#create a function that calls the team stats from the api for a Team instance
def get_team_stats(team_id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_stats'].format(team_id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['teamStats'][0]['splits'][0]['stat']

#create a function that calls the team stat ranking from the api for a Team instance
def get_team_rankings(team_id,season=get_current_season()):
    #will have to chagne at some point to take in the season expression
    url = BASE_URL + ENDPOINT_DICT['team_stats'].format(team_id, season)
    response = requests.get(url)
    data = response.json()
    return data['teams'][0]['teamStats'][0]['splits'][1]['stat']


##function to populate Players from the NHL api.
def populate_players(season=get_current_season()):
    teams = Team.objects.all()
    for team in teams:
        #fetch all the player from 'teams'
        players = fetch_team_players(team.id, season=season)
        player_instances = []
        for player_data in players:
            player_id = player_data['id']
            info = get_player_info(player_id)
            breakpoint()
            player = Player(
                #these we can get from player_data because they come from the team roster information we used to make player_data
                nhl_id=player_id,
                name=player_data['name'],
                info=info,
                position=info['primaryPosition']['code'],
                team=team,
                season=season,
                )
            player_instances.append(player)
        Player.objects.bulk_create(player_instances)


#create a function that gets all the palyers from a team. NOT COMPLETE.
def fetch_team_players(team_id, season=None):
    """
    Fetches player data for a given team from the NHL API.

    Parameters:
    - team_id (int): the database id of the team
    - season (str): the season to get data for (in YYYY-YYYY format)
    """
    url = BASE_URL + ENDPOINT_DICT['team_roster'].format(team_id, season)
    response = requests.get(url)
    data = response.json()
    players = []
    for player_data in data['teams'][0]['roster']['roster']:
        player = {
            'id': player_data['person']['id'],
            'name': player_data['person']['fullName'],
            'position': player_data['position']['name'],
        }
        players.append(player)
    return players

#helper functions:

#create a function that calls the players information 
def get_player_info(player_id):
    """
    Fetches player information from the NHL API.

    Parameters:
    - player_id (int): the NHL ID for the player
    """
    url = BASE_URL + ENDPOINT_DICT['player_info'].format(player_id)
    response = requests.get(url)
    data = response.json()
    return data


##function to populate PlayerGameLog stats tables from the NHL api
def populate_player_game_logs(season=get_current_season()):
    players = Player.objects.all()
    player_game_logs = []
    for player in players:
        player_id = player.nhl_id
        game_log_data = get_player_game_log(player_id, season)
        for game_data in game_log_data:
            player_game_log = PlayerGameLog(
                player=player,
                season=game_data['season'],
                time_on_ice=game_data['time_on_ice'],
                assists=game_data['assists'],
                goals=game_data['goals'],
                pim=game_data['pim'],
                shots=game_data['shots'],
                games=game_data['games'],
                hits=game_data['hits'],
                power_play_goals=game_data['power_play_goals'],
                power_play_points=game_data['power_play_points'],
                power_play_time_on_ice=game_data['power_play_time_on_ice'],
                even_time_on_ice=game_data['even_time_on_ice'],
                penalty_minutes=game_data['penalty_minutes'],
                faceoff_pct=game_data['faceoff_pct'],
                shot_pct=game_data['shot_pct'],
                game_winning_goals=game_data['game_winning_goals'],
                overtime_goals=game_data['overtime_goals'],
                shorthanded_goals=game_data['shorthanded_goals'],
                shorthanded_points=game_data['shorthanded_points'],
                shorthanded_time_on_ice=game_data['shorthanded_time_on_ice'],
                blocked=game_data['blocked'],
                plus_minus=game_data['plus_minus'],
                points=game_data['points'],
                shifts=game_data['shifts'],
                team_id=game_data['team_id'],
                team_name=game_data['team_name'],
                opponent_id=game_data['opponent_id'],
                opponent_name=game_data['opponent_name'],
                game_id=game_data['game_id'],
                game_link=game_data['game_link'],
                date=game_data['date'],
                is_home=game_data['is_home'],
                is_win=game_data['is_win'],
                is_ot=game_data['is_ot'],
            )
            player_game_logs.append(player_game_log)
    PlayerGameLog.objects.bulk_create(player_game_logs)


#create a function that calls the players game_log, season is defined when running parent function populate_players
def get_player_game_log(player_id, season):
    """
    Fetches game log data for a given player ID and season from the NHL API and returns it in a dictionary format.

    Parameters:
    - player_id (int): the NHL ID for the player
    - season (str): the season to get data for (in YYYY-YYYY format)
    """
    url = BASE_URL + ENDPOINT_DICT['player_game_log'].format(player_id, season)
    response = requests.get(url)
    data = response.json()
    game_log = data
    game_log_data = []
    if game_log['stats'] and game_log['stats'][0]['splits']:
        for split in game_log['stats'][0]['splits']:
            game_data = {}
            game_data['season'] = split['season']
            
            # Extract fields from 'stat' dictionary
            stat_data = split['stat']
            game_data['time_on_ice'] = str(datetime.datetime.strptime(stat_data.get('timeOnIce'), '%M:%S').time())  if stat_data.get('timeOnIce') else '00:00:00'
            game_data['assists'] = stat_data.get('assists')
            game_data['goals'] = stat_data.get('goals')
            game_data['pim'] = stat_data.get('pim')
            game_data['shots'] = stat_data.get('shots')
            game_data['games'] = stat_data.get('games')
            game_data['hits'] = stat_data.get('hits')
            game_data['power_play_goals'] = stat_data.get('powerPlayGoals')
            game_data['power_play_points'] = stat_data.get('powerPlayPoints')
            game_data['power_play_time_on_ice'] = str(datetime.datetime.strptime(stat_data.get('powerPlayTimeOnIce'), '%M:%S').time()) if stat_data.get('powerPlayTimeOnIce') else '00:00:00'
            game_data['penalty_minutes'] = stat_data.get('penaltyMinutes')
            game_data['faceoff_pct'] = stat_data.get('faceOffPct', None)
            game_data['shot_pct'] = stat_data.get('shotPct', None)
            game_data['game_winning_goals'] = stat_data.get('gameWinningGoals')
            game_data['overtime_goals'] = stat_data.get('overTimeGoals')
            game_data['shorthanded_goals'] = stat_data.get('shortHandedGoals')
            game_data['shorthanded_points'] = stat_data.get('shortHandedPoints')
            game_data['shorthanded_time_on_ice'] = str(datetime.datetime.strptime(stat_data.get('shorthanded_time_on_ice'), '%M:%S').time()) if stat_data.get('shorthanded_time_on_ice') else '00:00:00'
            game_data['blocked'] = stat_data.get('blocked')
            game_data['plus_minus'] = stat_data.get('plusMinus')
            game_data['points'] = stat_data.get('points')
            game_data['shifts'] = stat_data.get('shifts')
            
            # Extract fields from 'team' dictionary
            team_data = split['team']
            game_data['team_id'] = team_data['id']
            game_data['team_name'] = team_data['name']
            
            # Extract fields from 'opponent' dictionary
            opponent_data = split['opponent']
            game_data['opponent_id'] = opponent_data['id']
            game_data['opponent_name'] = opponent_data['name']
            
            # Extract fields from 'game' dictionary
            game_data_dict = split['game']
            game_data['game_id'] = game_data_dict['gamePk']
            game_data['game_link'] = game_data_dict['link']
            
            # Extract remaining fields
            game_data['date'] = split['date']
            game_data['is_home'] = split['isHome']
            game_data['is_win'] = split['isWin']
            game_data['is_ot'] = split['isOT']
            
            game_log_data.append(game_data)
            breakpoint()
    return game_log_data

    # if data['stats'][0]['splits']:  ##to pull the game splits as a dictionary
    #     # Extract the stats data from the JSON response
    #     game_data = data['stats'][0]
    #     game_log = game_data['splits']


    

#create a function that calls season stats from api and extracts the stats
def get_player_season_stats(player_id, season):
    """
    Fetches player season stats for a given player ID and season from the NHL API.

    Parameters:
    - player_id (int): the NHL ID of the player
    - season (str): the season to get data for (in YYYY-YYYY format)
    """
    url = BASE_URL + ENDPOINT_DICT['player_season_stats'].format(player_id, season)
    response = requests.get(url)
    data = response.json()
    season_stats = {}
    if data['stats']:
        # Extract the stats data from the JSON response
        stats_data = data['stats'][0]
        season_stats = stats_data['splits'][0]['stat']
    return season_stats

#create a function that calls division splits from api and extracts the stats
def get_player_div_splits(player_id, season):
    """
    Fetches player division splits for a given player ID and season from the NHL API.

    Parameters:
    - player_id (int): the NHL ID of the player
    - season (str): the season to get data for (in YYYY-YYYY format)
    """
    url = BASE_URL + ENDPOINT_DICT['player_div_splits'].format(player_id, season)
    response = requests.get(url)
    data = response.json()
    div_splits = {}
    if data['stats']:
        # Extract the division splits data from the JSON response
        div_splits_data = data['stats'][0]
        div_splits = div_splits_data['splits']
    return div_splits


