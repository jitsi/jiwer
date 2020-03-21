import unittest
import jiwer


class TestWERInputMethods(unittest.TestCase):
    def test_input_gt_string_h_string(self):
        cases = [
            ("This is a test", "This is a test", 0),
            ("This is a test", "", 1),
            ("This is a test", "This test", 0.5),
        ]

        self._apply_test_on(cases)

    def test_input_gt_string_h_list(self):
        cases = [
            ("This is a test", ["This is a test"], 0),
            ("This is a test", [""], 1),
            ("This is a test", ["This test"], 0.5),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_string(self):
        cases = [
            (["This is a test"], "This is a test", 0),
            (["This is a test"], "", 1),
            (["This is a test"], "This test", 0.5),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_list(self):
        cases = [
            (["This is a test"], ["This is a test"], 0),
            (["This is a test"], [""], 1),
            (["This is a test"], ["This test"], 0.5),
        ]

        self._apply_test_on(cases)

    def test_different_sentence_length(self):
        cases = [
            (["hello", "this", "sentence", "is fractured"], ["this sentence"], 0.6)
        ]

        self._apply_test_on(cases)

    def test_fail_on_empty_ground_truth(self):
        def callback():
            jiwer.wer("", "test")

        self.assertRaises(ValueError, callback)

    def _apply_test_on(self, cases):
        for gt, h, correct_wer in cases:
            wer = jiwer.wer(truth=gt, hypothesis=h)
            self.assertAlmostEqual(wer, correct_wer, delta=1e-16)
