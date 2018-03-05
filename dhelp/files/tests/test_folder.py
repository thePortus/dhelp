#!/usr/bin/python

import os
import shutil

from .abc_case import AbstractBaseUnitTest

from ..folder import Folder


fixtures_path = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
)
fixture_dir = 'txt'
temp_dir = '.testing'


class FolderLayer:

    @classmethod
    def testSetUp(cls):
        source = os.path.join(fixtures_path, fixture_dir)
        destination = os.path.join(fixtures_path, temp_dir)
        # remove any extant temp fixture files
        if os.path.exists(destination):
            shutil.rmtree(destination)
        # ensure requisite parent dirs created, make them if not
        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))
        # copy fixture files to temp dir
        shutil.copytree(source, destination)

    @classmethod
    def testTearDown(cls):
        # destroy any temporary fixture files remaining
        destination = os.path.join(fixtures_path, temp_dir)
        if os.path.exists(destination):
            shutil.rmtree(destination)


class TestFolder(AbstractBaseUnitTest):
    layer = FolderLayer
    test_class = Folder
    fixtures_path = os.path.join(fixtures_path, temp_dir)

    def test_contents(self):
        # should have 5 items in the folder
        exempla = self.make_test_obj()
        return self.assertTrue(len(exempla.contents) == 5)

    def test_files(self):
        # should be 5 items in the folder
        exempla = self.make_test_obj()
        return self.assertTrue(len(exempla.files) == 5)

    def test_folders(self):
        # should be no length since there area no folders
        exempla = self.make_test_obj()
        return self.assertEqual(len(exempla.folders), 0)

    def test_length(self):
        # should have 5 items in the folder
        exempla = self.make_test_obj()
        return self.assertTrue(exempla.length == 5)
