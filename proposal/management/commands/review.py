# coding: utf-8
from django.core.management import BaseCommand
from django.conf import settings
from django.db import transaction

from proposal.parsers import videos
from proposal.exceptions import ProposalError


class Command(BaseCommand):
    help = 'Performs a video proposal review'

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                for video in videos(settings.PROPOSAL_ROOT):
                    self.stdout.write(u'%s %s' %
                        ('Updating' if video.object.pk else 'Adding', video.object.title)
                    )
                    video.save()
            # display exception details
            except ProposalError as e:
                for cls, msg in e.args[0]:
                    self.stdout.write('%s - %s' % (cls.__name__, msg))
                raise
