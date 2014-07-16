# coding: utf-8
import pathlib


def force_path(path):
    """
    Return a pathlib.Path instance.

    :param path: An object representing a file path ('/tmp/foo', Path(/tmp/foo), etc)
    """
    return path if isinstance(path, pathlib.Path) else pathlib.Path(path)
