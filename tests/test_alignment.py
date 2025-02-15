import unittest

import jiwer

from jiwer import visualize_alignment


class TestAlignmentVisualizationWords(unittest.TestCase):
    def test_insertion(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: this is a ****
HYP: this is a test
                  I
"""

        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a", "this is a test"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_deletion(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: this is a test
HYP: this is a ****
                  D
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test", "this is a"), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_substitution(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: this  is a test
HYP: this was a test
            S       
"""

        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test", "this was a test"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_all_three(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: this  is a ***** test of skill
HYP: this was a messy test ** *****
            S       I       D     D
"""

        alignment = jiwer.visualize_alignment(
            jiwer.process_words("this is a test of skill", "this was a messy test"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_show_measures(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: this test will have a high word error rate
HYP:   no   it will  not * **** **** ***** ****
        S    S         S D    D    D     D    D

=== SUMMARY ===
number of sentences: 1
substitutions=3 deletions=5 insertions=0 hits=1

mer=88.89%
wil=97.22%
wip=2.78%
wer=88.89%
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(
                "this test will  have a high word error rate", "no it will not"
            ),
            show_measures=True,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_hypothesis(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: empty
HYP: *****
         D
"""
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
        correct_alignment = """=== SENTENCE 1 ===

REF: one
HYP:   1
       S

=== SENTENCE 2 ===

REF: two
HYP:   2
       S
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(["one", "two"], ["1", "2"]),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_skip_correct(self):
        correct_alignment = """=== SENTENCE 2 ===

REF: one
HYP:   1
       S

=== SENTENCE 3 ===

REF: two
HYP:   2
       S
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words(
                ["perfect", "one", "two", "three"], ["perfect", "1", "2", "three"]
            ),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_ref(self):
        correct_alignment = ""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("", ""),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_ref_with_hyp_deletion(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: ********
HYP: inserted
            I
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_words("", "inserted"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_line_width(self):
        correct = """=== SENTENCE 1 ===

REF: this sentence could be
HYP: this sentence  will be
                       S   

REF: split ** **
HYP: split by ai
            I  I
"""
        alignment = visualize_alignment(
            jiwer.process_words(
                "this sentence could be split", "this sentence will be split by ai"
            ),
            line_width=30,
            show_measures=False,
        )
        self.assertEqual(correct, alignment)


class TestAlignmentVisualizationCharacters(unittest.TestCase):
    def test_insertion(self):
        correct_alignment = (
            "=== SENTENCE 1 ===\n\n"
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
            "=== SENTENCE 1 ===\n\n"
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
            "=== SENTENCE 1 ===\n\n"
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
            "=== SENTENCE 1 ===\n\n"
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
            "=== SENTENCE 1 ===\n\n"
            "REF: this test will  have a high word error rate\n"
            "HYP: no** i**t will n*************o***********t*\n"
            "     SSDD SDD       SDDDDDDDDDDDDD DDDDDDDDDDD D\n"
            "\n=== SUMMARY ===\n"
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
        correct_alignment = """=== SENTENCE 1 ===

REF: empty
HYP: *****
     DDDDD
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("empty", ""), show_measures=False
        )
        self.assertEqual(alignment, correct_alignment)

    def test_multiple_sentences(self):
        correct_alignment = (
            "=== SENTENCE 1 ===\n\n"
            "REF: one\n"
            "HYP: 1**\n"
            "     SDD\n"
            "\n"
            "=== SENTENCE 2 ===\n\n"
            "REF: two\n"
            "HYP: 2**\n"
            "     SDD\n"
        )
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters(["one", "two"], ["1", "2"]),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_ref(self):
        correct_alignment = ""
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("", ""),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_empty_ref_with_hyp_deletion(self):
        correct_alignment = """=== SENTENCE 1 ===

REF: ********
HYP: inserted
     IIIIIIII
"""
        alignment = jiwer.visualize_alignment(
            jiwer.process_characters("", "inserted"),
            show_measures=False,
        )
        self.assertEqual(alignment, correct_alignment)

    def test_line_width(self):
        correct = """=== SENTENCE 1 ===

REF: this sentence could be sp
HYP: this sentence will* be sp
                   SSS D      

REF: lit******
HYP: lit by ai
        IIIIII
"""
        alignment = visualize_alignment(
            jiwer.process_characters(
                "this sentence could be split", "this sentence will be split by ai"
            ),
            line_width=30,
            show_measures=False,
        )
        self.assertEqual(correct, alignment)
