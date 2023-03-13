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
  has long been (and arguably still is) the de facto standard for computing
  ASR performance.
- Match Error Rate (MER)
- Word Information Lost (WIL)
- Word Information Preserved (WIP)
"""
import rapidfuzz

from typing import Any, Dict, List, Tuple, Union
from itertools import chain

from rapidfuzz.distance import Editop, Editops, Opcodes

from jiwer import transforms as tr
from jiwer.transformations import wer_default, cer_default_transform

__all__ = [
    "wer",
    "mer",
    "wil",
    "wip",
    "cer",
    "compute_measures",
]

################################################################################
# Implementation of the WER method and co, exposed publicly


def wer(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate word error rate (WER) between a set of ground-truth sentences and
    a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WER as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform
    )
    return measures["wer"]


def mer(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate match error rate (MER) between a set of ground-truth sentences and
    a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: MER as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform
    )
    return measures["mer"]


def wip(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate Word Information Preserved (WIP) between a set of ground-truth
    sentences and a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WIP as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform
    )
    return measures["wip"]


def wil(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> float:
    """
    Calculate Word Information Lost (WIL) between a set of ground-truth sentences
    and a set of hypothesis sentences.

    See `compute_measures` for details on the arguments.

    :return: WIL as a floating point number
    """
    measures = compute_measures(
        truth, hypothesis, truth_transform, hypothesis_transform
    )
    return measures["wil"]


def compute_measures(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> Dict[str, float]:
    """
    Calculate error measures between a set of ground-truth sentences and a set of
    hypothesis sentences.

    The set of sentences can be given as a string or a list of strings. A string
    input is assumed to be a single sentence. A list of strings is assumed to be
    multiple sentences which need to be evaluated independently. Each word in a
    sentence is separated by one or more spaces. A sentence is not expected to end
    with a specific token (such as a `.`). If the ASR system does delimit sentences
    it is expected that these tokens are filtered out.

    The optional `transforms` arguments can be used to apply pre-processing to
    respectively the ground truth and hypotheses input. By default, the following
    transform is applied to both the ground truth and hypothesis string(s). These
    steps are required and necessary in order to compute the measures.

    1) The start and end of a string are stripped of white-space symbols
    2) Contiguous spaces (e.g `   `) are reduced to a single space (e.g ` `)
    3) A sentence (with a single space (` `) between words) is reduced to a
       list of words

    Any non-default transformation is required to reduce the input to at least
    one list of words in order to facility the computation of the edit distance.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :return: a dict with WER, MER, WIP and WIL measures as floating point numbers
    """
    # validate input type
    if isinstance(truth, str):
        truth = [truth]
    if isinstance(hypothesis, str):
        hypothesis = [hypothesis]
    if any(len(t) == 0 for t in truth):
        raise ValueError("one or more groundtruths are empty strings")

    # Preprocess truth and hypothesis
    (truth_transformed, truth_as_chars), (hp_transformed, hp_as_chars) = _preprocess(
        truth, hypothesis, truth_transform, hypothesis_transform
    )

    # keep track of total hits, substitutions, deletions and insertions
    # across all input sentences
    H, S, D, I = 0, 0, 0, 0

    # also keep track of the total number of ground truth words and hypothesis words
    gt_tokens, hp_tokens = 0, 0
    all_edit_ops = []
    all_ops = []

    for groundtruth_sentence, hypothesis_sentence in zip(truth_as_chars, hp_as_chars):
        # Get the operation counts (#hits, #substitutions, #deletions, #insertions)
        edit_ops = _get_edit_operations(groundtruth_sentence, hypothesis_sentence)
        edit_ops_list = edit_ops.as_list()

        substitutions = sum(1 if op[0] == "replace" else 0 for op in edit_ops_list)
        deletions = sum(1 if op[0] == "delete" else 0 for op in edit_ops_list)
        insertions = sum(1 if op[0] == "insert" else 0 for op in edit_ops_list)
        hits = len(groundtruth_sentence) - (substitutions + deletions)

        H += hits
        S += substitutions
        D += deletions
        I += insertions
        gt_tokens += len(groundtruth_sentence)
        hp_tokens += len(hypothesis_sentence)
        all_edit_ops.append(edit_ops_list)
        all_ops.append(Opcodes.from_editops(edit_ops).as_list())

    # Compute Word Error Rate
    wer = float(S + D + I) / float(H + S + D)

    # Compute Match Error Rate
    mer = float(S + D + I) / float(H + S + D + I)

    # Compute Word Information Preserved
    wip = (float(H) / gt_tokens) * (float(H) / hp_tokens) if hp_tokens >= 1 else 0

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
        "edits": all_edit_ops,
        "ops": all_ops,
        "truth": truth_transformed,
        "hypothesis": hp_transformed,
    }


################################################################################
# Implementation of character error rate


def cer(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = cer_default_transform,
    hypothesis_transform: Union[
        tr.Compose, tr.AbstractTransform
    ] = cer_default_transform,
    return_dict: bool = False,
) -> Union[float, Dict[str, Union[float, int]]]:
    """
    Calculate character error rate (CER) between a set of ground-truth sentences and
    a set of hypothesis sentences. By default, the CER includes space (` `) as a
    character over which the error rate is computed.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :param return_dict: when true, return a dictionary containing the CER and the number of
    insertions, deletions, substitution and hits between truth and hypothesis. When false,
    only return the CER as a floating point number
    :return: CER as a floating point number, or dictionary containing CER, #hits, #substitutions, #deletions and #insertions
    """
    r = compute_measures(truth, hypothesis, truth_transform, hypothesis_transform)

    result_dict = {
        "cer": r["wer"],
        "hits": r["hits"],
        "substitutions": r["substitutions"],
        "deletions": r["deletions"],
        "insertions": r["insertions"],
    }

    if return_dict:
        return result_dict
    else:
        return result_dict["cer"]


################################################################################
# Implementation of helper methods


def _preprocess(
    truth: List[str],
    hypothesis: List[str],
    truth_transform: Union[tr.Compose, tr.AbstractTransform],
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform],
) -> Tuple[Tuple[List[str], List[str]], Tuple[List[str], List[str]]]:
    """
    Pre-process the truth and hypothesis by applying the transforms, and then convert
    each word into a unique character such that we can compute the levenshtein distance
    on word-level, which is required to the word-error-rate.

    :param truth: the ground-truth sentence(s) as a string or list of strings
    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param truth_transform: the transformation to apply on the truths input
    :param hypothesis_transform: the transformation to apply on the hypothesis input
    :return: the preprocessed truth and hypothesis
    """
    # Apply transforms. The transforms should collapses input to a list of list of words
    transformed_truth = truth_transform(truth)
    transformed_hypothesis = hypothesis_transform(hypothesis)

    # raise an error if the ground truth is empty or the output
    # is not a list of list of strings
    if len(transformed_truth) != len(transformed_hypothesis):
        raise ValueError(
            "number of ground truth inputs ({}) and hypothesis inputs ({}) must match.".format(
                len(transformed_truth), len(transformed_hypothesis)
            )
        )
    if not _is_list_of_list_of_strings(transformed_truth, require_non_empty_lists=True):
        raise ValueError(
            "truth should be a list of list of strings after transform which are non-empty"
        )
    if not _is_list_of_list_of_strings(
        transformed_hypothesis, require_non_empty_lists=False
    ):
        raise ValueError(
            "hypothesis should be a list of list of strings after transform"
        )

    # tokenize each word into an integer
    vocabulary = set(chain(*transformed_truth, *transformed_hypothesis))

    if "" in vocabulary:
        raise ValueError(
            "Empty strings cannot be a word. "
            "Please ensure that the given transform removes empty strings."
        )

    word2char = dict(zip(vocabulary, range(len(vocabulary))))

    truth_chars = [
        "".join([chr(word2char[w]) for w in sentence]) for sentence in transformed_truth
    ]
    hypothesis_chars = [
        "".join([chr(word2char[w]) for w in sentence])
        for sentence in transformed_hypothesis
    ]

    return (transformed_truth, truth_chars), (transformed_hypothesis, hypothesis_chars)


def _is_list_of_list_of_strings(x: Any, require_non_empty_lists: bool):
    if not isinstance(x, list):
        return False

    for e in x:
        if not isinstance(e, list):
            return False

        if require_non_empty_lists and len(e) == 0:
            return False

        if not all([isinstance(s, str) for s in e]):
            return False

    return True


def _get_edit_operations(source_string: str, destination_string: str) -> Editops:
    """
    Check how many edit operations (delete, insert, replace) are required to
    transform the source string into the destination string. The number of hits
    can be given by subtracting the number of deletes and substitutions from the
    total length of the source string.

    :param source_string: the source string to transform into the destination string
    :param destination_string: the destination to transform the source string into
    :return: a list of operations (replace, delete, or insert) required to go from source to target string
    """
    editops = rapidfuzz.distance.Levenshtein.editops(source_string, destination_string)

    return editops
