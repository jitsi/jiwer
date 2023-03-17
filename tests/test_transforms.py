import unittest

from jiwer.transforms import *
from jiwer.transforms import ReduceToListOfListOfChars


def _apply_test_on(self: unittest.TestCase, tr, cases):
    for inp, outp in cases:
        self.assertEqual(outp, tr(inp))


class TestReduceToSingleSentence(unittest.TestCase):
    def test_normal(self):
        cases = [
            ("this is a test", "this is a test"),
            ("", ""),
            (["this is one", "is two"], ["this is one is two"]),
            (["one", "two", "three", "", "five six"], ["one two three five six"]),
            ([""], []),
        ]

        _apply_test_on(self, ReduceToSingleSentence(), cases)

    def test_delimiter(self):
        cases = [
            ("this_is_a_test", "this_is_a_test"),
            ("", ""),
            (["this_is_one", "is_two"], ["this_is_one_is_two"]),
            (["one", "two", "three", "", "five_six"], ["one_two_three_five_six"]),
            ([""], []),
        ]

        _apply_test_on(self, ReduceToSingleSentence("_"), cases)


class TestReduceToListOfListOfWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            ("this is a test", [["this", "is", "a", "test"]]),
            ("", [[]]),
            (["this is one", "is two"], [["this", "is", "one"], ["is", "two"]]),
            (
                ["one", "two", "three", "", "five six"],
                [["one"], ["two"], ["three"], [], ["five", "six"]],
            ),
            ([], [[]]),
            ([""], [[]]),
            (["", "", ""], [[], [], []]),
        ]

        _apply_test_on(self, ReduceToListOfListOfWords(), cases)

    def test_delimiter(self):
        cases = [
            ("this_is_a_test", [["this", "is", "a", "test"]]),
            ("", [[]]),
            (["this_is_one", "is_two"], [["this", "is", "one"], ["is", "two"]]),
            (
                ["one", "two", "three", "", "five_six"],
                [["one"], ["two"], ["three"], [], ["five", "six"]],
            ),
            ([], [[]]),
            ([""], [[]]),
            (["", "", ""], [[], [], []]),
        ]

        _apply_test_on(self, ReduceToListOfListOfWords("_"), cases)


class TestReduceToListOfListOfChars(unittest.TestCase):
    def test_normal(self):
        cases = [
            (
                "this is a test",
                [
                    [
                        "t",
                        "h",
                        "i",
                        "s",
                        " ",
                        "i",
                        "s",
                        " ",
                        "a",
                        " ",
                        "t",
                        "e",
                        "s",
                        "t",
                    ]
                ],
            ),
            ("", [[]]),
            (
                ["this is one", "is two"],
                [
                    ["t", "h", "i", "s", " ", "i", "s", " ", "o", "n", "e"],
                    ["i", "s", " ", "t", "w", "o"],
                ],
            ),
            (
                ["one", "two", "three", "", "five six"],
                [
                    ["o", "n", "e"],
                    ["t", "w", "o"],
                    ["t", "h", "r", "e", "e"],
                    [],
                    ["f", "i", "v", "e", " ", "s", "i", "x"],
                ],
            ),
            ([], [[]]),
            ([""], [[]]),
            (["", "", ""], [[], [], []]),
        ]

        _apply_test_on(self, ReduceToListOfListOfChars(), cases)

    def test_delimiter(self):
        cases = [
            (
                "this_is_a_test",
                [
                    [
                        "t",
                        "h",
                        "i",
                        "s",
                        "_",
                        "i",
                        "s",
                        "_",
                        "a",
                        "_",
                        "t",
                        "e",
                        "s",
                        "t",
                    ]
                ],
            ),
            ("", [[]]),
            (
                ["this_is_one", "is_two"],
                [
                    ["t", "h", "i", "s", "_", "i", "s", "_", "o", "n", "e"],
                    ["i", "s", "_", "t", "w", "o"],
                ],
            ),
            (
                ["one", "two", "three", "", "five_six"],
                [
                    ["o", "n", "e"],
                    ["t", "w", "o"],
                    ["t", "h", "r", "e", "e"],
                    [],
                    ["f", "i", "v", "e", "_", "s", "i", "x"],
                ],
            ),
            ([], [[]]),
            ([""], [[]]),
            (["", "", ""], [[], [], []]),
        ]

        _apply_test_on(self, ReduceToListOfListOfChars(), cases)


class TestRemoveSpecificWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["yhe about that bug"], ["  about that bug"]),
            (["yeah about that bug"], ["  about that bug"]),
            (["one bug"], ["one bug"]),
            (["yhe", "about", "bug"], [" ", "about", "bug"]),
            (["yeah", "about", "bug"], [" ", "about", "bug"]),
            (["one", "bug"], ["one", "bug"]),
            (["yhe about bug"], ["  about bug"]),
            (["yeah about bug"], ["  about bug"]),
            (["about bug yhe"], ["about bug  "]),
            (["one bug"], ["one bug"]),
            (["he asked a helpful question"], ["  asked   helpful question"]),
            (["normal sentence"], ["normal sentence"]),
            (["yhe awesome", "  awesome"]),
            (["the apple is not a pear", "  apple is not   pear"]),
            (["yhe", " "]),
        ]

        _apply_test_on(
            self, RemoveSpecificWords(["yhe", "yeah", "a", "he", "the"]), cases
        )


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
            (["this sentence has no punctuation", "this sentence has no punctuation"]),
        ]

        _apply_test_on(self, RemovePunctuation(), cases)

    def test_non_ascii_punctuation(self):
        cases = [
            (["word༆’'", "word"]),
            (["‘no’", "no"]),
            (["“yes”", "yes"]),
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


class TestSubstituteWords(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["you're pretty"], ["i am awesome"]),
            (["your book"], ["your book"]),
            (["foobar"], ["foobar"]),
        ]

        _apply_test_on(
            self,
            SubstituteWords(
                {"pretty": "awesome", "you": "i", "'re": " am", "foo": "bar"}
            ),
            cases,
        )


class TestSubstituteRegexes(unittest.TestCase):
    def test_normal(self):
        cases = [
            (["is the world doomed or loved?"], ["is the world sacr or lov?"]),
            (["the sun is loved"], ["the sun is lov"]),
            (["edibles are allegedly cultivated"], ["edibles are allegedly cultivat"]),
        ]

        _apply_test_on(
            self,
            SubstituteRegexes({r"doom": r"sacr", r"\b(\w+)ed\b": r"\1"}),
            cases,
        )


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
