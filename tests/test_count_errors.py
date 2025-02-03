import jiwer

ref = ["sub", "sub", "sub", "sub", "sub", "this was", "del", "hit"]
hyp = ["bus", "bus", "bus", "usb", "bsu", "this was ins", "", "hit"]


def test_count_word_errors():
    correct = """=== SUBSTITUTIONS ===
sub --> bus = 3x
sub --> usb = 1x
sub --> bsu = 1x

=== INSERTIONS ===
ins = 1x

=== DELETIONS ===
del = 1x"""
    actual = jiwer.visualize_error_counts(jiwer.process_words(ref, hyp))
    assert correct == actual


def test_count_char_errors():
    correct = """=== SUBSTITUTIONS ===
s --> b = 3x
b --> s = 3x

=== INSERTIONS ===
u    = 1x
b    = 1x
 ins = 1x

=== DELETIONS ===
u   = 1x
b   = 1x
del = 1x"""

    actual = jiwer.visualize_error_counts(jiwer.process_characters(ref, hyp))
    assert actual == correct


def test_top_k():
    correct = """=== SUBSTITUTIONS ===
sub --> bus = 3x

=== INSERTIONS ===
ins = 1x

=== DELETIONS ===
del = 1x"""
    actual = jiwer.visualize_error_counts(jiwer.process_words(ref, hyp), top_k=1)
    assert correct == actual


def test_show_selective():
    no_sub = jiwer.visualize_error_counts(
        jiwer.process_words(ref, hyp), show_substitutions=False
    )
    no_ins = jiwer.visualize_error_counts(
        jiwer.process_words(ref, hyp), show_insertions=False
    )
    no_del = jiwer.visualize_error_counts(
        jiwer.process_words(ref, hyp), show_deletions=False
    )

    sub = "=== SUBSTITUTIONS ==="
    ins = "=== INSERTIONS ==="
    del_ = "=== DELETIONS ==="

    assert sub not in no_sub and ins in no_sub and del_ in no_sub
    assert sub in no_ins and ins not in no_ins and del_ in no_ins
    assert sub in no_del and ins in no_del and del_ not in no_del
