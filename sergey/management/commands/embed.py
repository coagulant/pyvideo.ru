# coding: utf-8
import os
from django.core.management import BaseCommand
from embedly import Embedly
from richard.videos.models import Video


class Command(BaseCommand):
    help = 'Fixes embed for youtube videos'

    def handle(self, *args, **options):

        client = Embedly(key=os.environ.get('EMBEDLY_KEY'))

        for video in Video.objects.all():
            if video.source_url.startswith('http://www.youtube') and 'embed' not in video.embed:
                data = client.oembed(video.source_url).data
                video.embed = data['html']
                video.save()
                self.stdout.write(u'Updated %s' % video.title)