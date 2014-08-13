# coding: utf-8
from django.core.management import BaseCommand
from django.conf import settings
from django.db import transaction

from proposal.parsers import videos


class Command(BaseCommand):
    help = 'Performs a video proposal review'

    def handle(self, *args, **options):
        with transaction.atomic():
            for video in videos(settings.PROPOSAL_ROOT):
                self.stdout.write(u'%s %s' %
                    ('Updating' if video.object.pk else 'Adding', video.object.title)
                )
                video.save()
