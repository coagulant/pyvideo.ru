# coding: utf-8
from django.contrib import admin
from richard.videos.models import Speaker


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