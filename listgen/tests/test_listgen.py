from unittest import TestCase

import listgen

class TestJoke(TestCase):
    def test_is_string(self):
        s = listgen.joke()
        self.assertTrue(isinstance(s, str))
