import unittest

from .preview import Params, preview_function

class TestPreviewFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practice to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use preview_function() to check your algorithm works
    as it should.
    """

    def test_returns_preview_key(self):
        response, params = "A", Params()
        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])

    def test_returns_preview_sympy(self):
        response, params = "A | B", Params()

        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertEqual(result["preview"]["sympy"], "A | B")
        self.assertRaises(KeyError, lambda: result["preview"]["feedback"])

    def test_returns_preview_latex(self):
        response, params = "A & B", Params(is_latex=True)

        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertEqual(result["preview"]["latex"], "A \\cdot B")
        self.assertRaises(KeyError, lambda: result["preview"]["feedback"])

    def test_returns_none_not_parseable(self):
        response, params = "A u", Params()

        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"]["feedback"])
        self.assertRaises(KeyError, lambda: result["preview"]["sympy"])
        self.assertRaises(KeyError, lambda: result["preview"]["latex"])
