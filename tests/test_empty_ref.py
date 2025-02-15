import pytest

import jiwer


def test_empty_ref_empty_hyp():
    for i in range(10):
        if i == 0:
            ref = ""
            hyp = ""
        else:
            ref = [""] * i
            hyp = [""] * i

        out = jiwer.process_words(reference=ref, hypothesis=hyp)

        assert out.hits == 0
        assert out.deletions == 0
        assert out.insertions == 0
        assert out.substitutions == 0

        assert out.wer == 0
        assert out.mer == 0
        assert out.wip == 1
        assert out.wil == 0


def test_empty_ref():
    out = jiwer.process_words(reference="", hypothesis="hello")

    assert out.insertions == 1

    assert out.wer == 1
    assert out.mer == 1
    assert out.wip == 0
    assert out.wil == 1


def test_empty_ref_more():
    for i in range(2, 11):
        out = jiwer.process_words(
            reference="", hypothesis=" ".join(str(j) for j in range(i))
        )

        assert out.insertions == i

        assert out.wer == i
        assert out.mer == 1
        assert out.wip == 0
        assert out.wil == 1


def test_empty_hyp():
    out = jiwer.process_words(reference="hello", hypothesis="")

    assert out.deletions == 1

    assert out.wer == 1
    assert out.mer == 1
    assert out.wip == 0
    assert out.wil == 1


def test_multiple_one_empty_ref():
    out = jiwer.process_words(
        reference=["hello world", ""], hypothesis=["hello world", "done"]
    )

    assert out.insertions == 1
    assert out.wer == pytest.approx(1 / 2)
    assert out.mer == pytest.approx(1 / 3)
    assert out.wil == pytest.approx(1 / 3)
    assert out.wip == pytest.approx(2 / 3)


def test_one_empty_ref_and_hyp():
    out_without = jiwer.process_words(
        reference=["hello world"], hypothesis=["hello world"]
    )
    out_with = jiwer.process_words(
        reference=["hello world", ""], hypothesis=["hello world", ""]
    )

    assert out_without.hits == out_with.hits
    assert out_without.substitutions == out_with.substitutions
    assert out_without.insertions == out_with.insertions
    assert out_without.deletions == out_with.deletions

    assert out_without.wer == out_with.wer
    assert out_without.mer == out_with.mer
    assert out_without.wip == out_with.wip
    assert out_without.wil == out_with.wil


def test_cer_empty_ref():
    out = jiwer.process_characters("", "")
    assert out.cer == 0

    out = jiwer.process_characters("", "a")
    assert out.cer == 1

    out = jiwer.process_characters("", "abd")
    assert out.cer == 3

    out = jiwer.process_characters("a", "")
    assert out.cer == 1

    out = jiwer.process_characters("abc", "")
    assert out.cer == 1
