#!/usr/bin/python

import unittest

from bs4 import BeautifulSoup

from ..web_page import WebPage


class TestWebPage(unittest.TestCase):
    page = WebPage('https://stackoverflow.com', options={'silent': True})

    def test_fetch(self):
        # ensure request returns text data
        return self.assertTrue(len(self.page.fetch()) > 0)

    def test_soup(self):
        # ensure object is a BeautifulSoup type object
        return self.assertTrue(type(self.page.soup()) == BeautifulSoup)
