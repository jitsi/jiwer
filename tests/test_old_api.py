import unittest
import jiwer


class TestOldAPI(unittest.TestCase):
    def test_standardize(self):
        ground_truth = "he's my neminis"
        hypothesis = "he is my <unk> [laughter]"

        x = jiwer.wer(ground_truth, hypothesis, standardize=True)

        # is equivalent to
        ground_truth = "he is my neminis"
        hypothesis = "he is my"

        y = jiwer.wer(ground_truth, hypothesis)

        self.assertEqual(x, y)

    def test_words_to_filter(self):
        ground_truth = "yhe about that bug"
        hypothesis = "yeah about that bug"

        x = jiwer.wer(ground_truth, hypothesis, words_to_filter=["yhe", "yeah"])

        # is equivalent to

        ground_truth = "about that bug"
        hypothesis = "about that bug"

        y = jiwer.wer(ground_truth, hypothesis)

        self.assertEqual(x, y)
