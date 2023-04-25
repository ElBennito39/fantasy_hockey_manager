
CURRENT_SEASON = "20212022"
LAST_SEASON = "20202021"
START_DATE = "2022-10-11"
END_DATE = "2022-04-14"
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
    'fetch_teams' :     '/teams',
    'team_schedule' :   '/schedule?teamId={}&startDate={}&endDate={}',
    'team_roster' :     '/teams/{}?expand=team.roster',
    }

