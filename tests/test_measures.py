import unittest

import pytest

import jiwer


def all_m(wer, mer, wil):
    return {
        "wer": wer,
        "mer": mer,
        "wip": 1 - wil,
        "wil": wil,
    }


def to_measure_dict(x: jiwer.WordOutput):
    return {"wer": x.wer, "mer": x.mer, "wip": x.wip, "wil": x.wil}


def assert_dict_almost_equal(
    test_case: unittest.TestCase, a, b, places=None, msg=None, delta=None
):
    test_case.assertIsInstance(a, dict)
    test_case.assertIsInstance(b, dict)
    test_case.assertEqual(set(a.keys()), set(b.keys()))

    for k in a.keys():
        test_case.assertAlmostEqual(a[k], b[k], places=places, msg=msg, delta=delta)


class TestMeasuresContiguousSentencesTransform(unittest.TestCase):
    def test_input_ref_string_hyp_string(self):
        cases = [
            ("This is a test", "This is a test", all_m(0, 0, 0)),
            ("This is a test", "", all_m(1, 1, 1)),
            ("This is a test", "This test", all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_ref_string_hyp_list(self):
        cases = [
            ("This is a test", ["This is a test"], all_m(0, 0, 0)),
            ("This is a test", [""], all_m(1, 1, 1)),
            ("This is a test", ["This test"], all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_ref_list_hyp_string(self):
        cases = [
            (["This is a test"], "This is a test", all_m(0, 0, 0)),
            (["This is a test"], "", all_m(1, 1, 1)),
            (["This is a test"], "This test", all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_ref_list_hyp_list(self):
        cases = [
            (["This is a test"], ["This is a test"], all_m(0, 0, 0)),
            (["This is a test"], [""], all_m(1, 1, 1)),
            (["This is a test"], ["This test"], all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_different_sentence_length_equal_type(self):
        cases = [
            (
                ["hello", "this", "sentence", "is fractured"],
                ["this sentence"],
                all_m(0.6, 0.6, 0.6),
            ),
            (
                "i am a short ground truth",
                "i am a considerably longer and very much incorrect hypothesis",
                all_m(7 / 6, 0.7, 0.85),
            ),
        ]

        self._apply_test_on(cases)

    def test_different_sentence_length_unequaL_type(self):
        reference = [
            "i like monthy python",
            "what do you mean african or european swallow",
        ]
        hypothesis = ["i like", "python", "what you mean", "or swallow"]
        x = jiwer.process_words(
            reference,
            hypothesis,
            reference_transform=jiwer.transformations.wer_contiguous,
            hypothesis_transform=jiwer.transformations.wer_contiguous,
        )
        x_dict = to_measure_dict(x)

        # is equivalent to

        reference = "i like monthy python what do you mean african or european swallow"
        hypothesis = "i like python what you mean or swallow"
        y = jiwer.process_words(
            reference,
            hypothesis,
            reference_transform=jiwer.transformations.wer_contiguous,
            hypothesis_transform=jiwer.transformations.wer_contiguous,
        )
        y_dict = to_measure_dict(y)

        assert_dict_almost_equal(self, x_dict, y_dict, delta=1e-9)

    def test_fail_on_empty_reference(self):
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
                all_m(0, 0, 0),
            ),
            (
                "X",
                "X X Y Y",
                all_m(3, 0.75, 0.75),
            ),
            (
                "X Y X",
                "X Z",
                all_m(2 / 3, 2 / 3, 5 / 6),
            ),
            (
                "X",
                "Y",
                all_m(1, 1, 1),
            ),
            (
                "X",
                "Y Z",
                all_m(2, 1, 1),
            ),
        ]

        self._apply_test_on(cases)

    def test_permutations_variance(self):
        cases = [
            (
                ["i", "am i good"],
                ["i am", "i good"],
                all_m(0.0, 0.0, 0),
            ),
            (
                ["am i good", "i"],
                [
                    "i good",
                    "i am",
                ],
                all_m(0.5, 0.4, 7 / 16),
            ),
        ]

        self._apply_test_on(cases)

    def _apply_test_on(self, cases):
        for ref, hyp, correct_measures in cases:
            output = jiwer.process_words(
                reference=ref,
                hypothesis=hyp,
                reference_transform=jiwer.transformations.wer_contiguous,
                hypothesis_transform=jiwer.transformations.wer_contiguous,
            )
            output_dict = to_measure_dict(output)

            assert_dict_almost_equal(self, output_dict, correct_measures, delta=1e-16)


class TestMeasuresDefaultTransform(unittest.TestCase):
    def test_input_gt_string_h_string(self):
        cases = [
            ("This is a test", "This is a test", all_m(0, 0, 0)),
            ("This is a test", "", all_m(1, 1, 1)),
            ("This is a test", "This test", all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_gt_string_h_list(self):
        cases = [
            ("This is a test", ["This is a test"], all_m(0, 0, 0)),
            ("This is a test", [""], all_m(1, 1, 1)),
            ("This is a test", ["This test"], all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_string(self):
        cases = [
            (["This is a test"], "This is a test", all_m(0, 0, 0)),
            (["This is a test"], "", all_m(1, 1, 1)),
            (["This is a test"], "This test", all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_input_gt_list_h_list(self):
        cases = [
            (["This is a test"], ["This is a test"], all_m(0, 0, 0)),
            (["This is a test"], [""], all_m(1, 1, 1)),
            (["This is a test"], ["This test"], all_m(0.5, 0.5, 0.5)),
        ]

        self._apply_test_on(cases)

    def test_fail_on_different_sentence_length(self):
        for method in [
            jiwer.process_words,
            jiwer.wer,
            jiwer.wil,
            jiwer.wip,
            jiwer.mer,
            jiwer.compute_measures,
        ]:

            def callback():
                method(["hello", "this", "sentence", "is fractured"], ["this sentence"])

            self.assertRaises(ValueError, callback)

    def test_fail_on_empty_reference(self):
        for method in [
            jiwer.process_words,
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
                all_m(0, 0, 0),
            ),
            (
                "X",
                "X X Y Y",
                all_m(3, 0.75, 0.75),
            ),
            (
                "X Y X",
                "X Z",
                all_m(2 / 3, 2 / 3, 5 / 6),
            ),
            (
                "X",
                "Y",
                all_m(1, 1, 1),
            ),
            (
                "X",
                "Y Z",
                all_m(2, 1, 1),
            ),
        ]

        self._apply_test_on(cases)

    def test_permutations_invariance(self):
        cases = [
            (
                ["i", "am i good"],
                ["i am", "i good"],
                all_m(0.5, 0.4, 7 / 16),
            ),
            (
                ["am i good", "i"],
                [
                    "i good",
                    "i am",
                ],
                all_m(0.5, 0.4, 7 / 16),
            ),
        ]

        self._apply_test_on(cases)

    def _apply_test_on(self, cases):
        for ref, hyp, correct_measures in cases:
            output = jiwer.process_words(reference=ref, hypothesis=hyp)
            output_dict = to_measure_dict(output)

            assert_dict_almost_equal(self, output_dict, correct_measures, delta=1e-16)

            with pytest.deprecated_call():
                output = jiwer.compute_measures(truth=ref, hypothesis=hyp)
                output_dict = {
                    "wer": output["wer"],
                    "mer": output["mer"],
                    "wil": output["wil"],
                    "wip": output["wip"],
                }
                assert_dict_almost_equal(
                    self, output_dict, correct_measures, delta=1e-16
                )

        self._apply_test_deprecated_truth(cases)

    def _apply_test_deprecated_truth(self, cases):
        with pytest.deprecated_call():
            for ref, hyp, correct_measures in cases:
                output_dict = {}
                for key, method in [
                    ("wer", jiwer.wer),
                    ("mer", jiwer.mer),
                    ("wil", jiwer.wil),
                    ("wip", jiwer.wip),
                ]:
                    output = method(truth=ref, hypothesis=hyp)
                    output_dict[key] = output

                assert_dict_almost_equal(
                    self, output_dict, correct_measures, delta=1e-16
                )

    def test_deprecated_truth_and_ref(self):
        for key, method in [
            ("wer", jiwer.wer),
            ("mer", jiwer.mer),
            ("wil", jiwer.wil),
            ("wip", jiwer.wip),
            ("cer", jiwer.cer),
        ]:
            with pytest.raises(ValueError):
                method(truth="ref", reference="truth", hypothesis="huh")
                method()
                method(truth="only truth")
                method(reference="only ref")
                method(hypothesis="only hypothesis")

    def test_deprecated_truth_and_ref_with_transform(self):
        wer_transform = jiwer.Compose(
            [
                jiwer.ToLowerCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.Strip(),
                jiwer.ReduceToListOfListOfWords(),
            ]
        )
        cer_transform = jiwer.Compose(
            [
                jiwer.ToLowerCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.Strip(),
                jiwer.ReduceToListOfListOfChars(),
            ]
        )

        for key, method in [
            ("wer", jiwer.wer),
            ("mer", jiwer.mer),
            ("wil", jiwer.wil),
            ("wip", jiwer.wip),
            ("cer", jiwer.cer),
        ]:
            if key == "cer":
                tr = cer_transform
            else:
                tr = wer_transform

            result = method(
                truth="This is a short Sentence with a few Words with upper and Lower cases",
                hypothesis="His is a short Sentence with a few Words with upper and Lower cases",
                truth_transform=tr,
                hypothesis_transform=tr,
            )
            result_same = method(
                reference="This is a short Sentence with a few Words with upper and Lower cases",
                hypothesis="His is a short Sentence with a few Words with upper and Lower cases",
                reference_transform=tr,
                hypothesis_transform=tr,
            )
            self.assertAlmostEqual(result, result_same)


def test_deprecate_compute_measures():
    # TODO: remove once deprecated
    with pytest.deprecated_call():
        jiwer.compute_measures("no more", "compute_measures")
