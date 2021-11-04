import unittest
import jiwer


class TestCERInputMethods(unittest.TestCase):
    def test_input_gt_string_h_string(self):
        cases = [
            ("This is a test", "This is a test", ),
            ("This is a test", "", ),
            ("This is a test", "This test", ),
        ]

        self._apply_test_on(cases)

    def test_input_gt_string_h_list(self):
        cases = [
            ("This is a test", ["This is a test"], _m(0, 0, 0)),
            ("This is a test", [""], _m(1, 1, 1)),
            ("This is a test", ["This test"], _m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_string(self):
        cases = [
            (["This is a test"], "This is a test", _m(0, 0, 0)),
            (["This is a test"], "", _m(1, 1, 1)),
            (["This is a test"], "This test", _m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_list(self):
        cases = [
            (["This is a test"], ["This is a test"], _m(0, 0, 0)),
            (["This is a test"], [""], _m(1, 1, 1)),
            (["This is a test"], ["This test"], _m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_different_sentence_length(self):
        cases = [
            (
                ["hello", "this", "sentence", "is fractured"],
                ["this sentence"],
                _m(0.6, 0.6, 0.6),
            ),
            (
                "i am a short ground truth",
                "i am a considerably longer and very much incorrect hypothesis",
                _m(7 / 6, 0.7, 0.85),
            ),
        ]

        self._apply_test_on(cases)

        ground_truth = [
            "i like monthy python",
            "what do you mean african or european swallow",
        ]
        hypothesis = ["i like", "python", "what you mean", "or swallow"]
        x = jiwer.compute_measures(ground_truth, hypothesis)

        # is equivalent to

        ground_truth = (
            "i like monthy python what do you mean african or european swallow"
        )
        hypothesis = "i like python what you mean or swallow"
        y = jiwer.compute_measures(ground_truth, hypothesis)

        self.assertDictAlmostEqual(x, y, delta=1e-9)

    def test_fail_on_empty_ground_truth(self):
        for method in [
            jiwer.cer
        ]:

            def callback():
                method("", "test")

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
                3,
            ),
            (
                "X Y X",
                "X Z",
                1/3,
            ),
            (
                "X",
                "Y",
                1,
            ),
            (
                "X",
                "Y Z",
                2,
            ),
        ]

        self._apply_test_on(cases)

    def _apply_test_on(self, cases):
        for gt, h, correct_cer in cases:
            cer = jiwer.cer(truth=gt, hypothesis=h)

            self.assertAlmostEquals(cer, correct_cer, delta=1e-16)
