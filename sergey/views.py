# coding: utf-8
from django.db.models import Count
from django.views.generic import ListView
from richard.videos.models import Speaker


class SpeakerList(ListView):
    template_name = 'videos/speaker_list.html'
    context_object_name = 'speakers'
    queryset = Speaker.objects.annotate(video_count=Count('videos'))
