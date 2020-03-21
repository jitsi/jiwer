import unittest

from jiwer.transforms import *


def _apply_test_on(self: unittest.TestCase, tr, cases):
    for inp, outp in cases:
        self.assertEqual(outp, tr(inp))


class TestSentencesToListOfWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            ("this is a test", ["this", "is", "a", "test"]),
            ("", [""]),
            (["this is one", "is two"], ["this", "is", "one", "is", "two"]),
            (["one", "two", "three", "", "five"], ["one", "two", "three", "", "five"]),
        ]

        _apply_test_on(self, SentencesToListOfWords(), cases)

    def test_delimiter(self):
        cases = [
            ("this_is_a_test", ["this", "is", "a", "test"]),
            ("", [""]),
            (["this_is_one", "is_two"], ["this", "is", "one", "is", "two"]),
            (["one", "two", "three", "", "five"], ["one", "two", "three", "", "five"]),
        ]

        _apply_test_on(self, SentencesToListOfWords("_"), cases)


class TestRemoveSpecificWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            ("yhe about that bug", " about that bug"),
            ("yeah about that bug", " about that bug"),
            ("one bug", "one bug"),
            (["yhe", "about", "bug"], ["", "about", "bug"]),
            (["yeah", "about", "bug"], ["", "about", "bug"]),
            (["one", "bug"], ["one", "bug"]),
            (["yhe about bug"], [" about bug"]),
            (["yeah about bug"], [" about bug"]),
            (["one bug"], ["one bug"]),
        ]

        _apply_test_on(self, RemoveSpecificWords(["yhe", "yeah"]), cases)


class TestRemoveWhiteSpace(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["this is an example", "thisisanexample"]),
            (["hello\tworld\n\r", "helloworld"]),
        ]

        _apply_test_on(self, RemoveWhiteSpace(), cases)

    def test_replace_by_space(self):
        cases = [
            (["this is an example", "this is an example"]),
            (["hello\tworld\n\r", "hello world  "]),
        ]

        _apply_test_on(self, RemoveWhiteSpace(replace_by_space=True), cases)


class TestRemovePunctuation(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["this is an example!", "this is an example"]),
            (["hello. goodbye", "hello goodbye"]),
        ]

        _apply_test_on(self, RemovePunctuation(), cases)


class TestRemoveMultipleSpaces(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["this is   an   example "], ["this is an example "]),
            (["  hello goodbye  "], [" hello goodbye "]),
            (["  "], [" "]),
        ]

        _apply_test_on(self, RemoveMultipleSpaces(), cases)

    pass


class TestStrip(unittest.TestCase):
    def test_normal(self):
        cases = [
            ([" this is an example "], ["this is an example"]),
            (["  hello goodbye  "], ["hello goodbye"]),
            (["  "], [""]),
            (["                       "], [""]),
        ]

        _apply_test_on(self, Strip(), cases)


class TestRemoveEmptyStrings(unittest.TestCase):
    def test_normal(self):
        cases = [
            ([""], []),
            (["this is an example"], ["this is an example"]),
            ([" "], []),
            (["                "], []),
        ]

        _apply_test_on(self, RemoveEmptyStrings(), cases)


class TestExpandCommonEnglishContractions(unittest.TestCase):
    def test_normal(self):
        cases = [
            (
                ["she'll make sure you can't make it"],
                ["she will make sure you can not make it"],
            ),
            (["let's party!"], ["let us party!"]),
        ]

        _apply_test_on(self, ExpandCommonEnglishContractions(), cases)


class TestToLowerCase(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["You're PRETTY"], ["you're pretty"]),
        ]

        _apply_test_on(self, ToLowerCase(), cases)


class TestToUpperCase(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["You're amazing"], ["YOU'RE AMAZING"]),
        ]

        _apply_test_on(self, ToUpperCase(), cases)


class TestRemoveKaldiNonWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["you <unk> like [laugh]"], ["you  like "]),
        ]

        _apply_test_on(self, RemoveKaldiNonWords(), cases)
