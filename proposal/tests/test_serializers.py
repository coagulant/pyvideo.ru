# coding: utf-8
from datetime import date

from django import test
from django.conf import settings

from proposal import serializers
from richard.videos.models import Category, Video, Speaker, Tag, Language


try:
    test.TestCase.assertCountEqual
except AttributeError:
    test.TestCase.assertCountEqual = test.TestCase.assertItemsEqual


class CategorySerializerTestCase(test.TestCase):

    good_values = (
        {'title': 'Foo'},
        {'title': 'Foo', 'description': 'Foo Description'},
        {'title': 'Foo', 'description': 'Foo Description', 'date': '2012-02-12'},
        {'title': 'FooBar', 'url': 'http://example.org/foobar/videos/'},
        {'title': 'Bar', 'url': 'htTPs://eXamPle.ORG/'},  # -> django.core.validators.URLValidator

        # although extra fields are validated, the values do not appear in deserialized data
        {'title': 'Foo', 'slug': None},
        {'title': 'Foo', 'slug': 'sl-ug', 'extra': 'bar', 'extra_extra': 'baz'},
    )

    bad_values = (
        'foo',
        42,
        None,
        '',
        True,

        {},  # category title must not be empty
        {'description': 'Foo Description'},  # same as above
        {'date': date(2014, 2, 23)},  # same as above
        {'title': None},  # neither None

        {'TITLE': 'Foo'},   # field names must be case insensitive
        {'TITLE': 'Foo', 'DESCRIPTION': 'Foo Description'}, 
        {'TITLE': 'Foo', 'DATE': '2013-07-22'},  # same as above
        {'TITLE': 'Foo', 'UrL': 'http://example.org/'},

        {'title': 'Foo', 'date': 'foo'}, # invalid date field value
        {'title': 'Foo', 'date': 42}, # same as above
        {'title': 'Foo', 'date': '06.07.2014'},  # same as above
        {'title': 'Foo', 'date': '2014/07/06'},  # same as above

        {'title': 'Foo', 'url': 'foo'},  # bad url,
        {'title': 'Foo', 'url': 'www.example.org'},  # no scheme,
        {'title': 'Foo', 'url': 'foo://example.org/'},  # invalid scheme
    )

    def test_known_values(self):
        for data in self.good_values:
            serializer = serializers.CategorySerializer(data=data)
            self.assertTrue(serializer.is_valid(), data)

        for data in self.bad_values:
            serializer = serializers.CategorySerializer(data=data)
            self.assertFalse(serializer.is_valid(), data)

    def test_empty_objects_are_not_valid(self):
        serializer = serializers.CategorySerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_category_title_is_sufficient(self):
        data = {'title': 'Foo'}

        serializer = serializers.CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()

        Category.objects.get(title='Foo')

    def test_existing_category_is_updated(self):
        attrs = {
            'title': 'Foo',
            'description': 'Foo Description.',
            'url': 'http://example.org/',
            'start_date': date(2013, 6, 30),
        }
        category = Category.objects.create(**attrs)

        data = {
            'title': 'Foo',
            # description is empty
            'url': 'http://example.com/',  # change url
            'date': date(2014, 5, 29),  # change date
        }

        serializer = serializers.CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()

        # refetch category
        category = Category.objects.get(pk=category.pk)

        self.assertEqual(category.title, 'Foo')
        # description is now empty
        self.assertFalse(category.description)
        self.assertEqual(category.url, 'http://example.com/')
        self.assertEqual(category.start_date, date(2014, 5, 29))

    def test_category_title_value_is_case_insensitive(self):
        attrs = {
            'title': 'FooBar',
            'description': 'FooBar Description.',
        }
        category = Category.objects.create(**attrs)

        data = {
            'title': 'foobar',
            'description': 'Descriptive FooBar Description.',
            # add url
            'url': 'http://example.org/',
        }

        serializer = serializers.CategorySerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # no extra category object was created
        self.assertEqual(Category.objects.count(), 1)

        category = Category.objects.get(pk=category.pk)

        # category name has been changed to the other case mix version
        self.assertEqual(category.title, 'foobar')
        # description was also changed
        self.assertEqual(category.description, 'Descriptive FooBar Description.')
        self.assertEqual(category.url, 'http://example.org/')

    def test_when_multiple_categories_exist_under_the_same_name_the_first_entry_is_picked(self):
        categories = [
            Category.objects.create(title='foo'),
            Category.objects.create(title='Foo'),
            Category.objects.create(title='FoO'),
            Category.objects.create(title='FOO'),
        ]

        data = {
            'title': 'Foo',
            'description': 'Foo Description.',
        }

        serializer = serializers.CategorySerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.pk, categories[0].pk)

    def test_serializer_field_names_are_case_sensitive(self):
        attrs = {
            'title': 'FooBar',
            'description': 'FooBar Description.',
            'url': 'http://example.org/',
        }
        category = Category.objects.create(**attrs)

        bad_data = {'TITLE': 'Foo'}
        good_data = {
            'title': 'FooBar',
            'description': '',
            'URL': 'http://example.com/videos/',
        }

        serializer = serializers.CategorySerializer(data=bad_data)
        self.assertFalse(serializer.is_valid())

        serializer = serializers.CategorySerializer(data=good_data)
        # although valid, invalid case field values will not be saved
        self.assertTrue(serializer.is_valid())

        serializer.save()
        category = Category.objects.get(pk=category.pk)
        # description is now empty
        self.assertFalse(category.description)
        # so is url
        self.assertFalse(category.url, '')

    def test_category_private_fields_are_not_exposed_to_public(self):
        attrs = {
            'title': 'Foo Bar',
            'slug': 'foo-bar',  # this will stay unchanged
            'whiteboard': 'My secret editor note',  # this as well
        }

        category = Category.objects.create(**attrs)

        data = {
            'title': 'Foo Bar',
            # add description
            'description': 'Foo Description.',

            # attempt to access private fields
            'slug': 'bad-slug',
            'whiteboard': 'Hacked!!!!111111',
        }

        serializer = serializers.CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        category = Category.objects.get(pk=category.pk)
        self.assertEqual(category.title, 'Foo Bar')
        # description was changed
        self.assertEqual(category.description, 'Foo Description.')
        # the private field values remain unchanged
        self.assertEqual(category.slug, 'foo-bar')
        self.assertEqual(category.whiteboard, 'My secret editor note')


class CategorySlugTestCase(test.TestCase):

    slugs = {
        'Moscow Django': 'moscow-django',
        'Разное': 'raznoe',
        'Яндекс.Events': 'iandeks-events',
        'Пайтон Митап': 'paiton-mitap',
        'Ежегодная встреча джангонавтов 2050': 'ezhegodnaia-vstrecha-dzhangonavtov-2050',
    }

    def test_categories_are_saved_with_correct_slugs(self):
        for name, slug in self.slugs.items():
            serializer = serializers.CategorySerializer(data={'title': name})

            serializer.is_valid()
            serializer.save()

            obj = Category.objects.get(pk=serializer.object.pk)
            self.assertEqual(obj.slug, slug)


class VideoSerializerKnownValues(test.TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='Baz')

    def test_good_values(self):
        good_values = (
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/'},
            {'category': self.category.pk, 'title': 'Bar', 'summary': 'Foo Bar', 'url': 'http://example.org/'},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'language': 'Russian'},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'language': 'English'},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'speakers': []},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'tags': []},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'speakers': ['Foo Bar', 'Bar Foo']},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'tags': ['foo', 'bar']},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'date': '2014-02-23'},
        )
        for data in good_values:
            serializer = serializers.VideoSerializer(data=data)
            self.assertTrue(serializer.is_valid(), 'data=%s' % data)

    def test_bad_values(self):
        bad_values = (
            # no category
            {'title': 'Foo'},
            # no title
            {'category': self.category.pk, 'title': None, 'url': 'http://example.org/'},
            {'category': self.category.pk, 'url': 'http://example.org/'},
            {'category': self.category.pk, 'title': '', 'url': 'http://example.org/'},
            # no source url
            {'title': 'Foo', 'category': self.category.pk},
            # source_url is accessed as "url"
            {'category': self.category.pk, 'title': 'Bar', 'source_url': 'http://example.org/'},
            # invalid category
            {'category': 'eggs', 'title': 'Bar', 'url': 'http://example.org/'},
            {'category': None, 'title': 'Bar', 'url': 'http://example.org/'},
            # bad field name
            {'category': self.category.pk, 'TITLE': 'Bar', 'url': 'http://example.org/'},
            # invalid language
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'language': 'Gibberish'},
            # invalid speakers
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'speakers': None},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'speakers': ''},
            # invalid tags
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'tags': None},
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'tags': ''},
            # invalid date
            {'category': self.category.pk, 'title': 'Bar', 'url': 'http://example.org/', 'date': '2014'},
            # invalid source url
            {'category': self.category.pk, 'title': 'Bar', 'url': 'example', 'date': '2014'},
        )

        for data in bad_values:
            serializer = serializers.VideoSerializer(data=data)
            self.assertFalse(serializer.is_valid(), 'data=%s' % data)


class VideoSerializerTestCase(test.TestCase):

    def setUp(self):
        self.test_category = Category.objects.create(title='Foo')

    def test_video_titles_are_case_insensitive(self):
        category = Category.objects.create(title='Foo')
        video = category.videos.create(title='Bar')

        data = {
            'category': category.pk,
            'title': 'bar',
            'description': 'New Bar Description.',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.pk, video.pk)
        # description has been updated
        self.assertEqual(Video.objects.get(pk=video.pk).description, 'New Bar Description.')

    def test_when_multiple_videos_exist_under_the_same_name_the_first_entry_is_picked(self):
        category = Category.objects.create(title='Foo')

        videos = [
            category.videos.create(title='Bar'),
            category.videos.create(title='bar'),
            category.videos.create(title='BAR'),
        ]

        data = {
            'category': category.pk,
            'title': 'BAR',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.pk, videos[0].pk)

    def test_language_field_value_is_case_insensitive(self):
        data = {
            'category': Category.objects.create(title='Moscow Django').pk,
            'title': 'Профилирование и отладка Django',
            'speakers': ['Владимир Рудных'],
            'language': 'russian',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.language.name, 'Russian')

    def test_invalid_language(self):
        data = {
            'category': Category.objects.create(title='Foo').pk,
            'title': 'Bar',
            'language': 'Gibberish',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_speakers_are_created(self):
        data = {
            'category': Category.objects.create(title='Moscow Django').pk,
            'title': 'Что нового в Django 1.5',
            'speakers': ['Илья Барышев'],
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        Speaker.objects.get(name='Илья Барышев')

    def test_existing_speakers_are_reused(self):
        speaker = Speaker.objects.create(name='Armin Ronacher')

        data = {
            'category': Category.objects.create(title='Pycon Russia 2014').pk,
            'title': 'Writing Secure APIs',
            'date': '2014-06-02',
            'speakers': ['Armin Ronacher'],
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(Speaker.objects.count(), 1)
        self.assertEqual(serializer.object.speakers.all()[0].pk, speaker.pk)

    def test_speaker_name_is_case_insensitive(self):
        Speaker.objects.create(name='Александр Козловский')
        Speaker.objects.create(name='Алексей Малашкевич')

        data = {
            'category': Category.objects.create(title='Pycon Russia 2014').pk,
            'title': 'Pony ORM - маппер нового поколения',
            'date': '2014-06-02',
            'speakers': ['Алексей Малашкевич', 'Александр Козловский'],
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # no extra speaker objects were created
        self.assertEqual(Speaker.objects.count(), 2)

        for speaker in serializer.object.speakers.all():
            self.assertTrue(speaker.name in ('Александр Козловский', 'Алексей Малашкевич'))

    def test_speaker_list_contains_unique_names(self):
        Speaker.objects.create(name='Armin Ronacher')

        data = {
            'category': Category.objects.create(title='Pycon Russia 2014').pk,
            'title': 'Writing Secure APIs',
            'date': '2014-06-02',
            'speakers': [
                'Armin Ronacher', 'Armin Ronacher', 'Armin Ronacher',
                'armin ronacher', 'armin Ronacher', 'Armin ronacher',
            ],
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # no extra speaker objects were created
        self.assertEqual(Speaker.objects.count(), 1)
        # the speakers list was trimmed down to 1 entry
        self.assertEqual(serializer.object.speakers.count(), 1)

    def test_when_speakers_list_is_emptied_the_speakers_remain_in_db(self):
        attrs = {
            'category': self.test_category,
            'title': 'На что уходит память?',
            'recorded': '2014-06-02',
            'source_url': 'http://example.org/',
        }

        self.assertEqual(Video.objects.count(), 0)

        video = Video.objects.create(**attrs)
        video.speakers = [Speaker.objects.create(name='Константин Лопухин')]

        self.assertEqual(video.speakers.count(), 1)
        self.assertEqual(Video.objects.count(), 1)

        data = {
            'category': self.test_category.pk,
            'title': 'На что уходит память?',
            'date': '2014-06-02',
            'url': 'http://example.org/',
            # speaker list is emptied
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(video.speakers.count(), 0)
        self.assertEqual(Video.objects.count(), 1)

    def test_speakers_are_saved_with_correct_slugs(self):
        speakers = {
            'Amaury Forgeot d\'Arc': 'amaury-forgeot-darc',
            'Amir Salihefendic': 'amir-salihefendic',
            'Валентин Синицын': 'valentin-sinitsyn',
            'Юрий Юревич': 'iurii-iurevich',
        }

        data = {
            'category': self.test_category.pk,
            'title': 'Bar',
            'speakers': list(speakers),
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        obj_slugs = [speaker.slug for speaker in serializer.object.speakers.all()]
        self.assertCountEqual(obj_slugs, list(speakers.values()))

    def test_video_tags_are_saved_lowercase(self):
        data = {
            'category': self.test_category.pk,
            'title': 'Bar',
            'tags': ['baz', 'BAR', 'haM'],
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        obj_tags = [tag.tag for tag in serializer.object.tags.all()]

        self.assertCountEqual(obj_tags, ['baz', 'bar', 'ham'])

    def test_video_tag_list_is_unique(self):
        data = {
            'category': self.test_category.pk,
            'title': 'Bar',
            'tags': ['baz', 'baz', 'BaZ', 'BAZ', 'BAZ', 'foo'],
            'url': 'http://example.org/',
        }
        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        obj_tags = [tag.tag for tag in serializer.object.tags.all()]
        self.assertCountEqual(obj_tags, ['baz', 'foo'])


    def test_video_tags_are_replaced_properly(self):
        attrs = {
            'category': self.test_category,
            'title': 'Jinja2 в Django',
            'recorded': '2013-12-09',
        }

        video = Video.objects.create(**attrs)
        video.tags = [Tag.objects.create(tag='foo'), Tag.objects.create(tag='jinja2')]

        obj_tags = [tag.tag for tag in video.tags.all()]
        self.assertCountEqual(obj_tags, ['foo', 'jinja2'])

        data = {
            'category': self.test_category.pk,
            'title': 'Jinja2 в Django',
            'date': '2013-12-09',
            'url': 'http://example.org/',
            'tags': ['Jinja2', 'django', 'templates']  # foo has been removed
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        self.assertFalse(serializer.errors)
        serializer.save()

        obj_tags = [tag.tag for tag in video.tags.all()]
        self.assertCountEqual(obj_tags, ['jinja2', 'django', 'templates'])

    def test_when_video_tag_list_emptied_the_tags_remain_in_db(self):
        attrs = {
            'category': self.test_category,
            'title': 'Foo',
            'source_url': 'http://example.org/',
        }
        video = Video.objects.create(**attrs)
        video.tags = [Tag.objects.create(tag='foo'), Tag.objects.create(tag='bar')]

        self.assertEqual(video.tags.count(), 2)
        self.assertEqual(Tag.objects.count(), 2)

        data = {
            'category': self.test_category.pk,
            'title': 'Foo',
            'url': 'http://example.org/',
            'tags': [],
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(serializer.object.pk, video.pk)

        self.assertEqual(video.tags.count(), 0)
        self.assertEqual(Tag.objects.count(), 2)

    def test_video_model_slug_is_not_editable(self):
        attrs = {
            'category': self.test_category,
            'title': 'Foo Bar Ham 2014',
            'description': 'Foo Description',
            'source_url': 'http://example.org/',
        }
        video = Video.objects.create(**attrs)

        self.assertEqual(video.slug, 'foo-bar-ham-2014')

        data = {
            'category': self.test_category.pk,
            'title': 'Foo Bar Ham 2014',
            'description': 'Foo Bar Ham 2014 Description',
            'slug': 'manually-inserted-slug',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # ensure this is the same object
        self.assertEqual(serializer.object.pk, video.pk)


        video = Video.objects.get(pk=video.pk)
        # ensure description has been updated
        self.assertEqual(video.description, 'Foo Bar Ham 2014 Description')
        # while the slug has not
        self.assertEqual(video.slug, 'foo-bar-ham-2014')

    def test_video_private_fields_are_not_exposed_to_public(self):
        attrs = {
            'category': self.test_category,
            'title': 'Foo',
            'source_url': 'http://example.org/',
            'embed': '<iframe src="http://example.org/"></iframe>',
            'thumbnail_url': 'http://example.org/thumnail.png',
        }
        video = Video.objects.create(**attrs)

        data = {
            'category': self.test_category.pk,
            'title': 'Foo',
            'url': 'http://example.org/',

            # attempt to alter public fields
            'summary': 'Foo Bar',
            'description': 'Foo Description',

            # attempt to alter private fields
            'embed': '<iframe src="http://malicious.site/"></iframe>',
            'thumbnail_url': 'http://malicious.site/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        video = Video.objects.get(pk=video.pk)

        # public field values have been changed
        self.assertEqual(video.description, 'Foo Description')
        self.assertEqual(video.summary, 'Foo Bar')

        # private fileds have not not
        self.assertEqual(video.embed, '<iframe src="http://example.org/"></iframe>')
        self.assertEqual(video.thumbnail_url, 'http://example.org/thumnail.png')

    def test_new_video_is_saved_as_draft(self):
        data = {
            'category': self.test_category.pk,
            'title': 'Foo',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        video = Video.objects.get(pk=serializer.object.pk)

        self.assertEqual(video.state, Video.STATE_DRAFT)

    def test_updating_existing_video_url_makes_the_video_a_draft(self):
        attrs = {
            'category': self.test_category,
            'title': 'Foo',
            'source_url': 'http://example.org/',
            'state': Video.STATE_LIVE,
            'embed': '<iframe src="http://example.org/"></iframe>'
        }
        video = Video.objects.create(**attrs)

        # the video is live
        self.assertEqual(Video.objects.get(pk=video.pk).state, Video.STATE_LIVE)

        data = {
            'category': self.test_category.pk,
            'title': 'Foo',
            'url': 'http://example.com/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        video = Video.objects.get(pk=video.pk)
        self.assertEqual(video.embed, '')
        # the video is now draft
        self.assertEqual(video.state, Video.STATE_DRAFT)


class OptionalVideoLanguageTestCase(test.TestCase):

    def test_language_is_optional_the_default_value_is_assumed(self):
        data = {
            'category': Category.objects.create(title='Foo Category').pk,
            'title': 'Foo',
            'url': 'http://example.org/',
        }

        serializer = serializers.VideoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        obj_lang = serializer.object.language

        lang_name, lang_iso = settings.PROPOSAL_LANGUAGE

        self.assertEqual(obj_lang.name, lang_name)
        self.assertEqual(obj_lang.iso639_1, lang_iso)
