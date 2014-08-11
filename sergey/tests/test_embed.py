# coding: utf-8
from django import test
from django.core.management import call_command
from embedly.models import Url
from embedly.client import Embedly
from unittest.mock import patch

from richard.videos.models import Category, Video


class EmbedCommandTestCase(test.TestCase):

    def setUp(self):
        self.test_category = Category.objects.create(title='Foo')

    @patch.object(Embedly, 'oembed')
    def test_draft_video_is_embedded(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'foo'})

        video = self.test_category.videos.create(
            title='Foo Video',
            state=Video.STATE_DRAFT,
            source_url='http://example.org/',
        )

        call_command('embed')
        self.assertEqual(Video.objects.get(pk=video.pk).embed, 'foo')

    @patch.object(Embedly, 'oembed')
    def test_draft_video_become_live_when_embedded(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'foo'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_DRAFT,
            'source_url': 'http://example.org/',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        self.assertEqual(Video.objects.get(pk=video.pk).state, Video.STATE_LIVE)

    @patch.object(Embedly, 'oembed')
    def test_draft_video_with_no_source_url_is_not_processed(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'foo'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_DRAFT,
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        video = Video.objects.get(pk=video.pk)
        self.assertEqual(video.state, Video.STATE_DRAFT)
        self.assertEqual(video.embed, '')

    @patch.object(Embedly, 'oembed')
    def test_draft_video_is_not_processed_on_embedly_failure(self, mock):
        mock.return_value = Url(data={'type': 'error', 'html': 'foo'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_DRAFT,
            'source_url': 'http://example.org',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        video = Video.objects.get(pk=video.pk)
        self.assertEqual(video.state, Video.STATE_DRAFT)
        self.assertEqual(video.embed, '')

    @patch.object(Embedly, 'oembed')
    def test_draft_video_is_embedded_despite_being_populated(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'foo'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_DRAFT,
            'source_url': 'http://example.org/',
            'embed': '<iframe src="http://example.org/"></iframe>',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        # the embed field value hasnt been changed
        self.assertEqual(Video.objects.get(pk=video.pk).embed, 'foo')

    @patch.object(Embedly, 'oembed')
    def test_draft_video_is_updated_with_thumbnail_picture(self, mock):
        mock_data = {
            'type': 'video',
            'thumbnail_url': 'http://example.org/picture.jpg',
            'html': 'foo',
        }
        mock.return_value = Url(data=mock_data)

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_DRAFT,
            'source_url': 'http://example.org/',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        self.assertEqual(
            Video.objects.get(pk=video.pk).thumbnail_url,
            'http://example.org/picture.jpg'
        )

    @patch.object(Embedly, 'oembed')
    def test_youtube_videos_with_broken_embed_code_are_fixed(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'fixed'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_LIVE,
            'source_url': 'http://youtube.com/watch?v=AiN71',
            'embed': 'broken',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        self.assertEqual(Video.objects.get(pk=video.pk).embed, 'fixed')

    @patch.object(Embedly, 'oembed')
    def test_youtube_videos_with_proper_embed_code_are_not_affected(self, mock):
        mock.return_value = Url(data={'type': 'video', 'html': 'fixed'})

        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_LIVE,
            'source_url': 'http://youtube.com/watch?v=AiN71',
            'embed': '<iframe src="http://youtube.com/embed/AiN71"></iframe>',
        }
        video = self.test_category.videos.create(**attrs)

        call_command('embed')

        self.assertEqual(
            Video.objects.get(pk=video.pk).embed,
            '<iframe src="http://youtube.com/embed/AiN71"></iframe>'
        )


class VideoEmbedDataTestCase(test.TestCase):

    def setUp(self):
        self.test_category = Category.objects.create(title='Foo Category')

    def test_video_embed_data_is_void_on_source_url_change(self):
        attrs = {
            'title': 'Foo Video',
            'source_url': 'http://example.org/',
            'embed': '<iframe src="http://example.org/"></iframe>',
            'thumbnail_url': 'http://example.org/picture.jpg',
        }
        video = self.test_category.videos.create(**attrs)

        self.assertEqual(video.embed, attrs['embed'])
        self.assertEqual(video.thumbnail_url, attrs['thumbnail_url'])

        video.source_url = 'http://example.com/'
        video.save()

        self.assertEqual(video.embed, '')
        self.assertEqual(video.thumbnail_url, '')

    def test_video_embed_data_is_kept_if_source_url_is_not_changed(self):
        attrs = {
            'title': 'Foo Video',
            'source_url': 'http://example.org/',
            'embed': '<iframe src="http://example.org/"></iframe>',
            'thumbnail_url': 'http://example.org/picture.jpg',
        }
        video = self.test_category.videos.create(**attrs)

        self.assertEqual(video.embed, attrs['embed'])
        self.assertEqual(video.thumbnail_url, attrs['thumbnail_url'])

        video.title = 'Bar Video'
        video.save()

        self.assertEqual(video.embed, attrs['embed'])
        self.assertEqual(video.thumbnail_url, attrs['thumbnail_url'])


    def test_saving_live_video_with_no_embed_data_makes_it_draft(self):
        attrs = {
            'title': 'Foo Video',
            'state': Video.STATE_LIVE,
            'source_url': 'http://example.org/',
        }
        video = self.test_category.videos.create(**attrs)

        self.assertEqual(Video.objects.get(pk=video.pk).state, Video.STATE_DRAFT)
