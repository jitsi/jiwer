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
This file implements methods for calculating a number of similarity error
measures between a ground-truth sentence and a hypothesis sentence, which are
commonly used to measure the performance for an automatic speech recognition
(ASR) system.

The following measures are implemented:

- Word Error Rate (WER), which is where this library got its name from. This
  has has long been (and arguably still is) the de facto standard for computing
  ASR performance.
- Match Error Rate (MER)
- Word Information Lost (WIL)
- Word Information Preserved (WIP)
"""

import Levenshtein

from typing import List, Mapping, Tuple, Union, Optional, Dict

import jiwer.transforms as tr

__all__ = ["wer", "mer", "wil", "wip", "compute_measures"]

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
    Calculate word error rate (WER) between a set of ground-truth sentences and
    a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WER as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform, **kwargs
    )
    return measures["wer"]


def mer(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    **kwargs
) -> float:
    """
    Calculate match error rate (MER) between a set of ground-truth sentences and
    a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: MER as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform, **kwargs
    )
    return measures["mer"]


def wip(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    **kwargs
) -> float:
    """
    Calculate Word Information Preserved (WIP) between a set of ground-truth
    sentences and a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WIP as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform, **kwargs
    )
    return measures["wip"]


def wil(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    **kwargs
) -> float:
    """
    Calculate Word Information Lost (WIL) between a set of ground-truth sentences
    and a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WIL as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform, **kwargs
    )
    return measures["wil"]


def compute_measures(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    weights: Optional[Dict[str, float]] = None,
    default_weight: Union[int,float] = 1,
    insertion_weight: Union[int,float] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = _default_transform,
    **kwargs
) -> Mapping[str, float]:
    """
    Calculate error measures between a set of ground-truth sentences and a set of
    hypothesis sentences.

    The set of sentences can be given as a string or a list of strings. A string
    input is assumed to be a single sentence. A list of strings is assumed to be
    multiple sentences. Each word in a sentence is separated by one or more spaces.
    A sentence is not expected to end with a specific token (such as a `.`). If
    the ASR does delimit sentences it is expected that these tokens are filtered out.
    
    Optional `weights` argument should be a dictionary of words and their corresponding
    (integer or float) weights. A word with weight x is treated as if it (and the 
    corresponding word in the aligned hypothesis string) were repeated x times in 
    the calculation of hits, substitutions and deletions. 
    Insertions always carry weight `insertion_weight` (by default this is equal to `default_weight`).
  
    Note that the weights are assigned AFTER preprocessing (see below).
    
    Words not present in the `weights` dictionary are given weight `default_weight`.
    This is set to 1 by default, but using a value of 0 would enable calculation
    of metrics like (W)KER which focus exclusively on specified keywords.

    The optional `transforms` arguments can be used to apply pre-processing to
    respectively the ground truth and hypotheses input. Note that the transform
    should ALWAYS include `SentencesToListOfWords`, as that is the expected input.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param weights: the dictionary of words and their corresponding (int or float) weights
    :param default_weight: the weight used for words not present in the weights dictionary
    :param insertion_weight: the 'cost' of an insertion operation. By default, equal to default_weight
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :return: a dict with WER, MER, WIP and WIL measures as floating point numbers
    """

    # deal with old API
    if "standardize" in kwargs:
        truth = _standardize_transform(truth)
        hypothesis = _standardize_transform(hypothesis)
    if "words_to_filter" in kwargs:
        t = tr.RemoveSpecificWords(kwargs["words_to_filter"])
        truth = t(truth)
        hypothesis = t(hypothesis)

    # Preprocess truth and hypothesis
    truth, hypothesis, w2c = _preprocess(
        truth, hypothesis, truth_transform, hypothesis_transform
    )

    # If weights dictionary or insertion_weight argument passed, perform weighted calculation
    # This is slower than the default version, so not used unless needed
    if weights or insertion_weight:
        
        # If no insertion_weight passed, set equal to default_weight
        if insertion_weight == None: 
            insertion_weight = default_weight
    
        # Mapping of word replacement characters to corresponding weights
        c2weight = {chr(v): weights[k] if k in weights else default_weight for k,v in w2c.items()}

        # Get the weighted operation counts (#hits, #substitutions, #deletions, #insertions)
        H, S, D, I = _get_weighted_operation_counts(truth, hypothesis, c2weight, insertion_weight)

        
    else:
        # Get the operation counts (#hits, #substitutions, #deletions, #insertions)
        H, S, D, I = _get_operation_counts(truth, hypothesis)


    # Compute Word Error Rate
    wer = float(S + D + I) / float(H + S + D)

    # Compute Match Error Rate
    mer = float(S + D + I) / float(H + S + D + I)

    # Compute Word Information Preserved
    #  Weighted N1 and N2 differ from the transformed string lengths
    wip = (float(H) / (H + S + D)) * (float(H) / (H + S + I)) if hypothesis else 0

    # Compute Word Information Lost
    wil = 1 - wip

    return {
        "wer": wer,
        "mer": mer,
        "wil": wil,
        "wip": wip,
        "hits": H,
        "substitutions": S,
        "deletions": D,
        "insertions": I,
    }


################################################################################
# Implementation of helper methods


def _preprocess(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform],
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform],
) -> Tuple[str, str]:
    """
    Pre-process the truth and hypothesis into a form that Levenshtein can handle.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :return: the preprocessed truth and hypothesis, and the word2char dictionary
    """

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

    truth_str = "".join(truth_chars)
    hypothesis_str = "".join(hypothesis_chars)

    return truth_str, hypothesis_str, word2char


def _get_operation_counts(
    source_string: str, destination_string: str
) -> Tuple[int, int, int, int]:
    """
    Check how many edit operations (delete, insert, replace) are required to
    transform the source string into the destination string. The number of hits
    can be given by subtracting the number of deletes and substitutions from the
    total length of the source string.

    :param source_string: the source string to transform into the destination string
    :param destination_string: the destination to transform the source string into
    :return: a tuple of #hits, #substitutions, #deletions, #insertions
    """

    editops = Levenshtein.editops(source_string, destination_string)

    substitutions = sum(1 if op[0] == "replace" else 0 for op in editops)
    deletions = sum(1 if op[0] == "delete" else 0 for op in editops)
    insertions = sum(1 if op[0] == "insert" else 0 for op in editops)
    hits = len(source_string) - (substitutions + deletions)

    return hits, substitutions, deletions, insertions
  
  
def _get_weighted_operation_counts(
    source_string: str, 
    destination_string: str,
    c2wmap: dict,
    insertion_weight: Union[int,float],
) -> Tuple[float, float, float, float]:
    """
    Check how many edit operations (delete, insert, replace) are required to
    transform the source string into the destination string.
    Non-insertion operations are weighted according to the character (originally a word) to which
    they are applied, per input mapping. Insertion operations all have weight insertion_weight.
    The number of hits can be given by subtracting the number of deletes and substitutions from the
    total (weighted) length of the source string.
    :param source_string: the source string to transform into the destination string
    :param destination_string: the destination to transform the source string into
    :param c2wmap: the character to weight mapping for the string contents
    :return: a tuple of (weighted) #hits, #substitutions, #deletions, #insertions
    """

    editops = Levenshtein.editops(source_string, destination_string)
    
    # Omit insert operations here, as they will universally receive weight insertion_weight and prevent uniqueness 
    #  of source position (whereas we will never both substitute and delete at the same source position).
    # Note that it might be desirable to penalise erroneous insertions of weighted keywords, but this would require a
    #  more complex iteration.
    edict = {spos:op for (op,spos,_) in editops if op != 'insert'}

    # Initialise weighted counts
    w_n = 0
    w_d = 0
    w_s = 0

    # Work through input (ground truth) string.
    #  Accumulate total weighted count (N)
    #  For non-insertion operations, accumulate corresponding weights
    for p,c in enumerate(source_string):

        _w = c2wmap[c]

        # Accumulate total weighted length
        w_n += _w

        # If there's a (non-insertion) operation at this position in truth, accumulate relevant operation count
        if p in edict:
            if edict[p] == 'replace': w_s += _w
            elif edict[p] == 'delete': w_d += _w
                
    # Count insertions
    w_i = sum(insertion_weight if op[0] == "insert" else 0 for op in editops)
    
    # Calculate hits
    w_h = w_n - (w_s + w_d)
        
    return w_h, w_s, w_d, w_i
