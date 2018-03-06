#!/usr/bin/python

import unittest

from ..english import EnglishText


class TestEnglishText(unittest.TestCase):

    def test_stringify(self):
        # Should get type of string
        exempla = EnglishText("Lorem ipsum dolor sit amet")
        exempla = type(exempla.stringify())
        comparanda = str
        return self.assertEqual(exempla, comparanda)

    def test_rm_lines(self):
        # should get version with endline replaced with space
        exempla = EnglishText("Lorem ipsum dolor\nsit amet")
        comparanda = EnglishText("Lorem ipsum dolor sit amet")
        exempla = exempla.rm_lines()
        return self.assertEqual(exempla, comparanda)

    def test_rm_nonchars(self):
        # numbers should be removed
        exempla = EnglishText("Lorem1 ipsum2 dolor3 sit4 amet5")
        comparanda = EnglishText("Lorem ipsum dolor sit amet")
        exempla = exempla.rm_nonchars()
        return self.assertEqual(exempla, comparanda)

    def test_rm_edits(self):
        # text between brackets should be removed
        exempla = EnglishText("Lorem ipsum [dolor] sit amet")
        comparanda = EnglishText("Lorem ipsum  sit amet")
        exempla = exempla.rm_edits()
        return self.assertEqual(exempla, comparanda)

    def test_rm_spaces(self):
        # redundant spaces should be gone
        exempla = EnglishText("Lorem   ipsum          dolor   sit    amet")
        comparanda = EnglishText("Lorem ipsum dolor sit amet")
        exempla = exempla.rm_spaces()
        return self.assertEqual(exempla, comparanda)

    def test_rm_stopwords(self):
        # word in stopword list should be removed
        exempla = EnglishText("Lorem ipsum dolor sit amet")
        comparanda = EnglishText("Lorem ipsum sit amet")
        exempla = exempla.rm_stopwords(['dolor'])
        return self.assertEqual(exempla, comparanda)

    def test_re_search_present(self):
        # should be true as pattern is present
        exempla = EnglishText("Lorem ipsum dolor sit amet")
        return self.assertTrue(exempla.re_search('ipsum'))

    def test_re_search_not_present(self):
        # should be false as pattern is not present
        exempla = EnglishText("Lorem ipsum dolor sit amet")
        return self.assertFalse(exempla.re_search('Arma virumque cano'))
