#!/usr/bin/python

import unittest

import os
import shutil

from ..txt import TextFile, TextFolder


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


class TestTextFile(unittest.TestCase):
    layer = TextFixturesLayer

    def test_load(self):
        # first line of loaded content should match
        exempla = TextFile(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            options={'silent': False}
        )
        exempla = exempla.load().split('\n')[0]
        comparanda = 'First test file'
        return self.assertEqual(exempla, comparanda)

    def test_save_no_overwrite(self):
        # should raise exception if overwrite is not specified
        exempla = TextFile(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            options={'silent': False, 'overwrite': False}
        )
        return self.assertRaises(Exception, lambda: exempla.save(
            'Altered test file',
        ))

    def test_save_overwrite(self):
        # should save altered testing file
        exempla = TextFile(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            options={'silent': False}
        )
        comparanda = 'Altered test file'
        exempla.save(
            comparanda, options={'overwrite': True, 'silent': False}
        )
        with open(
            os.path.join(fixtures_dest, 'fake_data_1.txt')
        ) as test_file:
            exempla = test_file.read()
        return self.assertEqual(exempla, comparanda)

    def test_context_manager(self):
        exempla = TextFile(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            options={'silent': False}
        )
        comparanda = 'Testing message'
        with exempla as file_data:
            exempla.save_data = 'Testing message'
        with open(
            os.path.join(fixtures_dest, 'fake_data_1.txt'),
            'r+',
            encoding='utf-8'
        ) as file_data:
            exempla = file_data.read()
        return self.assertEqual(exempla, comparanda)


class TestTextFolder(unittest.TestCase):
    layer = TextFixturesLayer

    def test_modify(self):
        # should see changes after modifying files with a cb function

        def modify_file_function(record):
            return comparanda

        exempla = ''
        comparanda = 'Altered test file'
        # perform modification
        TextFolder(fixtures_dest, options={'silent': False}).modify(
            os.path.join(
                os.path.dirname(fixtures_dest),
                '.testing-modified'
            ),
            modify_file_function,
            options={'silent': False, 'overwrite': True}
        )
        # open file to check for success
        with open(
            os.path.join(
                os.path.dirname(fixtures_dest),
                '.testing-modified',
                'fake_data_1.txt'
            ),
        ) as test_file:
            exempla = test_file.read()
        return self.assertEqual(exempla, comparanda)

    def test_context_manager(self):
        exempla = None
        comparanda = 'Testing message'
        with TextFolder(fixtures_dest, options={'silent': False}) as txt_files:
            for txt_file in txt_files:
                with txt_file as txt_data:
                    txt_file.save_data = txt_data
                    txt_file.save_data = 'Testing message'
        with open(
            os.path.join(
                fixtures_dest,
                'fake_data_1.txt'
            ),
        ) as file_data:
            exempla = file_data.read()
        return self.assertEqual(exempla, comparanda)
