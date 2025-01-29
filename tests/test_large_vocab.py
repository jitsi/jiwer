import pytest
from jiwer import process_words, wer

def test_basic_word_mapping():
    """Test that basic word mapping works correctly."""
    # Create a reference with 100 words where 50 are the same in hypothesis
    reference = ["same"] * 50 + ["ref_only"] * 50
    hypothesis = ["same"] * 50 + ["hyp_only"] * 50

    result = process_words(reference=reference, hypothesis=hypothesis)
    assert isinstance(result.wer, float)
    assert result.wer == 0.5  # Should detect exactly 50% difference
    assert result.hits == 50  # Should have 50 matching words

def test_vocabulary_size_limit():
    """Test that vocabularies exceeding Unicode limit are caught."""
    # Create a vocabulary that would exceed chr() limit (0x10FFFF)
    # We need the total unique words to be > 0x10FFFF
    # Using one more than the limit to trigger the error
    limit = 0x10FFFF

    # Create two lists with no overlap, each half the limit + 1
    # This ensures total unique words will be limit + 2
    half = (limit // 2) + 1
    reference = [f"ref{i}" for i in range(half)]
    hypothesis = [f"hyp{i}" for i in range(half)]  # All different from reference

    with pytest.raises(ValueError) as exc_info:
        process_words(reference=reference, hypothesis=hypothesis)

    assert "exceeds maximum allowed size" in str(exc_info.value)
    assert str(0x10FFFF) in str(exc_info.value)

def test_at_unicode_limit():
    """Test behavior exactly at the Unicode limit."""
    # Create exactly 0x10FFFF unique words total between ref and hyp
    limit = 0x10FFFF
    half = limit // 2

    # Split words between ref and hyp with no overlap
    # Total unique words will be exactly at the limit
    reference = [f"ref{i}" for i in range(half)]
    hypothesis = [f"hyp{i}" for i in range(limit - half)]  # Fills up to the limit

    # Make lists same length by repeating
    max_len = max(len(reference), len(hypothesis))
    reference = reference * (max_len // len(reference) + 1)
    hypothesis = hypothesis * (max_len // len(hypothesis) + 1)
    reference = reference[:max_len]
    hypothesis = hypothesis[:max_len]

    result = process_words(reference=reference, hypothesis=hypothesis)
    assert isinstance(result.wer, float)
    assert result.wer == 1.0  # All words should be different