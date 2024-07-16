import unittest

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_returns_is_correct_true_ascii(self):
        response, answer, params = "A & Test", "A & Test", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A \\cdot \mathrm{Test}")
        self.assertFalse(result.get("feedback"))
    
    def test_xor_identity(self):
        response, answer, params = "A ^ B", "A & ~B | ~A & B", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A \\oplus B")
        self.assertFalse(result.get("feedback"))
