#!/usr/bin/python

import unittest

import os
import shutil

from .._bases import BaseFile, BaseFolder


fixtures_src = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
    'txt'
)
fixtures_dest = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
    '.testing'
)
options = {
    'silent': False
}


class TextFixturesLayer:

    @classmethod
    def testSetUp(cls):
        # remove any extant temp fixture files
        if os.path.exists(fixtures_dest):
            shutil.rmtree(fixtures_dest)
        # ensure requisite parent dirs created, make them if not
        if not os.path.exists(os.path.dirname(fixtures_dest)):
            os.makedirs(os.path.dirname(fixtures_dest))
        # copy fixture files to temp dir
        shutil.copytree(fixtures_src, fixtures_dest)

    @classmethod
    def testTearDown(cls):
        # destroy any temporary fixture files remaining
        modified_fixtures_path = os.path.join(
            os.path.dirname(fixtures_dest),
            '.testing-modified'
        )
        if os.path.exists(fixtures_dest):
            shutil.rmtree(fixtures_dest)
        if os.path.exists(modified_fixtures_path):
            shutil.rmtree(modified_fixtures_path)


class TestBaseFile(unittest.TestCase):
    layer = TextFixturesLayer

    def test_error_non_string(self):
        # should error if not sent a string
        return self.assertRaises(Exception, lambda: BaseFile(2))

    def test_default_path(self):
        # should generate a default path if none given
        exempla = BaseFile()
        return self.assertTrue(os.path.exists(str(exempla)))

    def test_relative_path(self):
        # should build an absolute path when given a relative
        exempla = BaseFile('file.txt')
        comparanda = os.path.join(
            os.getcwd(),
            'file.txt'
        )
        return self.assertEqual(exempla, comparanda)

    def test_exists(self):
        # should return true since file exists
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        return self.assertTrue(exempla.exists)

    def test_size(self):
        # should have a file size greater than 0
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        return self.assertTrue(exempla.size > 0)

    def test_non_extant_size(self):
        # should return 0 when doesn't exist
        exempla = BaseFile('file.txt')
        return self.assertTrue(exempla.size == 0)

    def test_basename(self):
        # should return filename correctly
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        comparanda = 'fake_data_1.txt'
        return self.assertEqual(exempla.basename, comparanda)

    def test_dirname(self):
        # should return parent folder name correctly
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        comparanda = os.path.dirname(str(exempla))
        return self.assertEqual(exempla.dirname, comparanda)

    def test_is_file(self):
        # should return true
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        return self.assertTrue(exempla.is_file)

    def test_is_dir(self):
        # should return false
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        return self.assertFalse(exempla.is_dir)

    def test_is_link(self):
        # should return false
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        return self.assertFalse(exempla.is_link)

    def test_makedirs(self):
        # should automatically make parent dirs of path
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        exempla.makedirs(options={'silent': False})
        return self.assertTrue(os.path.exists(os.path.dirname(str(exempla))))

    def test_copy(self):
        # should return new path object, which should exist
        exempla = BaseFile(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            options={'silent': False}
        ).copy(os.path.join(fixtures_dest, 'fake_data_1_copy.txt'))
        return self.assertTrue(os.path.exists(str(exempla)))

    def test_remove(self):
        # should remove temp testing file
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        exempla.remove(options={'silent': False})
        return self.assertFalse(os.path.exists(str(exempla)))

    def test_move(self):
        # should copy temp testing file
        exempla = BaseFile(os.path.join(fixtures_dest, 'fake_data_1.txt'))
        comparanda = exempla.move(
            os.path.join(fixtures_dest, 'fake_data_1_copy.txt'),
            {'silent': False}
        )
        return self.assertTrue(
            os.path.exists(str(comparanda))
            and not
            os.path.exists(str(exempla))
        )


class TestBaseFolder(unittest.TestCase):
    layer = TextFixturesLayer

    def test_contents(self):
        # should have 5 items in the folder
        exempla = BaseFolder(fixtures_dest)
        return self.assertTrue(len(exempla.contents) == 5)

    def test_filenames(self):
        # should be 5 items in the folder
        exempla = BaseFolder(fixtures_dest)
        return self.assertTrue(len(exempla.filenames) == 5)

    def test_folders(self):
        # should be no length since there area no folders
        exempla = BaseFolder(fixtures_dest)
        return self.assertEqual(len(exempla.folders), 0)

    def test_length(self):
        # should have 5 items in the folder
        exempla = BaseFolder(fixtures_dest)
        return self.assertTrue(exempla.length == 5)

    def test_text_files(self):
        # should have 5 items in the folder
        exempla = BaseFolder(fixtures_dest)
        return self.assertTrue(len(exempla.files()) == 5)
