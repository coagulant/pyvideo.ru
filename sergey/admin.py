# coding: utf-8
from django.contrib import admin
from richard.videos.admin import VideoAdmin, SpeakerAdmin
from richard.videos.models import Speaker, Video


class PySpeakerAdmin(SpeakerAdmin):
    list_display_links = ('link',)
    list_display = ('link', 'name', 'slug')
    list_editable = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def link(self, obj):
        return obj.name


admin.site.unregister(Speaker)
admin.site.register(Speaker, PySpeakerAdmin)


class PyVideoAdmin(VideoAdmin):
    list_display = ('title', 'category', 'tags_string', 'speakers_string', 'whiteboard', 'state')
    list_editable = ('whiteboard',)
    search_fields = ('title', 'slug')
    ordering = ('-updated',)
    fields = ('title', 'slug', 'tags', 'description', 'category', 'speakers',
              'language', 'source_url', 'embed', 'thumbnail_url', 'duration',
              'recorded', 'state')

    def tags_string(self, obj):
        return u', '.join(obj.tags.values_list('tag', flat=True))

    def speakers_string(self, obj):
        return u', '.join(obj.speakers.values_list('name', flat=True))


admin.site.unregister(Video)
admin.site.register(Video, PyVideoAdmin)
