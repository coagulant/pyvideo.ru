# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        orm['videos.Language'].objects.bulk_create([
            orm['videos.Language'](name='English', iso639_1='en'),
            orm['videos.Language'](name='Russian', iso639_1='ru'),
        ])

    def backwards(self, orm):
        orm['videos.Language'].objects.filter(name__in=['English', 'Russian']).delete()

    models = {
        'videos.category': {
            'Meta': {'object_name': 'Category', 'ordering': "['title']"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'default': "''"}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'videos.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso639_1': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'videos.relatedurl': {
            'Meta': {'object_name': 'RelatedUrl'},
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Video']", 'related_name': "'related_urls'"})
        },
        'videos.speaker': {
            'Meta': {'object_name': 'Speaker', 'ordering': "['name']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'videos.tag': {
            'Meta': {'object_name': 'Tag', 'ordering': "['tag']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'videos.video': {
            'Meta': {'object_name': 'Video', 'ordering': "['-recorded', 'title']"},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Category']", 'related_name': "'videos'"}),
            'copyright_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'embed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Language']", 'null': 'True'}),
            'quality_notes': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'recorded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'source_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['videos.Speaker']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'videos'"}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['videos.Tag']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'videos'"}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'video_flv_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_flv_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_flv_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'video_mp4_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_mp4_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_mp4_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'video_ogv_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_ogv_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_ogv_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'video_webm_download_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_webm_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_webm_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'whiteboard': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'videos.videourlstatus': {
            'Meta': {'object_name': 'VideoUrlStatus'},
            'check_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'status_message': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Video']"})
        }
    }

    complete_apps = ['videos', 'sergey']
    symmetrical = True
    depends_on = (
        ('videos', '0004_auto__add_language__add_field_video_language'),
    )
