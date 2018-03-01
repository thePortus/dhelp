#!/usr/bin/python

import os
import shutil

from .abc_case import AbstractBaseUnitTest

from ..text_folder import TextFolder


fixtures_path = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
)
fixture_dir = 'txt'
temp_dir = '.testing'


class TextFolderLayer:

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


class TestTextFolder(AbstractBaseUnitTest):
    layer = TextFolderLayer
    test_class = TextFolder
    fixtures_path = os.path.join(fixtures_path, temp_dir)

    def test_text_files(self):
        # should have 5 items in the folder
        exempla = self.make_test_obj()
        return self.assertTrue(len(exempla.text_files()) == 5)

    def test_modify(self):
        # should see changes after modifying files with a cb function

        def modify_file_function(record):
            return comparanda

        exempla = ''
        comparanda = 'Altered test file'
        destination = os.path.join(fixtures_path, temp_dir, 'test')
        # perform modification
        self.make_test_obj().modify(
            destination,
            modify_file_function,
            options={'silent': True}
        )
        # open file to check for success
        with open(
            os.path.join(fixtures_path, temp_dir, 'test', 'fake_data_1.txt')
        ) as test_file:
            exempla = test_file.read()
        return self.assertEqual(exempla, comparanda)
