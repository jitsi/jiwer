import unittest
import jiwer


def _m(wer, mer, wil):
    return {
        "wer": wer,
        "mer": mer,
        "wip": 1 - wil,
        "wil": wil,
    }


class TestWERInputMethods(unittest.TestCase):
    def test_input_gt_string_h_string(self):
        cases = [
            ("This is a test", "This is a test", _m(0, 0, 0)),
            ("This is a test", "", _m(1, 1, 1)),
            ("This is a test", "This test", _m(0.5, 0.5, 0.5)),
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
            jiwer.wer,
            jiwer.wil,
            jiwer.wip,
            jiwer.mer,
            jiwer.compute_measures,
        ]:

            def callback():
                method("", "test")

            self.assertRaises(ValueError, callback)

    def _apply_test_on(self, cases):
        for gt, h, correct_measures in cases:
            measures = jiwer.compute_measures(truth=gt, hypothesis=h)
            self.assertDictAlmostEqual(measures, correct_measures, delta=1e-16)

    def assertDictAlmostEqual(self, a, b, places=None, msg=None, delta=None):
        self.assertIsInstance(a, dict)
        self.assertIsInstance(b, dict)
        self.assertEqual(set(a.keys()), set(b.keys()))
        for k in a.keys():
            self.assertAlmostEqual(a[k], b[k], places=places, msg=msg, delta=delta)
