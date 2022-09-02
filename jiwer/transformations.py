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

"""
This file is intended to provide the default transformation which need
to be applied to input text in order to compute the WER (or similar measures).

It also prevents some alternative transformations which might be
useful in specific use cases.
"""

import jiwer.transforms as tr

__all__ = [
    "wer_default",
    "wer_contiguous",
    "wer_standardize",
    "wer_standardize_contiguous",
    "cer_default_transform",
]

################################################################################
# implement transformations for WER (and accompanying measures)

wer_default = tr.Compose(
    [
        tr.RemoveMultipleSpaces(),
        tr.Strip(),
        tr.ReduceToListOfListOfWords(),
    ]
)

wer_contiguous = tr.Compose(
    [
        tr.RemoveMultipleSpaces(),
        tr.Strip(),
        tr.ReduceToSingleSentence(),
        tr.ReduceToListOfListOfWords(),
    ]
)


wer_standardize = tr.Compose(
    [
        tr.ToLowerCase(),
        tr.ExpandCommonEnglishContractions(),
        tr.RemoveKaldiNonWords(),
        tr.RemoveWhiteSpace(replace_by_space=True),
        tr.ReduceToListOfListOfWords(),
    ]
)

wer_standardize_contiguous = tr.Compose(
    [
        tr.ToLowerCase(),
        tr.ExpandCommonEnglishContractions(),
        tr.RemoveKaldiNonWords(),
        tr.RemoveWhiteSpace(replace_by_space=True),
        tr.ReduceToSingleSentence(),
        tr.ReduceToListOfListOfWords(),
    ]
)


################################################################################
# implement transformations for CER

cer_default_transform = tr.Compose(
    [
        tr.Strip(),
        tr.ReduceToListOfListOfChars(),
    ]
)
