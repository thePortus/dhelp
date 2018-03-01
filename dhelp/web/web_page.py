#!/usr/bin/python

import time

from collections import UserString

import requests
from bs4 import BeautifulSoup


class WebPage(UserString):
    """
    Provides methods to download/parse a specified webpage. Merges the request
    package with BeautifulSoup functions to enable users to request/soup
    a page in a single line.
    """

    def __init__(self, url, options={}):
        # call parent constructor
        super().__init__(str)
        if type(url) is not str:
            raise Exception('URL must be a string')
        if 'delay' not in options:
            options['delay'] = 2
        if 'max_retries' not in options:
            options['max_retries'] = 0
        if 'silent' not in options:
            options['silent'] = False
        self.data = url
        self.delay = options['delay']
        self.max_retries = options['max_retries']
        self.silent = options['silent']

    def fetch(self, retry_counter=0):
        """
        Makes web request and returns HTML as string.
        """
        # print message unless silent option
        if not self.silent:
            print('Fetching', self.data)
        # enforce delay to reduce server load
        time.sleep(self.delay)
        # attempt to fetch web page
        try:
            request = requests.get(self.data)
        # if error in getting page, call self recursively to try again
        except Exception:
            print('Problem fetching', self.data)
            # if infinite retries is set, always try again
            if not self.max_retries:
                if not self.silent:
                    print('Retrying...')
                return self.fetch()
            # if below retry limit, return recursively and increment counter
            elif retry_counter <= self.max_retries:
                if not self.silent:
                    print('Retrying')
                return self.fetch(retry_counter=retry_counter+1)
            # otherwise retry limit has been hit, stop fetching
            else:
                if not self.silent:
                    print('Retry limit reached, skipping', self.data)
                return None
        # if everything ok, returning page html instead of the entire request
        return request.text

    def soup(self):
        """
        Invokes web request then returns a soup object loaded with page HTML
        """
        return BeautifulSoup(self.fetch(), 'html.parser')
