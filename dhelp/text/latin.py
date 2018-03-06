#!/usr/bin/python

from ._bases_mixins import BaseText, CLTKMixin


class LatinText(CLTKMixin, BaseText):
    """Main class to interact with Latin-language texts.

    Provides Latin-specific CLTK functions for text passed upon construction.
    Most methods return a new version of the text, except those that give
    non-text results (e.g. pos tagging)

    Example:
        >>> from dhelp import LatinText
        >>> text = LatinText('Gallia est omnis divisa in partes tres')
        >>> print(text.lemmatize())
        gallia edo1 omne divido in pars tres
    """

    def __init__(self, text, options={}):
        options['language'] = 'latin'
        super().__init__(text=text, options=options)

    def macronize(self, mode='tag_ngram_123_backoff'):
        """Adds macrons (long vowel marks).

        Macrons distinguish long vowels from short. Distinguishing them is
        critical for the study of Latin poetry and occasionally is important
        in prose. Note that once you add macrons, long vowels are, for all
        intents and purposes, different letters than their short equivalents.

        Args:
            mode (:obj:`str`, optional) POS tagging method to use, 'tag_ngram_123_backoff', 'tag_tnt', or 'tag_crf'

        Returns:
            :obj:`self.__class__` New text with macrons added to long vowels

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.macronize())
            arma virumque cano , trojae quī prīmus ab ōrīs
        """ # noqa
        from cltk.prosody.latin.macronizer import Macronizer
        mode = mode.lower()
        if (
            mode != 'tag_ngram_123_backoff' and
            mode != 'tag_tnt' and
            mode != 'tag_crf'
        ):
            return False
        return self.__class__(
            Macronizer(tagger=mode).macronize_text(self.data),
            self.options
        )

    def normalize(self):
        """Replaces 'j's with 'i's and 'v's with 'u's.

        Ancient texts did not use j's or 'v's (viz. Indiana Jones and the Last
        Crusade), but their usage in modern texts can throw off word counts,
        pattern mataching, and general text-analysis methods. This method
        converts these letters to their ancient versions.

        Returns:
            :obj:`self.__class__` New text with macrons added to long vowels

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.normalize())
            Arma uirumque cano, Troiae qui primus ab oris
        """ # noqa
        from cltk.stem.latin.j_v import JVReplacer
        return self.__class__(
            JVReplacer().replace(self.data),
            self.options
        )

    def stemmify(self):
        """Returns text with only stems.

        An alternate method to lemmatization. Instead of converting to lemmata
        (principi -> princeps) converts to stemma (principi -> princp)

        Returns:
            :obj:`self.__class__` New text with stemma

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.stemmify())
            arm vir cano, troi qui prim ab or
        """ # noqa
        from cltk.stem.latin.stem import Stemmer
        return self.__class__(
            Stemmer().stem(self.data.lower()),
            self.options
        )

    def clausulae(self):
        """Counts different kinds of prose clausulae.

        Examines prose for evidence for poetic rythms (clausulae). Returns a
        keyword/value dict with total counts for each kind of clausula.

        Returns:
            :obj:`list` of `str` Individual clausulae results

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.clausulae())
            {'cretic + trochee': 0, '4th paeon + trochee': 0, '1st paeon + trochee': 0, 'substituted cretic + trochee': 0, '1st paeon + anapest': 0, 'double cretic': 0, '4th paeon + cretic': 0, 'molossus + cretic': 0, 'double trochee': 0, 'molossus + double trochee': 0, 'cretic + double trochee': 0, 'dactyl + double trochee': 0, 'choriamb + double trochee': 0, 'cretic + iamb': 0, 'molossus + iamb': 0, 'double spondee': 0, 'cretic + double spondee': 0, 'heroic': 0}
        """ # noqa
        from cltk.prosody.latin.clausulae_analysis import Clausulae
        return Clausulae().clausulae_analysis(self.data)
