#!/usr/bin/python

from ._bases_mixins import BaseText, CLTKMixin


class AncientGreekText(CLTKMixin, BaseText):
    """Main class to interact with Classical Greek-language texts.

    Provides Classical Greek-specific CLTK functions for text passed upon
    construction. Most methods return a new version of the text, except those
    that give non-text results (e.g. pos tagging)

    Example:
        >>> from dhelp import AncientGreekText
        >>> text = AncientGreekText('ἔστι δὲ σύμπαντα ταῦτα τὰ συγγράμματα ἐκείνῃ μάλιστα οὐκ ὠφέλιμα, ὅτι ὡς πρὸς εἰδότας συγγέγραπται.')
        >>> print(text.lemmatize())
        εἰμί δὲ σύμπας οὗτος τὰ σύγγραμμα ἐκεῖνος μάλιστα οὐ ὠφέλιμος , ὅστις ὡς πρὸς οἶδα συγγράφω.
    """ # noqa

    def __init__(self, text, options={}):
        options['language'] = 'greek'
        super().__init__(text=text, options=options)

    def normalize(self):
        """Fixes problems with differences in greek accent encoding.

        Certain Greek accents have more than one possible encoding. Uses cltk's
        built-in normalizer to correct the character encoding differences and
        ensure that accents are encoded the same way.

        Returns:
            :obj:`self.__class__` New instance with altered text

        Example:
            >>> text = AncientGreekText('ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι')
            >>> print(text.normalize())
            ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι
        """ # noqa
        from cltk.corpus.utils.formatter import cltk_normalize
        return self.__class__(
            text=cltk_normalize(str(self.data)),
            options=self.options
        )

    def tlgu_cleanup(self, rm_punctuation=True, rm_periods=False):
        """Fix TLG betacode texts using TLGU.

        Necessary to cleanup TLG texts before processing, but can also used to
        perform rudimentary cleaning operations on other Greek texts.

        Args:
            rm_punctuation (:obj:`bool`, optional) True to remove punctuation marks (exception periods)
            rm_periods (:obj:`bool`, optional) True to remove periods

        Returns:
            :obj:`self.__class__` New instance with altered text

        Example:
            >>> text = AncientGreekText('ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι')
            >>> print(text.tlgu_cleanup())
            ῖν εἰς δὲ τὸν ἕτερον καττίτερον εἰ λῶιον καὶ ἄμεινόν ἐστι
        """ # noqa
        from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
        return self.__class__(
            text=tlg_plaintext_cleanup(
                self.data, rm_punctuation=rm_punctuation, rm_periods=rm_periods
            ),
            options=self.options
        )

    def tag(self, mode='123'):
        """Gives words marked up with parts-of-speech.

        Override's the cltk POS tagger and uses cltk's instead. Has different
        methods for providing a POS tagger, if desired.

        Args:
            mode (:obj:`str`) Tagging mode, either '123', or 'tnt'

        Returns:
            :obj:`list` of :obj:`tuple` 2-tuples with word, part-of-speech

        Example:
            >>> text = AncientGreekText('ἔστι δὲ σύμπαντα ταῦτα τὰ συγγράμματα ἐκείνῃ μάλιστα οὐκ ὠφέλιμα, ὅτι ὡς πρὸς εἰδότας συγγέγραπται.')
            >>> print(text.tag())
            [('ἔστι', 'V3SPIA---'), ('δὲ', 'G--------'), ('σύμπαντα', None), ('ταῦτα', 'A-P---NA-'), ('τὰ', 'L-P---NA-'), ('συγγράμματα', None), ('ἐκείνῃ', 'A-S---FD-'), ('μάλιστα', 'D--------'), ('οὐκ', 'D--------'), ('ὠφέλιμα', None), (',', 'U--------'), ('ὅτι', 'C--------'), ('ὡς', 'C--------'), ('πρὸς', 'R--------'), ('εἰδότας', 'T-PRPAMA-'), ('συγγέγραπται', None), ('.', '---------')]
        """ # noqa
        from cltk.tag.pos import POSTag
        tagger = POSTag(self.options['language'])
        mode = mode.lower()
        if mode != '123' and mode != 'tnt':
            raise Exception(
                'Invalid part of speech tagging mode specified.'
            )
        elif mode == '123':
            return tagger.tag_ngram_123_backoff(self.data)
        elif mode == 'tnt':
            return tagger.tag_tnt(self.data)
