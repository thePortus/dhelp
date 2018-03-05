#!/usr/bin/python


from .base_text import BaseText


class CLTKLatinText(BaseText):
    """Main class to interact with Latin-language texts.

    Provides Latin-specific CLTK functions for text passed upon construction.
    Most methods return a new version of the text, except those that give
    non-text results (e.g. pos tagging)
    """
    pass
