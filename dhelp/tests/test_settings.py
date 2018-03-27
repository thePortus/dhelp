#!/usr/bin/python

import unittest

from .. import settings


class TestSettings(unittest.TestCase):

    def test_languages(self):
        return self.assertTrue(settings.LANGUAGES)

    def test_delimiters(self):
        return self.assertTrue(settings.DELIMITERS)

    def test_nltk_packages(self):
        return self.assertTrue(settings.NLTK_PACKAGES)

    def test_encodings(self):
        return self.assertTrue(settings.ENCODINGS)
