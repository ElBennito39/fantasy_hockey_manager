from django.core.management.base import CommandError, BaseCommand
from goal_predictor.apiNHL import populate_players

class Command(BaseCommand):
    help = 'Populate NHL players'

    def handle(self, *args, **kwargs):
        populate_players()
        self.stdout.write(self.style.SUCCESS('Players populated successfully'))
