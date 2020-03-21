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

import re

import numpy as np

from typing import Union, List
from itertools import chain

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

SPECIAL_EMPTY_HYPOTHESIS_TOKEN = "SPECIALEMPTYHYPOTHESISTOKENTHISWORDCANNEVERHAPPENINREALLIFEOK"


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

    # make sure the WER can be computed if the hypothesis is an empty string
    if len(hypothesis) == 0:
        hypothesis = [SPECIAL_EMPTY_HYPOTHESIS_TOKEN]

    # Create the list of vocabulary used
    vocab = {w: i for i, w in enumerate(set(chain(truth, hypothesis)))}

    # recreate the truth and hypothesis string as a list of integer tokens
    t = [vocab[w] for w in truth]
    h = [vocab[w] for w in hypothesis]

    # now that the words are tokenized, we can do alignment
    distance = _edit_distance(t, h)

    # and the WER is simply distance divided by the length of the truth
    n = len(truth)
    error_rate = distance / n

    return error_rate


################################################################################
# Implementation of helper methods


def _edit_distance(a: List[int], b: List[int]) -> int:
    """
    Calculate the edit distance between two lists of integers according to the
    Wagner-Fisher algorithm. Reference:
    https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm)

    :param a: the list of integers representing a string, where each integer is
    a single character or word
    :param b: the list of integers representing the string to compare distance
    with
    :return: the calculated distance
    """
    if len(a) == 0:
        raise ValueError("the reference string (called a) cannot be empty!")
    elif len(b) == 0:
        return len(a)

    # Initialize the matrix/table and set the first row and column equal to
    # 1, 2, 3, ...
    # Each column represent a single token in the reference string a
    # Each row represent a single token in the reference string b
    #
    m = np.zeros((len(b) + 1, len(a) + 1)).astype(dtype=np.int32)

    m[0, 1:] = np.arange(1, len(a) + 1)
    m[1:, 0] = np.arange(1, len(b) + 1)

    # Now loop over remaining cell (from the second row and column onwards)
    # The value of each selected cell is:
    #
    #   if token represented by row == token represented by column:
    #       value of the top-left diagonal cell
    #   else:
    #       calculate 3 values:
    #            * top-left diagonal cell + 1 (which represents substitution)
    #            * left cell + 1 (representing deleting)
    #            * top cell + 1 (representing insertion)
    #       value of the smallest of the three
    #
    for i in range(1, m.shape[0]):
        for j in range(1, m.shape[1]):
            if a[j - 1] == b[i - 1]:
                m[i, j] = m[i - 1, j - 1]
            else:
                m[i, j] = min(m[i - 1, j - 1] + 1, m[i, j - 1] + 1, m[i - 1, j] + 1)

    # and the minimum-edit distance is simply the value of the down-right most
    # cell

    return m[len(b), len(a)]
