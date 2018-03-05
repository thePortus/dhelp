#!/usr/bin/python


from .base_text import BaseText


class AncientGreekText(BaseText):
    """Main class to interact with Classical Greek-language texts.

    Provides Classical Greek-specific CLTK functions for text passed upon
    construction. Most methods return a new version of the text, except those
    that give non-text results (e.g. pos tagging)
    """
    pass
