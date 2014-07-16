# coding: utf-8
from __future__ import unicode_literals

import os
import pathlib

import appconf


class AppConf(appconf.AppConf):

    # path to the proposals root
    ROOT = None

    # Default video language
    # (Language name, ISO 639-1 code)
    LANGUAGE = ('Russian', 'ru')

    # category metadata filename stem
    # e.g. category.json, category.yaml, etc
    CATEGORY_META = 'category'

    # category directory name pattern
    # e.g. ^[A-Za-z0-9_]+$
    # if None then no restrictions are in effect
    CATEGORY_NAME = None

    # a video proposal filename stem (i.e. with no json/yaml/etc extension) pattern
    # e.g. ^[a-z0-9](?:[a-z0-9_-]+)?$
    # If left to None, then no restrictions are in effect
    VIDEO_NAME = None

    def configure_root(self, value):
        """
        Configure PROPOSAL_ROOT.
        The setting defaults to root/drafts (i.e. a sibling of the project module dir).

        Return a pathlib.Path object.
        """
        if not value:
            value = pathlib.Path(os.path.dirname(__file__)).parent / 'drafts'

        # return the value as-is
        if isinstance(value, pathlib.Path):
            return value

        return pathlib.Path(os.path.normpath(os.path.abspath(value)))

    class Meta:
        prefix = 'proposal'
