# coding: utf-8
import os

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Q
from embedly import Embedly

from richard.videos.models import Video


class Command(BaseCommand):
    help = 'Populates embed data for draft videos'

    def handle(self, *args, **options):
        client = Embedly(key=os.environ.get('EMBEDLY_KEY'), timeout=settings.EMBEDLY_TIMEOUT)

        qs = (Video.objects
            # skip source-less videos
            .filter(
                ~Q(source_url='') & ~Q(source_url__isnull=True)
            )
            .filter(
                # attempt to obtain embed code for videos
                Q(embed='') |
                # or fix youtube videos with broken embed code
                (Q(source_url__contains='youtube.com') & ~Q(embed__contains='embed'))
            )
        )

        for video in qs:
            video.fetch_embed(client=client)
            video.save()
            self.stdout.write(u'Updated %s' % video.title)
