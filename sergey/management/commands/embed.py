# coding: utf-8
import os

from django.core.management import BaseCommand
from django.db.models import Q
from embedly import Embedly

from richard.videos.models import Video


class Command(BaseCommand):
    help = 'Populates emded data for draft videos'

    def handle(self, *args, **options):
        client = Embedly(key=os.environ.get('EMBEDLY_KEY'))

        qs = (Video.objects
            # skip source-less videos
            .filter(
                ~Q(source_url='') & ~Q(source_url__isnull=True)
            )
            # attempt to fix either draft videos
            # or youtube videos with broken emded code
            .filter(
                Q(state=Video.STATE_DRAFT) |
                (Q(source_url__contains='youtube.com') & ~Q(embed__contains='embed'))
            )
        )

        for video in qs:
            data = client.oembed(video.source_url).data
            # check for errors
            if data['type'] not in ('video',):
                continue
            video.embed = data['html']
            video.thumbnail_url = data.get('thumbnail_url', None)
            video.state = Video.STATE_LIVE
            video.save()
            self.stdout.write(u'Updated %s' % video.title)
