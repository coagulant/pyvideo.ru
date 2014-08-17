# coding: utf-8
import os

from django import test
from django.core.exceptions import ObjectDoesNotExist

from richard.videos.models import Category, Language
from proposal import exceptions
from proposal.utils import force_path
from proposal.parsers import videos


try:
    test.TestCase.assertCountEqual
except AttributeError:
    test.TestCase.assertCountEqual = test.TestCase.assertItemsEqual


class TestCase(test.TestCase):
    test_path = force_path(os.path.abspath(os.path.dirname(__file__))) / 'test_proposal'

    @staticmethod
    def save_videos(path):
        for video in videos(path):
            video.save()


class InvalidProposalRootTestCase(TestCase):
    test_path = TestCase.test_path / 'invalid_roots'

    def test_proposal_root_must_contain_directories_only(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'root_contains_files')

    def test_category_directory_with_no_metafile_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'no_category_metafile')

    def test_category_directory_with_multiple_metafiles_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'multiple_category_metafiles')

    def test_category_directory_with_unexpected_video_files_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'unexpected_video_files')

    def test_category_directory_with_unknown_file_format_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'unknown_file_format')

    def test_improper_yaml_file_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'undeserializable_yaml_files')

    def test_improper_json_file_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'undeserializable_json_files')

    def test_improper_xml_file_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'undeserializable_xml_files')

    def test_category_with_invalid_metafile_object_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'invalid_category_object')

    def test_category_with_invalid_video_objects_raises_exception(self):
        with self.assertRaises(exceptions.ProposalError):
            self.save_videos(self.test_path / 'invalid_video_objects')


class ValidProposalRootTestCase(TestCase):
    test_path = TestCase.test_path / 'valid_roots'

    def test_valid_proposal_root(self):
        """Test no exception is raised when a valid proposal root is parsed."""
        self.save_videos(self.test_path / 'valid_categories')

    def test_empty_proposal_root_is_valid(self):
        """Test no exception is raised when an empty proposal root is parsed."""
        self.save_videos(self.test_path / 'empty_root')

    def test_namesake_categories_from_different_directories_get_their_videos_merged(self):
        self.save_videos(self.test_path / 'namesake_categories')
        self.assertEqual(Category.objects.get(title='Foo').videos.count(), 2)

    def test_category_video_list_is_not_emptied(self):
        category = Category.objects.create(title='Foo Category')
        category.videos.create(title='Foo Video', source_url='http://example.org/foo/')
        category.videos.create(title='Bar Video', source_url='http://example.org/foo/')
        self.assertEqual(category.videos.count(), 2)

        self.save_videos(self.test_path / 'empty_categories')
        self.assertEqual(category.videos.count(), 2)

    def test_category_directory_starting_with_non_alpha_numeric_character_is_ignored(self):
        self.save_videos(self.test_path / 'ignored_categories')

        # Bar is not ignored
        Category.objects.get(title='Bar')
        # All of the Foo are ignored
        with self.assertRaises(ObjectDoesNotExist):
            Category.objects.get(title='Foo')

    def test_category_is_created_when_parsing_empty_category_directory(self):
        self.save_videos(self.test_path / 'no_category_files')
        Category.objects.get(title='Empty category', slug='empty-category')

    def test_category_directory_name_is_looked_up_against_slug_when_no_metafile_provided(self):
        category = Category.objects.create(title='Test Category')

        self.save_videos(self.test_path / 'no_category_metafile')
        self.assertEqual(category.videos.count(), 1)

    def test_category_directory_is_not_used_as_source_of_slug_value_for_new_objects(self):
        self.save_videos(self.test_path / 'uncanonical_slug')
        # although directory name is looked up against existing slugs
        # it is ignored when creating new Category objects
        self.assertEqual(Category.objects.get(title='Test category').slug, 'test-category')
