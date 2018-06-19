# Word Error Rate for automatic speech recognition

This repository contains a simple python package to approximate the WER of a transcript. It computes the minimum-edit distance 
between the ground-truth sentence and the hypothesis sentence of a speech-to-text API. The minimum-edit distance is calculated
using the 
[Wagner-Fisher](https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm) 
algorithm. Because this algorithm computes the character-level minimum-edit distance, every word in a sentence is assigned a
unique integer, and the edit-distance is computed over a string of integers. 

# Installation

You should be able to install this package using pip: 

```bash
$ pip install jiwer
```

# Usage

The most simple use-case is computing the edit distance between two strings:

```python
from jiwer import wer

ground_truth = "hello world"
hypothesis = "hello duck"

error = wer(ground_truth, hypothesis)
```

You can also compute the WER over multiple sentences:

```python
from jiwer import wer

ground_truth = ["hello world", "i like monthy python"]
hypothesis = ["hello duck", "i like python"]

error = wer(ground_truth, hypothesis)
```

When the amount of ground-truth sentences and hypothesis sentences differ, a minimum alignment is done over the merged sentence:

```python
ground_truth = ["hello world", "i like monthy python", "what do you mean, african or european swallow?"]
hypothesis = ["hello", "i like", "python", "what you mean swallow"]

# is equivelent to

ground_truth = "hello world i like monhty python what do you mean african or european swallow"
hypothesis = "hello i like python what you mean swallow"
```

# Additional preprocessing

Some additional preprocessing can be done on the input. By default, whitespace is removed, everything is set to lower-case,
`.` and `,` are removed, everything between `[]` and `<>` (common for Kaldi models) is removed and each word is tokenized by 
splitting by one or more spaces. Additionally, common abbreviations, such as `won't`, `let's`,`n't` will be expanded if 
`standardize=True` is passed along the `wer` method.

```python
from jiwer import wer

ground_truth = "he's my neminis"
hypothesis = "he is my <unk> [laughter]"

wer(ground_truth, hypothesis, standardize=True)

# is equivelent to 

ground_truth = "he is my neminis"
hypothesis = "he is my"

wer(ground_truth, hypothesis)
```

Also, there is an option give a list of words to remove from the 
transcription, such as "yhe", or "so". 

```python
from jiwer import wer

ground_truth = "yhe about that bug"
hypothesis = "yeah about that bug"

wer(ground_truth, hypothesis, words_to_filter=["yhe", "yeah"])

# is equivelent to 

ground_truth = "about that bug"
hypothesis = "about that bug"

wer(ground_truth, hypothesis)

```





