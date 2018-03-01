#!/usr/bin/python

import os

import unittest


class AbstractBaseUnitTest(unittest.TestCase):
    test_class = None
    fixtures_path = None

    def make_test_obj(self, path=None):
        # build path from either fixtures_path or path if present
        if path and self.fixtures_path:
            path = os.path.join(self.fixtures_path, path)
        elif not path and self.fixtures_path:
            path = self.fixtures_path
        # if no path given in either place, raise exception
        elif not path and not self.fixtures_path:
            raise Exception('No fixtures_path or path specified for unittest.')
        return self.test_class(path)


if __name__ == "__main__":
    unittest.main()
