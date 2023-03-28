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
Convenience methods for calculating a number of similarity error
measures between a reference and hypothesis sentence.
These measures are
commonly used to measure the performance for an automatic speech recognition
(ASR) system.

The following measures are implemented:

- Word Error Rate (WER), which is where this library got its name from. This
  has long been (and arguably still is) the de facto standard for computing
  ASR performance.
- Match Error Rate (MER)
- Word Information Lost (WIL)
- Word Information Preserved (WIP)
- Character Error Rate (CER)

Note that these functions merely call
[jiwer.process_words][process.process_words] and
[jiwer.process_characters][process.process_characters].
It is more efficient to call `process_words` or `process_characters` and access the
results from the
[jiwer.WordOutput][process.WordOutput] and
[jiwer.CharacterOutput][process.CharacterOutput]
classes.
"""
import warnings

from typing import List, Union, Dict, Any

from jiwer import transforms as tr
from jiwer.transformations import wer_default, cer_default
from jiwer.process import process_words, process_characters

__all__ = [
    "wer",
    "mer",
    "wil",
    "wip",
    "cer",
    "compute_measures",
]

########################################################################################
# Implementation of the WER method and co, exposed publicly


def wer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    truth: Union[str, List[str]] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = None,
) -> float:
    """
    Calculate the word error rate (WER) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)
        truth: Deprecated, renamed to `reference`
        truth_transform: Deprecated, renamed to `reference_transform`

    Deprecated:
        Arguments `truth` and `truth_transform` have been renamed to respectively
        `reference` and `reference_transform`. Therefore, the keyword arguments
         `truth` and `truth_transform` will be removed in the next release.
         At the same time, `reference` and `reference_transform` will lose their
         default value.

    Returns:
        (float): The word error rate of the given reference and
                 hypothesis sentence(s).
    """
    (
        reference,
        hypothesis,
        reference_transform,
        hypothesis_transform,
    ) = _deprecate_truth(
        reference=reference,
        hypothesis=hypothesis,
        truth=truth,
        reference_transform=reference_transform,
        truth_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )
    return output.wer


def mer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    truth: Union[str, List[str]] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = None,
) -> float:
    """
    Calculate the match error rate (MER) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)
        truth: Deprecated, renamed to `reference`
        truth_transform: Deprecated, renamed to `reference_transform`

    Deprecated:
        Arguments `truth` and `truth_transform` have been renamed to respectively
        `reference` and `reference_transform`. Therefore, the keyword arguments
         `truth` and `truth_transform` will be removed in the next release.
         At the same time, `reference` and `reference_transform` will lose their
         default value.

    Returns:
        (float): The match error rate of the given reference and
                 hypothesis sentence(s).
    """
    (
        reference,
        hypothesis,
        reference_transform,
        hypothesis_transform,
    ) = _deprecate_truth(
        reference=reference,
        hypothesis=hypothesis,
        truth=truth,
        reference_transform=reference_transform,
        truth_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )

    return output.mer


def wip(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    truth: Union[str, List[str]] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = None,
) -> float:
    """
    Calculate the word information preserved (WIP) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)
        truth: Deprecated, renamed to `reference`
        truth_transform: Deprecated, renamed to `reference_transform`

    Deprecated:
        Arguments `truth` and `truth_transform` have been renamed to respectively
        `reference` and `reference_transform`. Therefore, the keyword arguments
         `truth` and `truth_transform` will be removed in the next release.
         At the same time, `reference` and `reference_transform` will lose their
         default value.

    Returns:
        (float): The word information preserved of the given reference and
                 hypothesis sentence(s).
    """
    (
        reference,
        hypothesis,
        reference_transform,
        hypothesis_transform,
    ) = _deprecate_truth(
        reference=reference,
        hypothesis=hypothesis,
        truth=truth,
        reference_transform=reference_transform,
        truth_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )

    return output.wip


def wil(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    truth: Union[str, List[str]] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = None,
) -> float:
    """
    Calculate the word information lost (WIL) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)
        truth: Deprecated, renamed to `reference`
        truth_transform: Deprecated, renamed to `reference_transform`

    Deprecated:
        Arguments `truth` and `truth_transform` have been renamed to respectively
        `reference` and `reference_transform`. Therefore, the keyword arguments
        `truth` and `truth_transform` will be removed in the next release.
         At the same time, `reference` and `reference_transform` will lose their
         default value.

    Returns:
        (float): The word information lost of the given reference and
                 hypothesis sentence(s).
    """
    (
        reference,
        hypothesis,
        reference_transform,
        hypothesis_transform,
    ) = _deprecate_truth(
        reference=reference,
        hypothesis=hypothesis,
        truth=truth,
        reference_transform=reference_transform,
        truth_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    output = process_words(
        reference, hypothesis, reference_transform, hypothesis_transform
    )

    return output.wil


########################################################################################
# deprecated method 'compute_measures'


def compute_measures(
    truth: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = wer_default,
) -> Dict[str, Any]:
    """
    Efficiently computes all measures using only one function call.

    Deprecated:
        Deprecated method. Superseded by [jiwer.process_words][process.process_words].
        This method will be removed on next release.

    Args:
        truth: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        truth_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)

    Returns:
        (dict): A dictionary containing key-value pairs for all measures.

    """
    warnings.warn(
        DeprecationWarning(
            "jiwer.compute_measures() is deprecated. Please use jiwer.process_words()."
        )
    )

    output = process_words(
        reference=truth,
        hypothesis=hypothesis,
        reference_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    return {
        "wer": output.wer,
        "mer": output.mer,
        "wil": output.wil,
        "wip": output.wip,
        "hits": output.hits,
        "substitutions": output.substitutions,
        "deletions": output.deletions,
        "insertions": output.insertions,
        "ops": output.alignments,
        "truth": output.references,
        "hypothesis": output.hypotheses,
    }


########################################################################################
# Implementation of character-error-rate, exposed publicly


def cer(
    reference: Union[str, List[str]] = None,
    hypothesis: Union[str, List[str]] = None,
    reference_transform: Union[tr.Compose, tr.AbstractTransform] = cer_default,
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform] = cer_default,
    return_dict: bool = False,
    truth: Union[str, List[str]] = None,
    truth_transform: Union[tr.Compose, tr.AbstractTransform] = None,
) -> Union[float, Dict[str, Any]]:
    """
    Calculate the character error rate (CER) between one or more reference and
    hypothesis sentences.

    Args:
        reference: The reference sentence(s)
        hypothesis: The hypothesis sentence(s)
        reference_transform: The transformation(s) to apply to the reference string(s)
        hypothesis_transform: The transformation(s) to apply to the hypothesis string(s)
        return_dict: Deprecated option to return the more results in a dict instead of
                     returning only the cer as a single float value
        truth: Deprecated, renamed to `reference`
        truth_transform: Deprecated, renamed to `reference_transform`

    Deprecated:
        Argument `return_dict` will be deprecated. Please use
        [jiwer.process_characters][process.process_characters] instead.

        Arguments `truth` and `truth_transform` have been renamed to respectively
        `reference` and `reference_transform`. Therefore, the keyword arguments
         `truth` and `truth_transform` will be removed in the next release.
         At the same time, `reference` and `reference_transform` will lose their
         default value.

    Returns:
        (float): The character error rate of the given reference and hypothesis
                 sentence(s).
    """
    (
        reference,
        hypothesis,
        reference_transform,
        hypothesis_transform,
    ) = _deprecate_truth(
        reference=reference,
        hypothesis=hypothesis,
        truth=truth,
        reference_transform=reference_transform,
        truth_transform=truth_transform,
        hypothesis_transform=hypothesis_transform,
    )

    output = process_characters(
        reference, hypothesis, reference_transform, hypothesis_transform
    )

    if return_dict:
        warnings.warn(
            DeprecationWarning(
                "`return_dict` is deprecated, "
                "please use jiwer.process_characters() instead."
            )
        )
        return {
            "cer": output.cer,
            "hits": output.hits,
            "substitutions": output.substitutions,
            "deletions": output.deletions,
            "insertions": output.insertions,
        }
    else:
        return output.cer


def _deprecate_truth(
    reference: Union[str, List[str]],
    hypothesis: Union[str, List[str]],
    truth: Union[str, List[str]],
    reference_transform: Union[tr.Compose, tr.AbstractTransform],
    hypothesis_transform: Union[tr.Compose, tr.AbstractTransform],
    truth_transform: Union[tr.Compose, tr.AbstractTransform],
):
    if truth is not None:
        warnings.warn(
            DeprecationWarning(
                "keyword argument `truth` is deprecated, please use `reference`."
            )
        )
        if reference is not None:
            raise ValueError("cannot give `reference` and `truth`")
        reference = truth
    if truth_transform is not None:
        warnings.warn(
            DeprecationWarning(
                "keyword argument `truth_transform` is deprecated, "
                "please use `reference_transform`."
            )
        )
        reference_transform = truth_transform

    if reference is None or hypothesis is None:
        raise ValueError(
            "detected default values for reference or hypothesis arguments, "
            "please provide actual string or list of strings"
        )

    return reference, hypothesis, reference_transform, hypothesis_transform
