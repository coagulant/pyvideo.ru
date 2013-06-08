# coding: utf-8
from django.contrib import admin
from richard.videos.admin import VideoAdmin
from richard.videos.models import Speaker, Video


class SpeakerAdmin(admin.ModelAdmin):
    list_display_links = ('link',)
    list_display = ('link', 'name', 'slug')
    list_editable = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def link(self, obj):
        return obj.name


admin.site.unregister(Speaker)
admin.site.register(Speaker, SpeakerAdmin)


class PyVideoAdmin(VideoAdmin):
    list_display = ('title', 'category', 'speakers_string', 'whiteboard', 'state')

    def speakers_string(self, obj):
        return u', '.join(obj.speakers.values_list('name', flat=True))


admin.site.unregister(Video)
admin.site.register(Video, PyVideoAdmin)
