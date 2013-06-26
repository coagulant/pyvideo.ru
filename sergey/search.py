# coding: utf-8
from django.conf import settings
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine


class ConfigurableElasticBackend(ElasticsearchSearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(ConfigurableElasticBackend, self).__init__(connection_alias, **connection_options)
        user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS')
        if user_settings:
            setattr(self, 'DEFAULT_SETTINGS', user_settings)


class ConfigurableElasticSearchEngine(ElasticsearchSearchEngine):
    backend = ConfigurableElasticBackend
