# JiWER

JiWER is a simple and fast python package to evaluate an automatic speech recognition system.
It supports the following measures:

1. word error rate (WER)
2. match error rate (MER)
3. word information lost (WIL) 
4. word information preserved (WIP) 
5. character error rate (CER)

These measures are computed with the use of the minimum-edit distance between one or more reference and hypothesis sentences.
The minimum-edit distance is calculated using [RapidFuzz](https://github.com/maxbachmann/RapidFuzz), which uses C++ under the hood, and is therefore faster than a pure python implementation.

# Installation

You should be able to install this package using [uv](https://docs.astral.sh/uv/): 

```
$ uv add jiwer
```

Or, if you prefer old-fashioned pip and you're using Python >= `3.8`:

```bash
$ pip install jiwer
```

## A note on empty references

There is undefined behaviour when you apply an empty reference and hypothesis pair
to the WER formula, as you get a division by zero.

As of version 4.0, `jiwer` defines the behaviour as follows, and thereby also
lifts the requirement for reference strings to be non-empty.
This allows for testing whether models hallucinate on silent audio.
Note that usually, there are multiple reference and hypothesis pairs.
It now supported that one or more of these references are empty, but to test well,
most references should still be non-empty.

```python3
import jiwer

# when ref and hyp are both empty, there is no error as
# an ASR system correctly predicted silence/non-speech.
assert jiwer.wer('', '') == 0 
assert jiwer.mer('', '') == 0
assert jiwer.wip('', '') == 1
assert jiwer.wil('', '') == 0

assert jiwer.cer('', '') == 0
```

When the hypothesis is non-empty, every word or character counts as an insertion:
```python3
import jiwer

assert jiwer.wer('', 'silence') == 1
assert jiwer.wer('', 'peaceful silence') == 2
assert jiwer.process_words('', 'now defined behaviour').insertions == 3

assert jiwer.cer('', 'a') == 1
assert jiwer.cer('', 'abcde') == 5
```
