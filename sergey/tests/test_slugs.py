# coding: utf-8
from __future__ import unicode_literals

from django import test

from richard.videos.models import Category, Video, Speaker


class CategorySlugTestCase(test.TestCase):

    slugs = (
        ('Boston Python Meetup', 'boston-python-meetup'),
        ('Chicago Djangonauts', 'chicago-djangonauts'),
        ('DjangoCon 2012', 'djangocon-2012'),
        ('DjangoCon AU 2013', 'djangocon-au-2013'),
        ('EuroPython 2011', 'europython-2011'),
        ('Kiwi PyCon 2009', 'kiwi-pycon-2009'),

        ('Computer Science Center', 'computer-science-center'),
        ('DUMP', 'dump'),
        ('EkbPy 2012', 'ekbpy-2012'),
        ('Разное', 'raznoe'),
        ('Яндекс.Events', 'iandeks-events'),

        ('PYCON AUSTRALIA NATIONAL CONFERENCE', 'pycon-australia-national-conference'),

        ('Пайтон Митап', 'paiton-mitap'),
        ('Ежегодная встреча джангонавтов 2050', 'ezhegodnaia-vstrecha-dzhangonavtov-2050'),

        ('Associação Python Brasil', 'associacao-python-brasil'),
    )

    def test_known_values(self):
        for title, slug in self.slugs:
            category = Category.objects.create(title=title)
            self.assertEqual(Category.objects.get(pk=category.pk).slug, slug)

    def test_category_slug_field_values_are_enforced_to_be_unique(self):
        category = Category.objects.create(title='Foo Bar')
        self.assertEqual(Category.objects.get(pk=category.pk).slug, 'foo-bar')

        category = Category.objects.create(title='Foo  Bar')
        self.assertEqual(Category.objects.get(pk=category.pk).slug, 'foo-bar-0')

        category = Category.objects.create(title='Foo   Bar')
        self.assertEqual(Category.objects.get(pk=category.pk).slug, 'foo-bar-1')


class SpeakerSlugTestCase(test.TestCase):

    slugs = (
        ('Amaury Forgeot d\'Arc', 'amaury-forgeot-darc'),
        ('Amir Salihefendic', 'amir-salihefendic'),
        ('Andrew Godwin', 'andrew-godwin'),
        ('Dr. Russell Keith-Magee', 'dr-russell-keith-magee'),
        ('Hall A day 2', 'hall-a-day-2'),
        ('Łukasz Langa', 'lukasz-langa'),
        ('Александр Будкарь', 'aleksandr-budkar'),
        ('Александр Соловьев', 'aleksandr-solovev'),
        ('Алексей Кирпичников', 'aleksei-kirpichnikov'),
        ('Андрей Попп', 'andrei-popp'),
        ('Артем Безукладичный', 'artem-bezukladichnyi'),
        ('Валентин Синицын', 'valentin-sinitsyn'),
        ('Илья Барышев', 'ilia-baryshev'),
        ('Илья Биин', 'ilia-biin'),
        ('Илья Глуховский', 'ilia-glukhovskii'),
        ('Юрий Юревич', 'iurii-iurevich'),

        # borrowed from http://pyvideo.org/api/v2/speaker/
        ('Aaron O\'Mullan', 'aaron-omullan'),
        ('Achiel van der Mandele', 'achiel-van-der-mandele'),
        ('Adam T. Lindsay', 'adam-t-lindsay'),
        ('Adrian Holovaty', 'adrian-holovaty'),
        ('A. Jesse Jiryu Davis', 'a-jesse-jiryu-davis'),
        ('Alan Barber II', 'alan-barber-ii'),
        ('Albert O\'Connor', 'albert-oconnor'),
        ('Alex DeCaria', 'alex-decaria'),
        ('Gavin M. Roy', 'gavin-m-roy'),
        ('G. Clifford Williams', 'g-clifford-williams'),
        ('Godfrey Ejroghene Akpojotor', 'godfrey-ejroghene-akpojotor'),
        ('Gökhan Sever', 'gokhan-sever'),
        ('H Krosing', 'h-krosing'),
        ('Jon Åslund', 'jon-aslund'),
        ('J Page', 'j-page'),
        ('Robert E Brewer', 'robert-e-brewer'),
        ('Russell Keith-Magee', 'russell-keith-magee'),
    )

    def test_known_values(self):
        for name, slug in self.slugs:
            speaker = Speaker.objects.create(name=name)
            self.assertEqual(Speaker.objects.get(pk=speaker.pk).slug, slug)

    def test_speaker_slug_field_values_are_enforced_to_be_unique(self):
        speaker = Speaker.objects.create(name='Foo Bar Ham')
        self.assertEqual(Speaker.objects.get(pk=speaker.pk).slug, 'foo-bar-ham')

        speaker = Speaker.objects.create(name='Foo-Bar Ham')
        self.assertEqual(Speaker.objects.get(pk=speaker.pk).slug, 'foo-bar-ham-0')

        speaker = Speaker.objects.create(name='Foo-Bar-Ham')
        self.assertEqual(Speaker.objects.get(pk=speaker.pk).slug, 'foo-bar-ham-1')


class VideoSlugTestCase(test.TestCase):

    slugs = (
        ('Lighting Talks Андрей Светлов',
            'lighting-talks-andrei-svetlov'),

        ('На что уходит память?',
            'na-chto-ukhodit-pamiat'),

        ('Auto scaling on the Cloud the right way',
            'auto-scaling-on-the-cloud-the-right-way'),

        ('Lightning talks 1',
            'lightning-talks-1'),

        ('Pony ORM - маппер нового поколения',
            'pony-orm-mapper-novogo-pokoleniia'),

        ('Python-разработка в части Яндекс-вселенной',
            'python-razrabotka-v-chasti-iandeks-vselennoi'),

        ('Как писать для asyncio',
            'kak-pisat-dlia-asyncio'),

        ('Нагрузочное тестирование с помощью Яндекс.Танка',
            'nagruzochnoe-testirovanie-s-pomoshchiu-iandeks-tanka'),

        ('Почему Python нужен (был) свой underscore',
            'pochemu-python-nuzhen-byl-svoi-underscore'),

        ('Pathlib. Маленькие вкусности Python 3.4',
            'pathlib-malenkie-vkusnosti-python-3-4'),

        ('Unittesting. Как?',
            'unittesting-kak'),

        ('Redis. Как мы боролись со сложностью',
            'redis-kak-my-borolis-so-slozhnostiu'),

        ('Обзор фреймворка Twisted',
            'obzor-freimvorka-twisted'),

        ('Работаем с RabbitMQ в Python используя kombu + gevent',
            'rabotaem-s-rabbitmq-v-python-ispolzuia-kombu-ge'),

        ('Асинхронное распределенное выполнение задач. Stdlib, Celery, RQ и собственные велосипеды',
            'asinkhronnoe-raspredelennoe-vypolnenie-zadach-stdl'),

        ('Введение в GIL и новый GIL',
            'vvedenie-v-gil-i-novyi-gil'),

        ('Django 1.6',
            'django-1-6'),

        ('The Best of LinuxCon Europe 2013 (imho)﻿',
            'the-best-of-linuxcon-europe-2013-imho'),

        ('"Внутренности" CPython, часть II',
            'vnutrennosti-cpython-chast-ii'),

        ('Django 1.6 and beyond: The Django Roadmap',
            'django-1-6-and-beyond-the-django-roadmap'),

        ('Lighting Talks #2',
            'lighting-talks-2'),

        ('Redis, the hacker\'s database',
            'redis-the-hackers-database'),

        ('Anatomy of Matplotlib - Part 1',
            'anatomy-of-matplotlib-part-1'),

        ('Anatomy of Matplotlib - Part 2',
            'anatomy-of-matplotlib-part-2'),

        ('Anatomy of Matplotlib - Part 3',
            'anatomy-of-matplotlib-part-3'),

        ('Astropy and astronomical tools Part I',
            'astropy-and-astronomical-tools-part-i'),

        ('Bayesian Statistical Analysis using Python - Part 1',
            'bayesian-statistical-analysis-using-python-part'),

        ('Bayesian Statistical Analysis using Python - Part 2',
            'bayesian-statistical-analysis-using-python-part-0'),

        ('Bayesian Statistical Analysis using Python - Part 3',
            'bayesian-statistical-analysis-using-python-part-1'),

        ('Geospatial data in Python: Database, Desktop, and the Web part 1',
            'geospatial-data-in-python-database-desktop-and'),

        ('Geospatial data in Python: Database, Desktop, and the Web part 2',
            'geospatial-data-in-python-database-desktop-and-0'),

        ('Geospatial data in Python: Database, Desktop and the Web - Part 3',
            'geospatial-data-in-python-database-desktop-and-1'),

        ('HDF5 is for Lovers, Tutorial part 1',
            'hdf5-is-for-lovers-tutorial-part-1'),
    )

    def setUp(self):
        self.category = Category.objects.create(title='Foo')

    def test_known_values(self):
        for title, slug in self.slugs:
            video = self.category.video_set.create(title=title)
            self.assertEqual(Video.objects.get(pk=video.pk).slug, slug)

    def test_video_slugs_are_enforced_to_be_unique(self):
        video = self.category.video_set.create(title='Foo Bar in Baz')
        self.assertEqual(Video.objects.get(pk=video.pk).slug, 'foo-bar-in-baz')

        video = self.category.video_set.create(title='Foo  Bar  in  Baz')
        self.assertEqual(Video.objects.get(pk=video.pk).slug, 'foo-bar-in-baz-0')

        video = self.category.video_set.create(title='Foo-Bar-in-Baz')
        self.assertEqual(Video.objects.get(pk=video.pk).slug, 'foo-bar-in-baz-1')
