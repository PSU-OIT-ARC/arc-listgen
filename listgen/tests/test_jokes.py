from unittest import TestCase

from listgen import jokes

class TestJoke(TestCase):
    def test_is_string(self):
        s = jokes.joke()
        self.assertTrue(isinstance(s, str))
