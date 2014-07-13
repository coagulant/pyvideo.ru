# coding: utf-8
from django.core.management import BaseCommand
from django.template.defaultfilters import slugify
from unidecode import unidecode

from richard.videos.models import Speaker


class Command(BaseCommand):
    help = 'Fixes speaker slugs'

    def handle(self, *args, **options):

        for speaker in Speaker.objects.all():
            old_slug = speaker.slug
            fixed_slug = slugify(unidecode(speaker.name))
            speaker.save()
            self.stdout.write(u'Changed slug for %s "%s" => %s\n' % (speaker.name, old_slug, fixed_slug))
