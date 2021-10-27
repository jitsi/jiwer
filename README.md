# JiWER: Similarity measures for automatic speech recognition evaluation

This repository contains a simple python package to approximate the Word Error Rate (WER), Match Error Rate (MER), Word Information Lost (WIL) and Word Information Preserved (WIP) of a transcript.
It computes the minimum-edit distance between the ground-truth sentence and the hypothesis sentence of a speech-to-text API.
The minimum-edit distance is calculated using the python C module [python-Levenshtein](https://github.com/ztane/python-Levenshtein).

_For a comparison between WER, MER and WIL, see: \
Morris, Andrew & Maier, Viktoria & Green, Phil. (2004). [From WER and RIL to MER and WIL: improved evaluation measures for connected speech recognition.](https://www.researchgate.net/publication/221478089_From_WER_and_RIL_to_MER_and_WIL_improved_evaluation_measures_for_connected_speech_recognition)_

# Installation

You should be able to install this package using [poetry](https://python-poetry.org/docs/): 

```
$ poetry add jiwer
```

Or, if you prefer old-fashioned pip and you're using Python >= `3.6`:

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

Similarly, to get other measures:

```python
import jiwer

ground_truth = "hello world"
hypothesis = "hello duck"

wer = jiwer.wer(ground_truth, hypothesis)
mer = jiwer.mer(ground_truth, hypothesis)
wil = jiwer.wil(ground_truth, hypothesis)

# faster, because `compute_measures` only needs to perform the heavy lifting once:
measures = jiwer.compute_measures(ground_truth, hypothesis)
wer = measures['wer']
mer = measures['mer']
wil = measures['wil']
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
ground_truth = ["i like monthy python", "what do you mean, african or european swallow"]
hypothesis = ["i like", "python", "what you mean" , "or swallow"]

# is equivalent to

ground_truth = "i like monthy python what do you mean african or european swallow"
hypothesis = "i like python what you mean or swallow"
```

# pre-processing

It might be necessary to apply some pre-processing steps on either the hypothesis or
ground truth text. This is possible with the transformation API:

```python
import jiwer

ground_truth = "I like  python!"
hypothesis = "i like Python?\n"

transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemoveWhiteSpace(replace_by_space=False),
    jiwer.SentencesToListOfWords(word_delimiter=" ")
]) 

jiwer.wer(
    ground_truth, 
    hypothesis, 
    truth_transform=transformation, 
    hypothesis_transform=transformation
)
```

By default, the following transformation is applied to both the ground truth and the hypothesis.
Note that is simply to get it into the right format to calculate the WER.

```python
default_transformation = jiwer.Compose([
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.SentencesToListOfWords(),
    jiwer.RemoveEmptyStrings()
])
```
### Transformations

#### Compose

`jiwer.Compose(transformations: List[Transform])` can be used to combine multiple transformations. 

Example:
```python
jiwer.Compose([
    jiwer.RemoveMultipleSpaces(),
    jiwer.SentencesToListOfWords()
])
```

#### SentencesToListOfWords

`jiwer.SentencesToListOfWords(word_delimiter=" ")` can be used to transform one or more sentences into a
list of words. The sentences can be given as a string (one sentence) or a list of strings (one or more sentences).

Example:
```python
sentences = ["hi", "this is an example"]

print(jiwer.SentencesToListOfWords()(sentences))
# prints: ['hi', 'this', 'is', 'an, 'example']
```

#### RemoveSpecificWords

`jiwer.RemoveSpecificWords(words_to_remove: List[str])` can be used to filter out certain words.

Example:
```python
sentences = ["yhe awesome", "the apple is not a pear", "yhe"]

print(jiwer.RemoveSpecificWords(["yhe", "the", "a"])(sentences))
# prints: ["awesome", "apple is pear", ""]
```

#### RemoveWhiteSpace

`jiwer.RemoveWhiteSpace(replace_by_space=False)` can be used to filter out white space.
The whitespace characters are ` `, `\t`, `\n`, `\r`, `\x0b` and `\x0c`.
Note that by default space (` `) is also removed, which will make it impossible to split a sentence into words by using `SentencesToListOfWords`.
This can be prevented by replacing all whitespace with the space character. 

Example:
```python
sentences = ["this is an example", "hello\tworld\n\r"]

print(jiwer.RemoveWhiteSpace()(sentences))
# prints: ["thisisanexample", "helloworld"]

print(jiwer.RemoveWhiteSpace(replace_by_space=True)(sentences))
# prints: ["this is an example", "hello world  "]
# note the trailing spaces
```

#### RemovePunctuation

`jiwer.RemovePunctuation()` can be used to filter out punctuation. The punctuation characters are:

``'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'``

Example:
```python
sentences = ["this is an example!", "hello. goodbye"]

print(jiwer.RemovePunctuation()(sentences))
# prints: ['this is an example', "hello goodbye"]
```

#### RemoveMultipleSpaces

`jiwer.RemoveMultipleSpaces()` can be used to filter out multiple spaces between words.

Example:
```python
sentences = ["this is   an   example ", "  hello goodbye  ", "  "]

print(jiwer.RemoveMultipleSpaces()(sentences))
# prints: ['this is an example ', " hello goodbye ", " "]
# note that there are still trailing spaces
```

#### Strip

`jiwer.Strip()` can be used to remove all leading and trailing spaces.

Example:
```python
sentences = [" this is an example ", "  hello goodbye  ", "  "]

print(jiwer.Strip()(sentences))
# prints: ['this is an example', "hello goodbye", ""]
# note that there is an empty string left behind which might need to be cleaned up
```


#### RemoveEmptyStrings

`jiwer.RemoveEmptyStrings()` can be used to remove empty strings.

Example:
```python
sentences = ["", "this is an example", " ",  "                "]

print(jiwer.RemoveEmptyStrings()(sentences))
# prints: ['this is an example']
```

#### ExpandCommonEnglishContractions

`jiwer.ExpandCommonEnglishContractions()` can be used to replace common contractions such as `let's` to `let us`.

Currently, this method will perform the following replacements. Note that `␣` is used to indicate a space (` `) to get
around markdown rendering constrains.

| Contraction   | transformed into |
| ------------- |:----------------:|
| `won't`       | `␣will not`      |
| `can't`       | `␣can not`       |
| `let's`       | `␣let us`        |
| `n't`         | `␣not`           |
| `'re`         | `␣are`           |
| `'s`          | `␣is`            |
| `'d`          | `␣would`         |
| `'ll`         | `␣will`          |
| `'t`          | `␣not`           |
| `'ve`         | `␣have`          |
| `'m`          | `␣am`            |

Example:
```python
sentences = ["she'll make sure you can't make it", "let's party!"]

print(jiwer.ExpandCommonEnglishContractions()(sentences))
# prints: ["she will make sure you can not make it", "let us party!"]
```

#### SubstituteWords

`jiwer.SubstituteWords(dictionary: Mapping[str, str])` can be used to replace a word into another word. Note that
the whole word is matched. If the word you're attempting to substitute is a substring of another word it will 
not be affected. 
For example, if you're substituting `foo` into `bar`, the word `foobar` will NOT be substituted into `barbar`.

Example:
```python
sentences = ["you're pretty", "your book", "foobar"]

print(jiwer.SubstituteWords({"pretty": "awesome", "you": "i", "'re": " am", 'foo': 'bar'})(sentences))

# prints: ["i am awesome", "your book", "foobar"]
```

#### SubstituteRegexes

`jiwer.SubstituteRegexes(dictionary: Mapping[str, str])` can be used to replace a substring matching a regex
 expression into another substring.

Example:
```python
sentences = ["is the world doomed or loved?", "edibles are allegedly cultivated"]

# note: the regex string "\b(\w+)ed\b", matches every word ending in 'ed', 
# and "\1" stands for the first group ('\w+). It therefore removes 'ed' in every match.
print(jiwer.SubstituteRegexes({r"doom": r"sacr", r"\b(\w+)ed\b": r"\1"})(sentences))

# prints: ["is the world sacr or lov?", "edibles are allegedly cultivat"]
```

#### ToLowerCase

`jiwer.ToLowerCase()` can be used to convert every character into lowercase.

Example:
```python
sentences = ["You're PRETTY"]

print(jiwer.ToLowerCase()(sentences))

# prints: ["you're pretty"]
```

#### ToUpperCase

`jiwer.ToUpperCase()` can be used to replace every character into uppercase.

Example:
```python
sentences = ["You're amazing"]

print(jiwer.ToUpperCase()(sentences))

# prints: ["YOU'RE AMAZING"]
```

#### RemoveKaldiNonWords

`jiwer.RemoveKaldiNonWords()` can be used to remove any word between `[]` and `<>`. This can be useful when working
with hypotheses from the Kaldi project, which can output non-words such as `[laugh]` and `<unk>`.

Example:
```python
sentences = ["you <unk> like [laugh]"]

print(jiwer.RemoveKaldiNonWords()(sentences))

# prints: ["you  like "]
# note the extra spaces
```
