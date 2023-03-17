# JiWER: Similarity measures for automatic speech recognition evaluation

This repository contains a simple python package to approximate the Word Error Rate (WER), Match Error Rate (MER), Word Information Lost (WIL) and Word Information Preserved (WIP) of a transcript.
It computes the minimum-edit distance between the ground-truth sentence and the hypothesis sentence of a speech-to-text API.
The minimum-edit distance is calculated using [RapidFuzz](https://github.com/maxbachmann/RapidFuzz), which uses C++ under the hood.

## Documentation

For further info, see the documentation at [nikvaessen.com/jiwer](https://nikvaessen.com/jiwer).

## Installation

You should be able to install this package using [poetry](https://python-poetry.org/docs/): 

```
$ poetry add jiwer
```

Or, if you prefer old-fashioned pip and you're using Python >= `3.7`:

```bash
$ pip install jiwer
```

## Usage

The most simple use-case is computing the edit distance between two strings:

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
