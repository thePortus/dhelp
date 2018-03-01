#!/usr/bin/python

import os
import csv
import shutil

from .abc_case import AbstractBaseUnitTest

from ..csv_file import CSVFile


fixtures_path = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
)
fixture_dir = 'csv'
temp_dir = '.testing'


class CSVFileLayer:

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


class TestCSVFile(AbstractBaseUnitTest):
    layer = CSVFileLayer
    test_class = CSVFile
    fixtures_path = os.path.join(fixtures_path, temp_dir)

    def test_load(self):
        # first record should match
        exempla = self.make_test_obj('fake_data.csv')
        exempla = exempla.load(options={'silent': True})[0]['text']
        comparanda = 'This is the first record'
        return self.assertEqual(exempla, comparanda)

    def test_save(self):
        # should correctly modified the first record
        csv_records = []
        # manually open csv file
        with open(
            os.path.join(
                fixtures_path,
                temp_dir,
                'fake_data.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        # alter first record, then save to file
        csv_records[0]['text'] = 'Altered test record'
        exempla = self.make_test_obj('fake_data.csv')
        exempla.save(
            csv_records,
            fieldnames=['id', 'text', 'notes'],
            options={'overwrite': True, 'silent': True}
        )
        # manually reopen csv file to check for results
        csv_records = []
        with open(
            os.path.join(
                fixtures_path,
                temp_dir,
                'fake_data.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        return self.assertEqual(csv_records[0]['text'], 'Altered test record')

    def test_modify(self):
        # should have modified first record

        def modify_function(csv_record):
            csv_record['text'] = 'Altered test record'
            return csv_record

        exempla = self.make_test_obj('fake_data.csv')
        exempla.modify(
            os.path.join(fixtures_path, temp_dir, 'fake_data_modified.csv'),
            modify_function,
            options={'silent': True}
        )
        # manually reopen csv file to check for results
        csv_records = []
        with open(
            os.path.join(
                fixtures_path,
                temp_dir,
                'fake_data_modified.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        return self.assertEqual(csv_records[4]['text'], 'Altered test record')

    def test_column_to_txts(self):
        # should have produced a folder of .txt files
        pass
