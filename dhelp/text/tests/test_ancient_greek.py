#!/usr/bin/python

import unittest

from ..ancient_greek import AncientGreekText


class AncientGreekSetupLayer:

    @classmethod
    def setUp(cls):
        AncientGreekText('').setup()


class TestAncientGreekText(unittest.TestCase):
    layer = AncientGreekSetupLayer

    def test_tokenize(self):
        # Should get type of string
        exempla = AncientGreekText('ὑπὲρ τοῦ υἱοῦ Χρυσίππου τοῦ Ἀντιφάνου')
        exempla = exempla.tokenize()
        comparanda = ['ὑπὲρ', 'τοῦ', 'υἱοῦ', 'Χρυσίππου', 'τοῦ', 'Ἀντιφάνου']
        return self.assertEqual(exempla, comparanda)

    def test_lemmatize(self):
        # Should get type of string
        exempla = AncientGreekText('ὑπὲρ τοῦ υἱοῦ Χρυσίππου τοῦ Ἀντιφάνου')
        exempla = exempla.lemmatize()
        comparanda = 'ὑπὲρ ὁ υἱός χρυσίππου ὁ ἀντιφάνου'
        return self.assertEqual(exempla, comparanda)

    # TODO: Fix scansion
    # def test_scansion(self):
        # Should get type of string
    #     exempla = AncientGreekText(
    #         'ἄνδρα μοι ἔννεπε, μοῦσα, πολύτροπον, ὃς μάλα πολλὰ'
    #     )
    #     exempla = exempla.scansion()
    #     comparanda = str
    #     return self.assertEqual(exempla, comparanda)

    def test_entities(self):
        # Should get type of string
        exempla = AncientGreekText('μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος')
        exempla = exempla.entities()
        comparanda = ['Ἀχιλῆος']
        return self.assertEqual(exempla, comparanda)

    def test_compare_longest_common_substring(self):
        # Should get type of string
        exempla = AncientGreekText('ὑπὲρ τοῦ υἱοῦ Χρυσίππου τοῦ Ἀντιφάνου')
        exempla = exempla.compare_longest_common_substring(
            'ὑπὲρ 3 τοῦ υἱοῦ Χρυ σίππου'
        )
        comparanda = 'τοῦ υἱοῦ Χρυ'
        return self.assertEqual(exempla, comparanda)

    def test_compare_minhash(self):
        # Should get type of string
        exempla = AncientGreekText('ὑπὲρ τοῦ υἱοῦ Χρυσίππου τοῦ Ἀντιφάνου')
        exempla = exempla.compare_minhash('ὑπὲρ 3 τοῦ υἱοῦ Χρυ σίππου')
        comparanda = 0.4594594594594595
        return self.assertEqual(exempla, comparanda)

    def test_word_count(self):
        # Should get type of string
        exempla = AncientGreekText('ὑπὲρ τοῦ υἱοῦ Χρυσίππου τοῦ Ἀντιφάνου')
        exempla = exempla.word_count(word='υἱοῦ')
        comparanda = 1
        return self.assertEqual(exempla, comparanda)

    def test_normalize(self):
        # Should get type of string
        exempla = AncientGreekText(
            'ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον'
        )
        exempla = exempla.normalize()
        comparanda = 'ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον'
        return self.assertEqual(exempla, comparanda)

    def test_tlgu_cleanup(self):
        # Should get type of string
        exempla = AncientGreekText(
            'ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον'
        )
        exempla = exempla.tlgu_cleanup()
        comparanda = 'ῖν εἰς δὲ τὸν ἕτερον καττίτερον'
        return self.assertEqual(exempla, comparanda)

    def test_tag(self):
        # Should get type of string
        exempla = AncientGreekText(
            'ἔστι δὲ σύμπαντα ταῦτα τὰ συγγράμματα'
        )
        exempla = exempla.tag()
        comparanda = [
            ('ἔστι', 'V3SPIA---'),
            ('δὲ', 'G--------'),
            ('σύμπαντα', None),
            ('ταῦτα', 'A-P---NA-'),
            ('τὰ', 'L-P---NA-'),
            ('συγγράμματα', None)
        ]
        return self.assertEqual(exempla, comparanda)
