#
# JiWER - Jitsi Word Error Rate
#
# Copyright @ 2018 - present 8x8, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This file implements methods for calculating the WER between a ground-truth
sentence and a hypothesis sentence, commonly a measure of performance for a
automatic speech recognition system
"""

import Levenshtein

from typing import Union, List

import jiwer.transforms as tr

__all__ = ["wer"]

################################################################################
# Implementation of the WER method, exposed publicly

_default_transform = tr.Compose(
    [
        tr.RemoveMultipleSpaces(),
        tr.Strip(),
        tr.SentencesToListOfWords(),
        tr.RemoveEmptyStrings(),
    ]
)

_standardize_transform = tr.Compose(
    [
        tr.ToLowerCase(),
        tr.ExpandCommonEnglishContractions(),
        tr.RemoveKaldiNonWords(),
        tr.RemoveWhiteSpace(replace_by_space=True),
    ]
)


def wer(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    **kwargs
) -> float:
    """
    Calculate the WER between between a set of ground-truth sentences and a set of
    hypothesis sentences.

    The set of sentences can be given as a string or a list of strings. A string
    input is assumed to be a single sentence. A list of strings is assumed to be
    multiple sentences. Each word in a sentence is separated by one or more spaces.
    A sentence is not expected to end with a specific token (such as a `.`). If
    the ASR does delimit sentences it is expected that these tokens are filtered out.

    The optional `transforms` arguments can be used to apply pre-processing to
    respectively the ground truth and hypotheses input. Note that the transform
    should ALWAYS include `SentencesToListOfWords`, as that is the expected input.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :return: the WER as a floating number between 0 and 1
    """
    # deal with old API
    if "standardize" in kwargs:
        truth = _standardize_transform(truth)
        hypothesis = _standardize_transform(hypothesis)
    if "words_to_filter" in kwargs:
        t = tr.RemoveSpecificWords(kwargs["words_to_filter"])
        truth = t(truth)
        hypothesis = t(hypothesis)

    # Apply transforms. By default, it collapses input to a list of words
    truth = truth_transform(truth)
    hypothesis = hypothesis_transform(hypothesis)

    # raise an error if the ground truth is empty
    if len(truth) == 0:
        raise ValueError("the ground truth cannot be an empty")

    # tokenize each word into an integer
    vocabulary = set(truth + hypothesis)
    word2char = dict(zip(vocabulary, range(len(vocabulary))))

    truth_chars = [chr(word2char[w]) for w in truth]
    hypothesis_chars = [chr(word2char[w]) for w in hypothesis]

    # now that the words are tokenized, we can do alignment
    distance = _edit_distance(truth_chars, hypothesis_chars)

    # and the WER is simply distance divided by the length of the truth
    n = len(truth_chars)
    error_rate = distance / n

    return error_rate


################################################################################
# Implementation of helper methods


def _edit_distance(a: List[str], b: List[str]) -> int:
    """
    Calculate the edit distance between two lists of words.

    :param a: a list of words, representing one or more sentences.
    :param b: another list of words, representing one or more sentences
    :return: the number of substitutions, insertions or deletions to apply to get from a to b
    """
    return Levenshtein.distance("".join(a), "".join(b))
