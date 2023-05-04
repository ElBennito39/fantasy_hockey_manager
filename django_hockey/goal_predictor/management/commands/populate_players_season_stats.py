from django.core.management.base import CommandError, BaseCommand
from goal_predictor.apiNHL import populate_player_season_stats

class Command(BaseCommand):
    help = 'Populate NHL players single season stats'

    def handle(self, *args, **kwargs):
        populate_player_season_stats()
        self.stdout.write(self.style.SUCCESS('Players single season stats populated successfully'))
