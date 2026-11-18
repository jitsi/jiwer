import pytest

import jiwer


@pytest.mark.parametrize(
    "replacement",
    [r"\1", r"\g<0>", r"\alpha", r"C:\new\test", "plain text", "α"],
)
def test_substitute_words_preserves_literal_replacement(replacement):
    transform = jiwer.SubstituteWords({"token": replacement})

    assert transform("token tokenizer token") == (
        f"{replacement} tokenizer {replacement}"
    )


def test_substitute_regexes_keeps_backreference_support():
    transform = jiwer.SubstituteRegexes({r"(token)": r"\1ized"})

    assert transform("token") == "tokenized"
