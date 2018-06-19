#
# JiWER - Jitsi Word Error Rate
#
# Copyright @ 2018 Atlassian Pty Ltd
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

from typing import Union, List, Tuple
from itertools import chain

################################################################################
# Implementation of the WER method, exposed publicly


def wer(truth: Union[str, List[str], List[List[str]]],
        hypothesis: Union[str, List[str], List[List[str]]],
        standardize=False,
        words_to_filter=None
        ) -> float:
    """
    Calculate the WER between a ground-truth string and a hypothesis string

    :param truth the ground-truth sentence as a string or list of words
    :param hypothesis the hypothesis sentence as a string or list of words
    :param standardize whether to apply some standard rules to the given string
    :param words_to_filter a list of words to remove from the sentences
    :return: the WER, the distance (also known as the amount of
    substitutions, insertions and deletions) and the length of the ground truth
    """
    truth = _preprocess(truth)
    hypothesis = _preprocess(hypothesis)

    if len(truth) == 0:
        raise ValueError("truth needs to be a non-empty list of string")

    # Create the list of vocabulary used
    vocab = list()

    for w in chain(truth, hypothesis):
        if w not in vocab:
            vocab.append(w)

    # recreate the truth and hypothesis string as a list of tokens
    t = []
    h = []

    for w in truth:
        t.append(vocab.index(w))

    for w in hypothesis:
        h.append(vocab.index(w))

    # now that the words are tokenized, we can do alignment
    distance = _edit_distance(t, h)

    # and the WER is simply distance divided by the length of the truth
    n = len(truth)
    error_rate = distance / n

    return error_rate

################################################################################
# Implementation of helper methods, private to this package


_common_words_to_remove = ["yeah", "so", "oh", "ooh", "yhe"]


def _preprocess(text: Union[str, List[str], List[List[str]]],
                standardize:bool = False,
                words_to_remove=None):
    """
    Preprocess the input, be it a string, list of strings, or list of list of
    strings, such that the output is a list of strings.
    :param text:
    :return:
    """
    if isinstance(text, str):
        return _preprocess_text(text,
                                standardize=standardize,
                                words_to_remove=words_to_remove)
    elif len(text) == 0:
        raise ValueError("received empty list")
    elif len(text) == 1:
        return _preprocess(text[0])
    elif all(isinstance(e, str) for e in text):
        return _preprocess_text("".join(text), standardize=standardize,
                                words_to_remove=words_to_remove)
    elif all(isinstance(e, list) for e in text):
        for e in text:
            if not all(isinstance(f, str) for f in e):
                raise ValueError("The second list needs to only contain "
                                 "strings")
        return _preprocess_text("".join(["".join(e) for e in text]),
                                        standardize = standardize,
                                        words_to_remove=words_to_remove)
    else:
        raise ValueError("given list should only contain lists or list of "
                         "strings")


def _preprocess_text(phrase: str,
                     standardize: bool = False,
                     words_to_remove: List[str] = None)\
        -> List[str]:
    """
    Applies the following preprocessing steps on a string of text (a sentence):

    * optionally expands common abbreviated words such as he's into he is, you're into
    you are, ect
    * makes everything lowercase
    * tokenize words
    * optionally remove common words such as "yeah", "so"
    * change all numbers written as one, two, ... to 1, 2, ...
    * remove strings between [] and <>, such as [laughter] and <unk>

    :param s: the string, which is a sentence
    :param standardize: standardize the string by removing common abbreviations
    :param words_to_remove: remove words in this list from the phrase
    :return: the processed string
    """
    if type(phrase) is not str:
        raise ValueError("can only preprocess a string type, got {} of type {}"
                         .format(phrase, type(phrase)))

    # lowercase
    phrase = phrase.lower()

    # deal with abbreviated words
    if standardize:
        phrase = _standardise(phrase)

    # remove words between [] and <>
    phrase = re.sub('[<\[](\w)*[>\]]', "", phrase)

    # remove redundant white space
    phrase = phrase.strip()
    phrase = phrase.replace("\n", "")
    phrase = phrase.replace("\t", "")
    phrase = phrase.replace("\r", "")
    phrase = phrase.replace(",", "")
    phrase = phrase.replace(".", "")
    phrase = re.sub("\s\s+", " ", phrase)  # remove more than one space between words

    # tokenize
    phrase = phrase.split(" ")

    # remove common stop words (from observation):
    if words_to_remove is not None:
        for word_to_remove in words_to_remove:
            if word_to_remove in phrase:
                phrase.remove(word_to_remove)

    return phrase


def _standardise(phrase: str):
    """
    Standardise a phrase by removing common abbreviations from a sentence
    as well as making everything lowercase

    :param phrase: the sentence
    :return: the sentence with common stuff removed
    """
    # lowercase
    if not phrase.islower():
        phrase = phrase.lower()

    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"let\'s", "let us",  phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)

    return phrase


def _edit_distance(a: List[int], b:List[int]) -> int:
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
            if a[j-1] == b[i-1]:
                m[i, j] = m[i-1, j-1]
            else:
                m[i, j] = min(
                    m[i-1, j-1] + 1,
                    m[i, j - 1] + 1,
                    m[i - 1, j] + 1
                )

    # and the minimum-edit distance is simply the value of the down-right most
    # cell

    return m[len(b), len(a)]

################################################################################
# Main method used for debugging purposes


def main():
    r = "hello this is a nice day"
    h = "hello this a day"

    print(r, "\n", h, sep="")
    print(wer(r, h))


if __name__ == '__main__':
    main()
