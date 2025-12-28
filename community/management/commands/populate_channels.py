from django.core.management.base import BaseCommand
from community.models import Channel

class Command(BaseCommand):
    help = 'Populates default community channels'

    def handle(self, *args, **kwargs):
        channels = [
            {'name': 'general', 'slug': 'general', 'desc': 'General discussion'},
            {'name': 'announcements', 'slug': 'announcements', 'desc': 'News and updates'},
            {'name': 'help-python', 'slug': 'help-python', 'desc': 'Python help and support'},
            {'name': 'project-showcase', 'slug': 'project-showcase', 'desc': 'Show off your work'},
        ]

        for c in channels:
            obj, created = Channel.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['desc']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created channel: {c["name"]}'))
            else:
                self.stdout.write(f'Channel already exists: {c["name"]}')
