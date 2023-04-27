from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Team, Player, PlayerGameLog

#auto generated tests for Models..
class ModelTestCase(TestCase):
    def setUp(self):
        # Create some test data
        self.team = Team.objects.create(name='Test Team')
        self.player = Player.objects.create(
            nhl_id=1111111,
            name='Test Player',
            position='C',
            team=self.team,
            season='20222023'
        )
        self.game_log = PlayerGameLog.objects.create(
            player=self.player,
            season='20222023',
            assists=1,
            goals=1,
            pim=0,
            shots=2,
            games=1,
            hits=0,
            power_play_goals=0,
            power_play_points=0,
            even_time_on_ice='16:31',
            penalty_minutes=0,
            faceOffPct=None,
            shotPct=50.0,
            gameWinningGoals=0,
            overTimeGoals=0,
            shortHandedGoals=0,
            shortHandedPoints=0,
            shortHandedTimeOnIce='01:02',
            blocked=1,
            plusMinus=0,
            points=2,
            shifts=0
        )

    def test_team_creation(self):
        # Test if the team was created successfully
        team = Team.objects.get(name='Test Team')
        self.assertEqual(team.name, 'Test Team')

    def test_player_creation(self):
        # Test if the player was created successfully
        player = Player.objects.get(nhl_id=1234)
        self.assertEqual(player.name, 'Test Player')

    def test_game_log_creation(self):
        # Test if the game log was created successfully
        game_log = PlayerGameLog.objects.get(player=self.player)
        self.assertEqual(game_log.games, 1)
