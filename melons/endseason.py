from django.core.management.base import BaseCommand
from .models import Profile


class Command(BaseCommand):
    def handle(self, per=0.8, *args, **options):
        for p in Profile.objects.all():
            p.score = p.score*per
            p.save()
        print("Done!")