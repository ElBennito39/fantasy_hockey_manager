from django.test import TestCase
from unittest.mock import patch

# Create your tests here.
from django.test import TestCase
from .models import get_current_season

#auto generated tests for Models..
from django.test import TestCase
from .models import Team, Player, PlayerGameLog, PlayerSeasonStats
from .apiNHL import *

class PopulationFunctionTests(TestCase):
    def test_populate_functions(self):
        test_team_id = 5  # Replace this with the desired team's ID
        test_player_id = 8471675  # Replace this with the desired player's NHL ID
        test_season = get_current_season()

        # Only populate the desired team
        original_teams = fetch_teams(season=test_season)
        filtered_teams = list(filter(lambda x: x['id'] == test_team_id, original_teams))
        with patch('goal_predictor.apiNHL.fetch_teams', return_value=filtered_teams):
            populate_teams()

        # Only populate players for the desired team
        original_players = fetch_team_players(test_team_id, season=test_season)
        with patch('goal_predictor.apiNHL.fetch_team_players', return_value=original_players):
            populate_players()

        test_player = Player.objects.get(nhl_id=test_player_id)
        populate_player_game_logs(test_player, test_season)
        populate_player_season_stats(test_season)

        # Check if the objects were created in the database
        self.assertIsNotNone(Team.objects.get(nhl_id=test_team_id))
        self.assertIsNotNone(test_player)
        self.assertIsNotNone(PlayerGameLog.objects.filter(player=test_player))
        self.assertIsNotNone(PlayerSeasonStats.objects.filter(player=test_player, season=test_season))


class TeamTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            id=1,
            nhl_id=5,
            name='Pittsburgh Penguins',
            info={},
            roster={},
            schedule={},
            stats={},
            rankings={},
            season=get_current_season(),
        )

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Pittsburgh Penguins')


class PlayerTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            id=1,
            nhl_id=5,
            name='Pittsburgh Penguins',
            info={},
            roster={},
            schedule={},
            stats={},
            rankings={},
            season=get_current_season(),
        )
        self.player = Player.objects.create(
            id=1,
            nhl_id=8471675,
            name='Sidney Crosby',
            position='C',
            team=self.team,
            info={
                "id" : 8471675,
                "fullName" : "Sidney Crosby",
                "link" : "/api/v1/people/8471675",
                "firstName" : "Sidney",
                "lastName" : "Crosby",
                "primaryNumber" : "87",
                "birthDate" : "1987-08-07",
                "currentAge" : 35,
                "birthCity" : "Cole Harbour",
                "birthStateProvince" : "NS",
                "birthCountry" : "CAN",
                "nationality" : "CAN",
                "height" : "5' 11\"",
                "weight" : 200,
                "active" : True,
                "alternateCaptain" : False,
                "captain" : True,
                "rookie" : False,
                "shootsCatches" : "L",
                "rosterStatus" : "Y",
                "currentTeam" : {
                    "id" : 5,
                    "name" : "Pittsburgh Penguins",
                    "link" : "/api/v1/teams/5"
                    },
                "primaryPosition" : {
                    "code" : "C",
                    "name" : "Center",
                    "type" : "Forward",
                    "abbreviation" : "C"
                    }
            },
            season='20222023',
        )
    #test the player object by seeing its string representation
    def test_player_str(self):
        self.assertEqual(str(self.player), 'Sidney Crosby')
    #test that the play info dictionary has the same id as the player's nhl_id
    def test_player_info_id(self):
        self.assertEqual(self.player.info['id'], self.player.nhl_id)
    # test the association between team and player
    def test_player_team(self):
        #check the player to team relationship
        self.assertEqual(self.player.team, self.team)
        #check the player's info dictionary for team name with the name from team
        self.assertEqual(self.player.info['currentTeam']['name'], self.team.name)
        #check the player's info dictionary for team id with the nhl_id from team
        self.assertEqual(self.player.info['currentTeam']['id'], self.team.nhl_id)


class PlayerGameLogTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            id=1,
            nhl_id=5,
            name='Pittsburgh Penguins',
            info={},
            roster={},
            schedule={},
            stats={},
            rankings={},
            season=get_current_season(),
        )
        self.player = Player.objects.create(
            id=1,
            nhl_id=8471675,
            name='Sidney Crosby',
            position='C',
            team=self.team,
            info={}
        )
        self.game_log = PlayerGameLog.objects.create(
            player=self.player,
            season='20222023',
            time_on_ice=600,
            assists=1,
            goals=1,
            pim=0,
            shots=2,
            games=1,
            hits=1,
            power_play_goals=1,
            power_play_points=1,
            power_play_time_on_ice=120,
            even_time_on_ice=480,
            penalty_minutes=0,
            faceoff_pct=None,
            shot_pct=50,
            game_winning_goals=1,
            overtime_goals=0,
            shorthanded_goals=0,
            shorthanded_points=0,
            shorthanded_time_on_ice=0,
            blocked=1,
            plus_minus=1,
            points=2,
            shifts=19,
            team_id=self.team.id,
            team_name=self.team.name,
            opponent_id=2,
            opponent_name='Test_Opponent',
            game_id=1,
            game_link='https://www.nhl.com/game/1',
            date='2022-10-01',
            is_home=True,
            is_win=True,
            is_ot=False
        )
    #test the string of our test data above.
    def test_game_log_str(self):
        self.assertEqual(str(self.game_log), 'Sidney Crosby - Pittsburgh Penguins vs. Test_Opponent on 2022-10-01')

    #test relationship between 'Player' and 'PlayerGameLog'
    def test_game_log_player(self):
        self.assertEqual(self.game_log.player, self.player)
    #test relationship between 'Team' and 'PlayerGameLog'
    def test_game_log_team(self):
        self.assertEqual(self.game_log.team_id, self.team.id)
        self.assertEqual(self.game_log.team_name, self.team.name)


class PlayerSeasonStatsTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            id=1,
            nhl_id=5,
            name='Pittsburgh Penguins',
            info={},
            roster={},
            schedule={},
            stats={},
            rankings={},
            season=get_current_season(),
        )
        self.player = Player.objects.create(
            id=1,
            nhl_id=8471675,
            name='Sidney Crosby',
            position='C',
            team=self.team,
            info={}
        )
        self.stats = PlayerSeasonStats.objects.create(
            player=self.player,
            season='20222023',
            games=0,
            goals=0,
            assists=0,
            points=0,
            plus_minus=0,
            pim=0,
            shots=0,
            shot_pct=None,
            faceoff_pct=None,
            hits=0,
            blocked=0,
            time_on_ice=0,
            power_play_goals=0,
            power_play_points=0,
            power_play_time_on_ice=0,
            even_time_on_ice=0,
            shifts=0,
            time_on_ice_per_game=0,
            even_time_on_ice_per_game=0,
            short_handed_time_on_ice_per_game=0,
            power_play_time_on_ice_per_game=0,
            game_winning_goals=0,
            overtime_goals=0,
            short_handed_goals=0,
            short_handed_points=0,
            short_handed_time_on_ice=0
        )

    def test_player_season_stats_str(self):
        expected_str = 'Sidney Crosby - 20222023 Season Stats'
        self.assertEqual(str(self.stats), expected_str)

    def test_player_season_stats_verbose_name_plural(self):
        expected_verbose_name_plural = 'player season stats'
        self.assertEqual(PlayerSeasonStats._meta.verbose_name_plural, expected_verbose_name_plural)

    def test_player_season_stats_defaults(self):
        defaults = {
            'games': 0,
            'goals': 0,
            'assists': 0,
            'points': 0,
            'plus_minus': 0,
            'pim': 0,
            'shots': 0,
            'shot_pct': None,
            'faceoff_pct': None,
            'hits': 0,
            'blocked': 0,
            'time_on_ice': 0,
            'power_play_goals': 0,
            'power_play_points': 0,
            'power_play_time_on_ice': 0,
            'even_time_on_ice': 0,
            'shifts': 0,
            'time_on_ice_per_game': 0,
            'even_time_on_ice_per_game': 0,
            'short_handed_time_on_ice_per_game': 0,
            'power_play_time_on_ice_per_game': 0,
            'game_winning_goals': 0,
            'overtime_goals': 0,
            'short_handed_goals': 0,
            'short_handed_points': 0,
            'short_handed_time_on_ice': 0
        }
        stats = PlayerSeasonStats.objects.create(player=self.player, season='20222023')
        for key, value in defaults.items():
            self.assertEqual(getattr(stats, key), value)
