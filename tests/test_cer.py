import unittest
import pytest

import jiwer

from .test_measures import assert_dict_almost_equal


class TestCERInputMethods(unittest.TestCase):
    def test_input_ref_string_hyp_string(self):
        cases = [
            ("This is a test", "This is a test", 0 / 14),
            ("This is a test", "", 14 / 14),
            ("This is a test", "This test", 5 / 14),
        ]

        self._apply_test_on(cases)

    def test_input_ref_string_hyp_list(self):
        cases = [
            ("This is a test", ["This is a test"], 0 / 14),
            ("This is a test", [""], 14 / 14),
            ("This is a test", ["This test"], 5 / 14),
        ]

        self._apply_test_on(cases)

    def test_input_ref_list_hyp_string(self):
        cases = [
            (["This is a test"], "This is a test", 0 / 14),
            (["This is a test"], "", 14 / 14),
            (["This is a test"], "This test", 5 / 14),
        ]

        self._apply_test_on(cases)

    def test_input_ref_list_hyp_list(self):
        cases = [
            (["This is a test"], ["This is a test"], 0 / 14),
            (["This is a test"], [""], 14 / 14),
            (["This is a test"], ["This test"], 5 / 14),
        ]

        self._apply_test_on(cases)

    def test_fail_on_different_sentence_length(self):
        def callback():
            jiwer.cer(["hello", "this", "sentence", "is fractured"], ["this sentence"])

        self.assertRaises(ValueError, callback)

    def test_fail_on_empty_reference(self):
        def callback():
            jiwer.cer("", "test")

        self.assertRaises(ValueError, callback)

    def test_known_values(self):
        # Taken from the "From WER and RIL to MER and WIL" paper, for link see README.md
        cases = [
            (
                "X",
                "X",
                0,
            ),
            (
                "X",
                "X X Y Y",
                6,
            ),
            (
                "X Y X",
                "X Z",
                3 / 5,
            ),
            (
                "X",
                "Y",
                1,
            ),
            (
                "X",
                "Y Z",
                3,
            ),
        ]

        self._apply_test_on(cases)

    def test_permutations_invariance(self):
        cases = [
            (
                ["i", "am i good"],
                ["i am", "i good"],
                0.6,
            ),
            (
                ["am i good", "i"],
                [
                    "i good",
                    "i am",
                ],
                0.6,
            ),
        ]

        self._apply_test_on(cases)

    def test_return_dict(self):
        # TODO: remove unit test once deprecated
        with pytest.deprecated_call():
            return_dict = jiwer.cer(
                ["i", "am i good"], ["i am", "y good"], return_dict=True
            )

        assert_dict_almost_equal(
            self,
            return_dict,
            {
                "cer": 0.7,
                "hits": 6,
                "substitutions": 1,
                "deletions": 3,
                "insertions": 3,
            },
            delta=1e-16,
        )

    def _apply_test_on(self, cases):
        for ref, hyp, correct_cer in cases:
            cer = jiwer.cer(reference=ref, hypothesis=hyp)

            self.assertTrue(isinstance(cer, float))
            if isinstance(cer, float):
                self.assertAlmostEqual(cer, correct_cer, delta=1e-16)
