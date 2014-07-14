# coding: utf-8

from richard.videos import utils
from slugify import slugify

# monkey patch richard.videos.utils.slugify so it handles all unicode characters
utils.slugify = slugify
