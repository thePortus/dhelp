#!/usr/bin/python

import os
import shutil

from .abc_case import AbstractBaseUnitTest

from ..text_file import TextFile


fixtures_path = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
)
fixture_dir = 'txt'
temp_dir = '.testing'


class TextFileLayer:

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


class TestTextFile(AbstractBaseUnitTest):
    layer = TextFileLayer
    test_class = TextFile
    fixtures_path = os.path.join(fixtures_path, temp_dir)

    def test_exists(self):
        # should return true since file exists
        exempla = self.make_test_obj('fake_data_1.txt')
        return self.assertTrue(exempla.exists)

    def test_size(self):
        # should have a file size greater than 0
        exempla = self.make_test_obj('fake_data_1.txt')
        return self.assertTrue(exempla.size > 0)

    def test_basename(self):
        # should return filename correctly
        exempla = self.make_test_obj('fake_data_1.txt')
        comparanda = 'fake_data_1.txt'
        return self.assertEqual(exempla.basename, comparanda)

    def test_dirname(self):
        # should return parent folder name correctly
        exempla = self.make_test_obj('fake_data_1.txt')
        comparanda = os.path.dirname(str(exempla))
        return self.assertEqual(exempla.dirname, comparanda)

    def test_is_file(self):
        # should return true
        exempla = self.make_test_obj('fake_data_1.txt')
        return self.assertTrue(exempla.is_file)

    def test_is_dir(self):
        # should return false
        exempla = self.make_test_obj('fake_data_1.txt')
        return self.assertFalse(exempla.is_dir)

    def test_is_link(self):
        # should return false
        exempla = self.make_test_obj('fake_data_1.txt')
        return self.assertFalse(exempla.is_link)

    def test_makedirs(self):
        # should automatically make parent dirs of path
        exempla = self.make_test_obj(os.path.join('subdir', 'fake_data_1.txt'))
        exempla.makedirs()
        return self.assertTrue(os.path.exists(os.path.dirname(str(exempla))))

    def test_copy(self):
        # should return new path object
        exempla = self.make_test_obj('fake_data_1.txt')
        exempla = exempla.copy(
            os.path.join(fixtures_path, temp_dir, 'fake_data_1_copy.txt')
        )
        return self.assertTrue(os.path.exists(str(exempla)))

    def test_remove(self):
        # should remove temp testing file
        exempla = self.make_test_obj('fake_data_1.txt')
        exempla.remove()
        return self.assertFalse(os.path.exists(str(exempla)))

    def test_move(self):
        # should copy temp testing file
        exempla = self.make_test_obj('fake_data_1.txt')
        comparanda = exempla.move(
            os.path.join(fixtures_path, temp_dir, 'fake_data_1_copy.txt')
        )
        return self.assertTrue(
            os.path.exists(str(comparanda)) and
            not os.path.exists(str(exempla))
        )

    def test_load(self):
        # first line of loaded content should match
        exempla = self.make_test_obj('fake_data_1.txt')
        exempla = exempla.load(options={'silent': True}).split('\n')[0]
        comparanda = 'First test file'
        return self.assertEqual(exempla, comparanda)

    def test_save_no_overwrite(self):
        # should raise exception if overwrite is not specified
        exemplum = self.make_test_obj('fake_data_1.txt')
        return self.assertRaises(Exception, lambda: exemplum.save(
            'Altered test file',
            options={'silent': True}
        ))

    def test_save_overwrite(self):
        # should save altered testing file
        exempla = None
        comparanda = 'Altered test file'
        self.make_test_obj('fake_data_1.txt').save(
            comparanda, options={'overwrite': True, 'silent': True}
        )
        with open(
            os.path.join(fixtures_path, temp_dir, 'fake_data_1.txt')
        ) as test_file:
            exempla = test_file.read()
        return self.assertEqual(exempla, comparanda)
