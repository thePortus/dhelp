#!/usr/bin/python

import unittest

from bs4 import BeautifulSoup

from ..web import WebPage


class TestWebPage(unittest.TestCase):

    def test_fetch(self):
        # ensure request returns text data
        page = WebPage('https://stackoverflow.com', options={'silent': True})
        return self.assertTrue(len(page.fetch()) > 0)

    def test_soup(self):
        # ensure object is a BeautifulSoup type object
        page = WebPage('https://stackoverflow.com', options={'silent': True})
        return self.assertTrue(type(page.soup()) == BeautifulSoup)

    def test_max_retries(self):
        # should return none after hitting max_retries getting invalid page
        page = WebPage(
            'http://0.0.0.0',
            options={
                'silent': True,
                'max_retries': 3
            }
        )
        return self.assertEqual(page.fetch(), None)

    def test_context_manager(self):
        # ensure soup works when invoked using with.. as.. context manager
        results = None
        page = WebPage('https://stackoverflow.com', options={'silent': True})
        with page as page_soup:
            results = page_soup
        return self.assertTrue((type(results)) == BeautifulSoup)
