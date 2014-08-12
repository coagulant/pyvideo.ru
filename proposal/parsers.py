# coding: utf-8
import re

from django.core.serializers import SerializerDoesNotExist
from django.conf import settings
from rest_framework.settings import api_settings

from .serializers import CategorySerializer, VideoSerializer
from .utils import force_path
from .exceptions import TemplateError, ObjectError


def deserialize(format, stream):
    """
    Attempt to read and deserialize data from ``stream``.
    Return a deserialized object.

    :param format: Serialization format (json, yaml, xml, etc)
    :param stream: file-like obj

    :raises django.core.serializers.SerializerDoesNotExist:
        If provided ``format`` value is not registered with a parser class.

    :raises proposal.exceptions.ObjectError: If failed to deserialize data
        according to format.
    """
    # build a format -> media type map
    format_map = {
        renderer.format: renderer.media_type for renderer
        in api_settings.DEFAULT_RENDERER_CLASSES
    }
    # assotitate media types with their parser classes
    parser_map = {
        parser.media_type: parser for parser
        in api_settings.DEFAULT_PARSER_CLASSES
    }
    try:
        media_type = format_map[format]
        parser_class = parser_map[media_type]
    except KeyError:
        raise SerializerDoesNotExist(format)
    else:
        parser = parser_class()
        try:
            return parser.parse(stream)
        except:
            raise ObjectError()


def videos(path):
    """
    Parse categories and videos from a proposal root located at ``path``.
    Yield ``proposal.serializers.VideoSerializer`` objects.

    :param path: Path to a proposal root (may as well be a pathlib.Path instance)

    :raises proposal.exceptions.TemplateError: If proposal root does not follow
        the expected file structure.

    :raises proposal.exceptions.ObjectError: If parsed category or video
        files cannot be deserialized into valid instances of
        ``proposal.serializers.CategorySerializer`` or
        ``proposal.serializers.VideoSerializer`` respectively.
    """
    try:
        for category_path in force_path(path).iterdir():
            # skip directories/files that begin with a non-alphanumeric character
            if not re.match(r'^[a-z0-9]', category_path.stem, flags=re.I):
                continue
            # a proposal root must contain directories only
            if not category_path.is_dir():
                raise TemplateError('%s is not a directory' % category_path)

            video_objects = []
            category_object = None

            # attempt to deserialize objects using assotiated serializers
            for video_path in category_path.iterdir():
                # skip files that begin with a dot
                if video_path.is_file() and video_path.stem.startswith('.'):
                    continue
                try:
                    with open(str(video_path), 'rb') as f:
                        try:
                            obj = deserialize(video_path.suffix[1:], f)
                        except SerializerDoesNotExist:
                            raise TemplateError('failed to deserialize %s' % video_path)

                        if not isinstance(obj, dict):
                            raise ObjectError('%s does not yield a dictionary' % video_path)
                except OSError:
                    raise TemplateError('failed to open %s' % video_path)

                # this is the category metafile
                if video_path.stem == settings.PROPOSAL_CATEGORY_META:
                    # a metafile (probably with another extension) has already been found
                    if category_object is not None:
                        raise TemplateError('duplicate category metafiles are found in %s' % category_path)
                    category_object = obj
                # this is a video file
                else:
                    video_objects.append(obj)

            if category_object is None:
                raise TemplateError('%s is missing category metafile' % category_path)

            # attempt to map the deserialized object to a django model
            category_serializer = CategorySerializer(data=category_object)

            if not category_serializer.is_valid():
                raise ObjectError('%s contains invalid metafile' % category_path)
            category_serializer.save()

            for video_object in video_objects:
                # assign the saved category id to all assotitated video objects
                video_object.update({'category': category_serializer.object.pk})
                video_serializer = VideoSerializer(data=video_object)

                if not video_serializer.is_valid():
                    raise ObjectError('%s is not a valid video object' % video_object)

                yield video_serializer

    # the path is not a directory?
    except OSError as e:
        raise TemplateError(str(e))
