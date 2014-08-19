# coding: utf-8
import os
import socket

from django.conf import settings
from richard.videos import utils, models
from slugify import slugify
from embedly import Embedly


# monkey patch richard.videos.utils.slugify so it handles all unicode characters
utils.slugify = slugify


def fetch_embed(self, client=None):
    """
    Update the embed data fields (embed and thumbnail_url) using embedly.

    :param client: Embedly instance
    :return:
    """
    if not 'EMBEDLY_KEY' in os.environ:
        return
    client = client or Embedly(key=os.environ['EMBEDLY_KEY'], timeout=settings.EMBEDLY_TIMEOUT)
    try:
        data = client.oembed(self.source_url).data
    except socket.timeout:
        return
    # check for errors
    if data['type'] not in ('video',):
        return
    self.embed = data['html']
    self.thumbnail_url = data.get('thumbnail_url', None)

# patch the Video model
models.Video.fetch_embed = fetch_embed


# register signals
from . import signals
