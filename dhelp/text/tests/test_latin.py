#!/usr/bin/python

import unittest

from ..latin import LatinText


class LatinSetupLayer:

    @classmethod
    def setUp(cls):
        LatinText('').setup()


class TestLatinText(unittest.TestCase):
    layer = LatinSetupLayer

    def test_tokenize(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres')
        exempla = exempla.tokenize()
        comparanda = [
            'Gallia',
            'est',
            'omnis',
            'divisa',
            'in',
            'partes',
            'tres'
        ]
        return self.assertEqual(exempla, comparanda)

    def test_lemmatize(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres')
        exempla = exempla.lemmatize()
        comparanda = 'gallia edo1 omne divido in pars tres'
        return self.assertEqual(exempla, comparanda)

    def test_scansion(self):
        # Should get type of string
        exempla = LatinText(
            'Arma virumque cano, Troiae qui primus ab oris'
        )
        exempla = exempla.scansion()
        comparanda = ['¯˘˘¯˘˘˘˘˘¯˘˘˘˘˘x']
        return self.assertEqual(exempla, comparanda)

    def test_entities(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres')
        exempla = exempla.entities()
        comparanda = ['Gallia']
        return self.assertEqual(exempla, comparanda)

    def test_compare_longest_common_substring(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres')
        exempla = exempla.compare_longest_common_substring(
            'Galliae sunt omnis divisae in partes tres'
        )
        comparanda = 'in partes tres'
        return self.assertEqual(exempla, comparanda)

    def test_compare_minhash(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres')
        exempla = exempla.compare_minhash(
            'Galliae sunt omnis divisae in partes tres'
        )
        comparanda = 0.6444444444444445
        return self.assertEqual(exempla, comparanda)

    def test_word_count(self):
        # Should get type of string
        exempla = LatinText('Gallia est omnis divisa in partes tres tres tres')
        exempla = exempla.word_count()['tres']
        comparanda = 3
        return self.assertEqual(exempla, comparanda)

    def test_macronize(self):
        # Should get type of string
        exempla = LatinText('Arma virumque cano, Troiae qui primus ab oris')
        exempla = exempla.macronize()
        comparanda = 'arma virumque cano , trojae quī prīmus ab ōrīs'
        return self.assertEqual(exempla, comparanda)

    def test_normalize(self):
        # Should get type of string
        exempla = LatinText('Arma virumque cano, Troiae qui primus ab oris')
        exempla = exempla.normalize()
        comparanda = 'Arma uirumque cano, Troiae qui primus ab oris'
        return self.assertEqual(exempla, comparanda)

    def test_stemmify(self):
        # Should get type of string
        exempla = LatinText('Arma virumque cano, Troiae qui primus ab oris')
        exempla = exempla.stemmify()
        comparanda = 'arm vir cano, troi qui prim ab or '
        return self.assertEqual(exempla, comparanda)

    def test_clausulae(self):
        # Should get type of string
        exempla = LatinText('Arma virumque cano, Troiae qui primus ab oris')
        exempla = exempla.clausulae()
        comparanda = {
            'cretic + trochee': 0,
            '4th paeon + trochee': 0,
            '1st paeon + trochee': 0,
            'substituted cretic + trochee': 0,
            '1st paeon + anapest': 0,
            'double cretic': 0,
            '4th paeon + cretic': 0,
            'molossus + cretic': 0,
            'double trochee': 0,
            'molossus + double trochee': 0,
            'cretic + double trochee': 0,
            'dactyl + double trochee': 0,
            'choriamb + double trochee': 0,
            'cretic + iamb': 0,
            'molossus + iamb': 0, 'double spondee': 0,
            'cretic + double spondee': 0, 'heroic': 0
        }
        return self.assertEqual(exempla, comparanda)
