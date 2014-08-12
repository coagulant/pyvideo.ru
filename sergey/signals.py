# coding: utf-8
from django.dispatch import receiver
from django.db.models.signals import pre_save

from richard.videos.models import Video


@receiver(pre_save, sender=Video)
def void_embed_data_on_source_url_change(sender, instance, raw, **kwargs):
    """
    Attempt to void video embed data on a source url change.

    :param sender: ``richard.videos.models.Video``
    :param instance: ``richard.videos.models.Video`` instance
    """
    # the instance is about to be created, skip it
    if not instance.pk or raw:
        return
    old = Video.objects.get(pk=instance.pk)
    # only empty data if the url has actually been changed
    if instance.source_url != old.source_url:
        # void embed details
        if instance.embed == old.embed:
            instance.embed = ''
            instance.thumbnail_url = ''


@receiver(pre_save, sender=Video)
def force_video_draft_state(sender, instance, raw, **kwargs):
    """
    Change video state to draft if it's about to saved with no embed data.

    :param sender: ``richard.videos.models.Video``
    :param instance: ``richard.videos.models.Video`` instance
    """
    if instance.source_url and not instance.embed and not raw:
        instance.state = Video.STATE_DRAFT
