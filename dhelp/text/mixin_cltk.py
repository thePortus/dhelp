#!/usr/bin/python


from .base_text import BaseText


class CLTKMixin(BaseText):
    """Mixin for CLTK-related functions.

    Parent class for Latin, Classical Greek, and other CLTK language-specific
    objects. Provides access to universal CLTK commands with child classes
    adding some methods and overriding others.
    """
    pass
