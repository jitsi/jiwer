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




