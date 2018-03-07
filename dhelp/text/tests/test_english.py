#!/usr/bin/python

import unittest

import nltk

from ..english import EnglishText


class AncientGreekSetupLayer:

    @classmethod
    def setUp(cls):
        nltk.download('punkt')


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

    def test_tokenize(self):
        # should return list of words
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = [
            'The',
            'quick',
            'brown',
            'fox',
            'jumped',
            'over',
            'the',
            'lazy',
            'dog'
        ]
        exempla = exempla.tokenize()
        return self.assertEqual(exempla, comparanda)

    def test_lemmatize(self):
        # should give lemmatized version of text
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = 'The quick brown fox jump over the lazy dog'
        exempla = exempla.lemmatize()
        return self.assertEqual(exempla, comparanda)

    def test_tag(self):
        # should return list of tuples with word|pos
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = [
            ('The', 'DT'),
            ('quick', 'JJ'),
            ('brown', 'NN'),
            ('fox', 'NN'),
            ('jumped', 'VBD'),
            ('over', 'IN'),
            ('the', 'DT'),
            ('lazy', 'JJ'),
            ('dog', 'NN')
        ]
        exempla = exempla.tag()
        return self.assertEqual(exempla, comparanda)

    def test_ngrams(self):
        # should return list of tuples with ngrams
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = [
            ('The', 'quick', 'brown'),
            ('quick', 'brown', 'fox'),
            ('brown', 'fox', 'jumped'),
            ('fox', 'jumped', 'over'),
            ('jumped', 'over', 'the'),
            ('over', 'the', 'lazy'),
            ('the', 'lazy', 'dog')
        ]
        exempla = exempla.ngrams()
        return self.assertEqual(exempla, comparanda)

    def test_skipgrams(self):
        # should return list of tuples with skipgrams
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = [
            ('The', 'quick', 'brown'),
            ('The', 'quick', 'fox'),
            ('The', 'brown', 'fox'),
            ('quick', 'brown', 'fox'),
            ('quick', 'brown', 'jumped'),
            ('quick', 'fox', 'jumped'),
            ('brown', 'fox', 'jumped'),
            ('brown', 'fox', 'over'),
            ('brown', 'jumped', 'over'),
            ('fox', 'jumped', 'over'),
            ('fox', 'jumped', 'the'),
            ('fox', 'over', 'the'),
            ('jumped', 'over', 'the'),
            ('jumped', 'over', 'lazy'),
            ('jumped', 'the', 'lazy'),
            ('over', 'the', 'lazy'),
            ('over', 'the', 'dog'),
            ('over', 'lazy', 'dog'),
            ('the', 'lazy', 'dog')
        ]
        exempla = exempla.skipgrams()
        return self.assertEqual(exempla, comparanda)

    def test_word_count(self):
        # should return dictionary with word tallys
        exempla = EnglishText('The quick brown fox jumped over the lazy dog')
        comparanda = {
            'The': 1,
            'quick': 1,
            'brown': 1,
            'fox': 1,
            'jumped': 1,
            'over': 1,
            'the': 1,
            'lazy': 1,
            'dog': 1
        }
        exempla = exempla.word_counts()
        return self.assertEqual(exempla, comparanda)
