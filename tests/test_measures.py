import unittest
import jiwer


def _m(wer, mer, wil):
    return {
        "wer": wer,
        "mer": mer,
        "wip": 1 - wil,
        "wil": wil,
    }


def assertDictAlmostEqual(
    test_case: unittest.TestCase, a, b, places=None, msg=None, delta=None
):
    test_case.assertIsInstance(a, dict)
    test_case.assertIsInstance(b, dict)
    test_case.assertEqual(set(a.keys()), set(b.keys()))

    for k in a.keys():
        test_case.assertAlmostEqual(a[k], b[k], places=places, msg=msg, delta=delta)


class TestMeasuresContiguousSentencesTransform(unittest.TestCase):
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
        x = jiwer.compute_measures(
            ground_truth,
            hypothesis,
            truth_transform=jiwer.transformations.wer_contiguous,
            hypothesis_transform=jiwer.transformations.wer_contiguous,
        )

        # is equivalent to

        ground_truth = (
            "i like monthy python what do you mean african or european swallow"
        )
        hypothesis = "i like python what you mean or swallow"
        y = jiwer.compute_measures(
            ground_truth,
            hypothesis,
            truth_transform=jiwer.transformations.wer_contiguous,
            hypothesis_transform=jiwer.transformations.wer_contiguous,
        )

        assertDictAlmostEqual(self, x, y, delta=1e-9)

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

    def test_known_values(self):
        # Taken from the "From WER and RIL to MER and WIL" paper, for link see README.md
        cases = [
            (
                "X",
                "X",
                _m(0, 0, 0),
            ),
            (
                "X",
                "X X Y Y",
                _m(3, 0.75, 0.75),
            ),
            (
                "X Y X",
                "X Z",
                _m(2 / 3, 2 / 3, 5 / 6),
            ),
            (
                "X",
                "Y",
                _m(1, 1, 1),
            ),
            (
                "X",
                "Y Z",
                _m(2, 1, 1),
            ),
        ]

        self._apply_test_on(cases)

    def test_permutations_variance(self):
        cases = [
            (
                ["i", "am i good"],
                ["i am", "i good"],
                _m(0.0, 0.0, 0),
            ),
            (
                ["am i good", "i"],
                [
                    "i good",
                    "i am",
                ],
                _m(0.5, 0.4, 7 / 16),
            ),
        ]

        self._apply_test_on(cases)

    def _apply_test_on(self, cases):
        for gt, h, correct_measures in cases:
            measures = jiwer.compute_measures(
                truth=gt,
                hypothesis=h,
                truth_transform=jiwer.transformations.wer_contiguous,
                hypothesis_transform=jiwer.transformations.wer_contiguous,
            )
            # Remove entries we are not testing against
            [
                measures.pop(k)
                for k in [
                    "hits",
                    "substitutions",
                    "deletions",
                    "insertions",
                    "ops",
                    "truth",
                    "hypothesis",
                ]
            ]
            assertDictAlmostEqual(self, measures, correct_measures, delta=1e-16)


class TestMeasuresDefaultTransform(unittest.TestCase):
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

    def test_fail_on_different_sentence_length(self):
        for method in [
            jiwer.wer,
            jiwer.wil,
            jiwer.wip,
            jiwer.mer,
            jiwer.compute_measures,
        ]:

            def callback():
                method(["hello", "this", "sentence", "is fractured"], ["this sentence"])

            self.assertRaises(ValueError, callback)

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

    def test_known_values(self):
        # Taken from the "From WER and RIL to MER and WIL" paper, for link see README.md
        cases = [
            (
                "X",
                "X",
                _m(0, 0, 0),
            ),
            (
                "X",
                "X X Y Y",
                _m(3, 0.75, 0.75),
            ),
            (
                "X Y X",
                "X Z",
                _m(2 / 3, 2 / 3, 5 / 6),
            ),
            (
                "X",
                "Y",
                _m(1, 1, 1),
            ),
            (
                "X",
                "Y Z",
                _m(2, 1, 1),
            ),
        ]

        self._apply_test_on(cases)

    def test_permutations_invariance(self):
        cases = [
            (
                ["i", "am i good"],
                ["i am", "i good"],
                _m(0.5, 0.4, 7 / 16),
            ),
            (
                ["am i good", "i"],
                [
                    "i good",
                    "i am",
                ],
                _m(0.5, 0.4, 7 / 16),
            ),
        ]

        self._apply_test_on(cases)

    def _apply_test_on(self, cases):
        for gt, h, correct_measures in cases:
            measures = jiwer.compute_measures(truth=gt, hypothesis=h)
            # Remove entries we are not testing against
            [
                measures.pop(k)
                for k in [
                    "hits",
                    "substitutions",
                    "deletions",
                    "insertions",
                    "ops",
                    "truth",
                    "hypothesis",
                ]
            ]
            print(measures)
            assertDictAlmostEqual(self, measures, correct_measures, delta=1e-16)
