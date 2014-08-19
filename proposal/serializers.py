# coding: utf-8
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import serializers
from rest_framework.compat import smart_text

from richard.videos.models import Category, Video, Language


class EnhancedSlugRelatedField(serializers.SlugRelatedField):

    def __init__(self, *args, **kwargs):
        # create new objects if none found in db
        self.allow_create = kwargs.pop('allow_create', True)
        # call a coercing function upon a native value
        self.coerce = kwargs.pop('coerce', None)
        # use a different field lookup option
        self.slug_lookup_field = kwargs.pop('slug_lookup_field', None)

        super(EnhancedSlugRelatedField, self).__init__(*args, **kwargs)

        # lookup field defaults to the slug field value
        self.slug_lookup_field = self.slug_lookup_field or self.slug_field

    def from_native(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a `queryset` argument')

        data = data.strip()

        # alter the value
        if self.coerce is not None:
            data = self.coerce(data)

        try:
            return self.queryset.get(**{self.slug_lookup_field: data})
        except ObjectDoesNotExist:
            if not self.allow_create:
                # new objects are not allowed to be created
                # hence the exception
                raise ValidationError(
                    self.error_messages['does_not_exist'] % (self.slug_field, smart_text(data))
                )
            obj = self.queryset.model(**{self.slug_field: data})
            obj.save()
            return obj
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)


class CategorySerializer(serializers.ModelSerializer):
    # remap start_date to date
    date = serializers.DateField(source='start_date', required=False)

    class Meta:
        model = Category
        fields = ('title', 'description', 'date', 'url')

    def restore_object(self, attrs, instance=None):
        if instance is None:
            # attempt to find an existing Category instance by case insensitive name
            try:
                # return the first matching row
                instance = (Category.objects
                    .filter(title__iexact=attrs['title'])
                    .order_by('pk')[:1]
                    .get()
                )
            except ObjectDoesNotExist:
                pass

        return super(CategorySerializer, self).restore_object(attrs, instance)


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField()
    date = serializers.DateField(source='recorded', required=False)
    url = serializers.URLField(required=True, source='source_url')
    # keep this field in order to pass model validation
    slug = serializers.SlugField(read_only=True)
    # dont create non-existent Language entries
    language = EnhancedSlugRelatedField(
        many=False, required=False, slug_field='name',
        slug_lookup_field='name__iexact', allow_create=False
    )
    speakers = EnhancedSlugRelatedField(
        many=True, slug_field='name',
        slug_lookup_field='name__iexact'
    )
    tags = EnhancedSlugRelatedField(
        many=True, slug_field='tag',
        slug_lookup_field='tag__iexact', coerce=str.lower
    )

    class Meta:
        model = Video
        fields = (
            'category', 'title', 'description', 'summary',
            'date', 'language', 'url',
            'slug', 'speakers', 'tags',
        )

    def full_clean(self, instance):

        # use default value for video entries with no language specified
        if not instance.language:
            name, iso639_1 = settings.PROPOSAL_LANGUAGE
            instance.language, _ = Language.objects.get_or_create(
                name=name, iso639_1=iso639_1
            )

        # proposed videos are live
        instance.state = Video.STATE_LIVE

        return super(VideoSerializer, self).full_clean(instance)

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # attempt to find an existing instance by category pk and case insensitive title
            try:
                # attempt to return the first matching Video instance
                instance = (Video.objects
                    .filter(category=attrs['category'], title__iexact=attrs['title'])
                    .order_by('pk')[:1]
                    .get()
                )
            except ObjectDoesNotExist:
                pass

        return super(VideoSerializer, self).restore_object(attrs, instance)
