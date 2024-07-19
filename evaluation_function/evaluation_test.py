import unittest
import json

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

    test_output = []

    # Utility to help extract test info for documentation:

    def docs_from_test(self, context):
        docs = {
            'response': context['response'],
            'answer': context['answer'],
            'params': context['params'],
            'is_correct': context['result'].get("is_correct"),
            'feedback': context['result'].get("feedback")
        }
        self.test_output.append(docs)

    # Tests

    def test_returns_is_correct_true_ascii(self):
        response, answer, params = "A & Test", "A & Test", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"),
                         "A \\cdot \mathrm{Test}")
        self.assertFalse(result.get("feedback"))
        self.docs_from_test(locals())

    def test_returns_negative(self):
        response, answer, params = "A | B", "A & B", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), False)
        self.assertEqual(result.get("response_latex"), "A + B")
        self.assertTrue(result.get("feedback"))
        self.docs_from_test(locals())

    def test_syntax_error(self):
        response, answer, params = "A £ B", "A & B", Params()

        try:
            evaluation_function(response, answer, params).to_dict()
            self.fail("Exception not raised for unexpected token")
        except:
            pass

    def test_xor_identity(self):
        response, answer, params = "A ^ B", "A & ~B | ~A & B", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A \\oplus B")
        self.assertFalse(result.get("feedback"))

    def test_nand_or(self):
        response, answer, params = "A | B", "~(~A & ~B)", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A + B")
        self.assertFalse(result.get("feedback"))

    def test_nand_or(self):
        response, answer, params = "A | B", "~(~A & ~B)", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A + B")
        self.assertFalse(result.get("feedback"))

    def test_nor_nand(self):
        response, answer, params = "~(A & B)", "~(~(~A | ~B))", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"),
                         "\\overline{\\left( A \\cdot B \\right)}")
        self.assertFalse(result.get("feedback"))

    def test_complex(self):
        response, answer, params = "A & B | B & C & (B | C)", "B & (A | C)", Params(
        )

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertFalse(result.get("feedback"))

    def test_brackets(self):
        response, answer, params = "(A)", "A", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), True)
        self.assertFalse(result.get("feedback"))

    @classmethod
    def tearDownClass(self):
        with open("docs/test_output.json", "w") as f:
            f.write(json.dumps({"test_results": self.test_output}))
