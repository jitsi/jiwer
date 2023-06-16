import unittest
import jiwer


class TestAlignmentVisualizationWords(unittest.TestCase):
    def test_insertion(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this is a ****\n"
            "HYP: this is a test\n"
            "                  I\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a", "this is a test"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

        pass

    def test_deletion(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this is a test\n"
            "HYP: this is a ****\n"
            "                  D\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test", "this is a"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_substitution(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this  is a test\n"
            "HYP: this was a test\n"
            "            S       \n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test", "this was a test"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_all_three(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this  is a ***** test of skill\n"
            "HYP: this was a messy test ** *****\n"
            "            S       I       D     D\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test of skill", "this was a messy test"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_show_measures(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this test will have a high word error rate\n"
            "HYP:   no   it will  not * **** **** ***** ****\n"
            "        S    S         S D    D    D     D    D\n"
            "\n"
            "number of sentences: 1\n"
            "substitutions=3 deletions=5 insertions=0 hits=1\n"
            "\n"
            "mer=88.89%\n"
            "wil=97.22%\n"
            "wip=2.78%\n"
            "wer=88.89%\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(
                "this test will  have a high word error rate", "no it will not"
            ),
            show_measures=True,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_hypothesis(self):
        correct_alignment = "sentence 1\n" "REF: empty\n" "HYP: *****\n" "         D\n"
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("empty", ""), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_multiple_sentences(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: one\n"
            "HYP:   1\n"
            "       S\n"
            "\n"
            "sentence 2\n"
            "REF: two\n"
            "HYP:   2\n"
            "       S\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(["one", "two"], ["1", "2"]),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_skip_correct(self):
        correct_alignment = (
            "sentence 2\n"
            "REF: one\n"
            "HYP:   1\n"
            "       S\n"
            "\n"
            "sentence 3\n"
            "REF: two\n"
            "HYP:   2\n"
            "       S\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(
                ["perfect", "one", "two", "three"], ["perfect", "1", "2", "three"]
            ),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)


class TestAlignmentVisualizationCharacters(unittest.TestCase):
    def test_insertion(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this is a*****\n"
            "HYP: this is a test\n"
            "              IIIII\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("this is a", "this is a test"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

        pass

    def test_deletion(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this is a test\n"
            "HYP: this is a*****\n"
            "              DDDDD\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("this is a test", "this is a"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_substitution(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this is a test\n"
            "HYP: this iz a test\n"
            "           S       \n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("this is a test", "this iz a test"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_all_three(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this *is a tes*t of skill\n"
            "HYP: this was a messy te*st***\n"
            "          IS    S  IS SSD SDDD\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters(
                "this is a test of skill", "this was a messy test"
            ),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_show_measures(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: this test will  have a high word error rate\n"
            "HYP: no** i**t will n*************o***********t*\n"
            "     SSDD SDD       SDDDDDDDDDDDDD DDDDDDDDDDD D\n"
            "\n"
            "number of sentences: 1\n"
            "substitutions=4 deletions=29 insertions=0 hits=10\n"
            "\n"
            "cer=76.74%\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters(
                "this test will  have a high word error rate", "no it will not"
            ),
            show_measures=True,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_hypothesis(self):
        correct_alignment = "sentence 1\n" "REF: empty\n" "HYP: *****\n" "     DDDDD\n"
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("empty", ""), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_multiple_sentences(self):
        correct_alignment = (
            "sentence 1\n"
            "REF: one\n"
            "HYP: 1**\n"
            "     SDD\n"
            "\n"
            "sentence 2\n"
            "REF: two\n"
            "HYP: 2**\n"
            "     SDD\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters(["one", "two"], ["1", "2"]),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)
