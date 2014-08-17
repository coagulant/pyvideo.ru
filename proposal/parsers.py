# coding: utf-8
import re

from django.core.serializers import SerializerDoesNotExist
from django.conf import settings
from rest_framework.settings import api_settings
from richard.videos.models import Category

from .serializers import CategorySerializer, VideoSerializer
from .utils import force_path
from .exceptions import ProposalError, TemplateError, ObjectError


class BaseParser(object):

    def __init__(self):
        # build a format -> media type map
        self.formats = {
            renderer.format: renderer.media_type for renderer
            in api_settings.DEFAULT_RENDERER_CLASSES
        }
        # associate media types with their parser classes
        self.parsers = {
            parser.media_type: parser for parser
            in api_settings.DEFAULT_PARSER_CLASSES
        }

    def deserialize(self, format, stream):
        """
        Attempt to read and deserialize data from ``stream``.
        Return a deserialized object.

        :param format: Serialization format (json, yaml, xml, etc)
        :param stream: file-like obj

        :raises django.core.serializers.SerializerDoesNotExist:
            If provided ``format`` value is not registered with a parser class.
        """
        try:
            media_type = self.formats[format]
            parser_class = self.parsers[media_type]
        except KeyError:
            raise SerializerDoesNotExist(format)
        else:
            return parser_class().parse(stream)


class Videos(BaseParser):
    """
    Parser class that takes a file path as an argument.

    An instance of the class is an iterator that walks the file tree
    seeking for serialized video and category objects, deserializes the objects
    with either ``proposal.serializers.VideoSerializer`` or
    ``proposal.serializers.CategorySerializer`` serializers and
     yields "unsaved" instances of the video serializer class.

    :param path: Path to a proposal root (may as well be a pathlib.Path instance)

    :raises proposal.exceptions.ProposalError:
        If proposal root does not follow the correct file structure or contains unserializable files.
    """
    def __init__(self, path):
        super(Videos, self).__init__()
        self.path = path

    def __iter__(self):
        """
        Return and iterator that walks the file tree seeking for serialized objects
        and yielding unsaved instances of ``proposal.serializers.VideoSerializer``.
        """
        return self._iter_proposal_root(self.path)

    def _iter_proposal_root(self, path):
        # list of caught exceptions
        exc_list = []
        try:
            for category_path in force_path(path).iterdir():
                # skip directories/files that begin with a non-alphanumeric character
                if not re.match(r'^[a-z0-9]', category_path.stem, flags=re.I):
                    continue
                try:
                    yield from self._iter_category(category_path)
                except ProposalError as e:
                    exc_list.append((type(e), str(e)))
        # catch all uncaught OSError's
        except OSError as e:
            raise TemplateError(str(e))

        if exc_list:
            # provide the caller with a full list of occured errors
            raise ProposalError(exc_list)

    def _iter_category(self, path):
        # a proposal root must contain directories only
        if not path.is_dir():
            raise TemplateError('%s is not a directory' % path)

        # list of video objects (dictionaries) found in the directory
        objects = []
        # category description object
        category_obj = None

        # attempt to deserialize objects using associated serializers
        for video_path in path.iterdir():

            # skip files that begin with a dot
            if video_path.is_file() and video_path.stem.startswith('.'):
                continue

            obj = self._get_object(video_path)

            # this is the category metafile
            if video_path.stem == settings.PROPOSAL_CATEGORY_META:
                # a metafile (probably with another extension) has already been found
                if category_obj is not None:
                    raise TemplateError('duplicate metafiles are found in %s' % path)
                category_obj = obj
            # this is a video object
            else:
                objects.append(obj)

        # acquire a Category instance either from non-empty description object
        # or directory name as a category slug
        category = self._get_category(category_obj, path.stem)

        for video_obj in objects:
            # assign the saved category id to all assotitated video objects
            video_obj.update({'category': category.pk})
            serializer = VideoSerializer(data=video_obj)

            if not serializer.is_valid():
                raise ObjectError('%s is not a valid video object' % video_obj)

            yield serializer

    def _get_object(self, path):
        path = force_path(path)
        try:
            with open(str(path), 'rb') as f:
                try:
                    obj = self.deserialize(path.suffix[1:], f)
                except SerializerDoesNotExist:
                    raise TemplateError('%s is not a registered serializer format (%s)' % (path.suffix[1:], path))
                except Exception as e:
                    raise ObjectError('failed to deserialize %s (%s)' % (path, e))

                if not isinstance(obj, dict):
                    raise ObjectError('%s does not yield a dictionary' % path)

                return obj
        except OSError:
            raise TemplateError('failed to open %s' % path)

    def _get_category(self, obj, slug=''):
        if not obj:
            # attempt to deslugify title
            title = re.sub(r'\W+', ' ', slug).strip().capitalize()

            # category title must not be empty
            if not title:
                raise ProposalError('failed to deslugify "%s"' % slug)

            return Category.objects.get_or_create(slug=slug, defaults={'title': title, 'slug': None})[0]
        else:
            # attempt to map the deserialized object to a django model
            serializer = CategorySerializer(data=obj)

            if not serializer.is_valid():
                raise ObjectError('failed to map %s to a model' % obj)

            return serializer.save() or serializer.object


# backward compat
videos = Videos
