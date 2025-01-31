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

## Documentation

For further info, see the documentation at [jitsi.github.io/jiwer](https://jitsi.github.io/jiwer).

## Installation

You should be able to install this package using [uv](https://docs.astral.sh/uv/): 

```
$ uv add jiwer
```

Or, if you prefer old-fashioned pip and you're using Python >= `3.8`:

```bash
$ pip install jiwer
```

## Usage

The most simple use-case is computing the word error rate between two strings:

```python
from jiwer import wer

reference = "hello world"
hypothesis = "hello duck"

error = wer(reference, hypothesis)
```

## Licence

The jiwer package is released under the `Apache License, Version 2.0` licence by [8x8](https://www.8x8.com/).

For further information, see [`LICENCE`](./LICENSE).

## Reference

_For a comparison between WER, MER and WIL, see: \
Morris, Andrew & Maier, Viktoria & Green, Phil. (2004). [From WER and RIL to MER and WIL: improved evaluation measures for connected speech recognition.](https://www.researchgate.net/publication/221478089_From_WER_and_RIL_to_MER_and_WIL_improved_evaluation_measures_for_connected_speech_recognition)_
