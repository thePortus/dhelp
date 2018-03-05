#!/user/bin/python

from .base_text import BaseText
from .mixin_nltk import NLTKMixin


class EnglishText(NLTKMixin, BaseText):
    """Main class to interact with English-language texts.

    EnglishText provides methods for altering texts for pre-processing as well
    as numerous nlp methods for analyzing the text. Text alteration methods
    can be chained since they each return a new instance of the class created
    with the altered text.

    Example:
        >>> english_text = EnglishText('Th3e Qui\\nck b     rown fox jumped over the lazy dog') # noqa
        >>> english_text.rm_lines().rm_nonchars().rm_spaces()
        'The quick brown fox jumped over the lazy dog'
    """

    def __init__(self, text, options={}):
        options['language'] = 'english'
        super().__init__(text=text, options=options)
