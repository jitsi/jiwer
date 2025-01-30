import pytest
from jiwer import process_words, wer


def test_basic_word_mapping():
    """Test that basic word mapping works correctly."""
    # Create a reference with 100 words where 50 are the same in hypothesis
    reference = ["same"] * 50 + ["ref_only"] * 50
    hypothesis = ["same"] * 50 + ["hyp_only"] * 50

    result = process_words(reference=reference, hypothesis=hypothesis)
    assert isinstance(result.wer, float)
    assert result.wer == 0.5  # 50% of words are different
    assert result.hits == 50  # 50 "same" matches


def test_vocabulary_size_limit():
    """Test processing with very large vocabulary (no size limit now)."""
    # Create a large vocabulary that would have exceeded the old chr() limit
    vocab_size = 0x110000  # 1,114,112 unique words

    # Split into reference and hypothesis
    reference = [f"word{i}" for i in range(vocab_size // 2)]
    hypothesis = [f"word{i}" for i in range(vocab_size // 2, vocab_size)]

    try:
        result = process_words(reference=reference, hypothesis=hypothesis)
        assert isinstance(result.wer, float)
        assert result.wer == 1.0  # All words are different
    except Exception as e:
        pytest.fail(f"Large vocabulary processing failed: {e}")


def test_wer_large_vocabulary():
    """Test WER calculation with very large vocabulary."""
    vocab_size = 0x110000  # 1,114,112 unique words, above the chr() limit

    reference = " ".join(f"word{i}" for i in range(vocab_size // 2))
    hypothesis = " ".join(f"word{i}" for i in range(vocab_size // 2, vocab_size))

    try:
        error_rate = wer(reference=reference, hypothesis=hypothesis)
        assert isinstance(error_rate, float)
        assert error_rate == 1.0  # All words are different
    except Exception as e:
        pytest.fail(f"WER calculation failed with large vocabulary: {e}")


def test_hash_collision_handling():
    """Test that hash collisions don't affect results."""
    # Create words that might have hash collisions
    reference = ["a" * i for i in range(1, 1001)]  # Start from 1 to avoid empty strings
    hypothesis = [
        "b" * i for i in range(1, 1001)
    ]  # Start from 1 to avoid empty strings

    try:
        result = process_words(reference=reference, hypothesis=hypothesis)
        assert isinstance(result.wer, float)
        assert result.wer > 0  # Should detect differences
    except Exception as e:
        pytest.fail(f"Hash collision test failed: {e}")
