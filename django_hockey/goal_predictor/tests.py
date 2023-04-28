from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import get_current_season

#auto generated tests for Models..
from django.test import TestCase
from .models import Team, Player, PlayerGameLog


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

    def test_game_log_str(self):
        self.assertEqual(str(self.game_log), 'Sidney Crosby - Pittsburgh Penguins vs. Test_Opponent on 2022-10-01')
