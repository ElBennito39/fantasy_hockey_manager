from django.core.management.base import CommandError, BaseCommand
from goal_predictor.apiNHL import populate_teams

class Command(BaseCommand):
    help = 'Populate NHL teams'

    def handle(self, *args, **kwargs):
        populate_teams()
        self.stdout.write(self.style.SUCCESS('Teams populated successfully'))
