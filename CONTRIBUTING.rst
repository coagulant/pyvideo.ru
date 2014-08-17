Video requirements
------------------

* russian language
* can be embeded
* title and description
* somewhat of a good quality, both recording and materials


Proposing new videos
--------------------

1. Fork the project
2. Navigate to the ``drafts/<category>`` directory

   If necessary define a new category:

   a. Create a directory for the new category

        The directory name is not vital, but it would be nice if you kept it sensible.
        For instance, **drafts/moscowdjango** looks like a well named directory.

   b. Inside the new directory create a file named ``category.[yaml|json|xml]``

   c. Describe the category object using the following fields: **title**, **description**, **date** and **url**.

        The only required field is **title** though.


   Suppose we wanted to create a category for `Moscow Django <http://moscowdjango.ru/>`_ (monthly django developers meetup in Moscow).
   To do so, we would describe the category in ``drafts/moscowdjango/category.yaml`` using YAML:

   ::

        title: MoscowDjango
        description: |
            Moscow Django Meetup — это ежемесячные встречи разработчиков на Джанго.

            Несколько человек выступают перед публикой с докладами, так или иначе связанными с веб-разработкой, Python и Django.
            Не обходится и без самого интересного: общения в кулуарах.

            Благодаря организаторам, встречи проходят в тёплой компании проектора и вай-фая. Следующий митап пройдёт в офисе Mail.ru Group.

            Для тех, кто не может приехать, мы будем стараться проводить онлайн-трансляции и выкладывать видео-записи выступлений.

            Участие во встречах бесплатное, надо только зарегистрироваться на событие.
        url: http://moscowdjango.ru/

3. Add files that describe the proposed videos using either of the formats: yaml, json or xml.

     The way you name the video files is entirely up to you,
     but that would be great if the file names were describing their contents.

   A video object is described with the following fields:

   +---------------+-------------------------------+
   | Field name    | Field description             |
   +===============+===============================+
   | title         | Title                         |
   +---------------+-------------------------------+
   | description   | Description                   |
   +---------------+-------------------------------+
   | summary       | Brief summary                 |
   +---------------+-------------------------------+
   | url           | Source URL                    |
   +---------------+-------------------------------+
   | language      | Language                      |
   +---------------+-------------------------------+
   | date          | Date the video was recorded   |
   +---------------+-------------------------------+
   | speakers      | List of speaker names         |
   +---------------+-------------------------------+
   | tags          | List of tags                  |
   +---------------+-------------------------------+

     The only required fields are **title** and **url**.

   For instance, if you had to add a video about a new django release you would
   probably describe the video in ``drafts/moscowdjango/django_16.yaml``:

   ::

        title: Django 1.6
        url: http://www.youtube.com/watch?v=AhmjPTrdgGM
        summary: Обзор нового релиза Django 1.6
        description: |
          Обзор нового релиза Django 1.6 и небольшое превью миграций в 1.7

          http://moscowdjango.ru/meetup/15/django-16/
        date: 2013-12-12
        speakers:
            - Илья Барышев
        tags:
            - moscowdjango
            - django

4. Create a pull request.

Now that we are aware of your proposal, it may take some time for us to review it.
If everything is well, the proposed videos will appear at the `website <http://pyvideo.ru/>`_ shortly.
