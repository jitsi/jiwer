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
Utility method to visualize the alignment between one or more reference and hypothesis
pairs.
"""

from typing import Dict, List, Tuple, Union


from jiwer.process import CharacterOutput, WordOutput, AlignmentChunk

__all__ = ["visualize_alignment", "get_alignment_words"]


def visualize_alignment(
    output: Union[WordOutput, CharacterOutput],
    show_measures: bool = True,
    skip_correct: bool = True,
) -> str:
    """
    Visualize the output of [jiwer.process_words][process.process_words] and
    [jiwer.process_characters][process.process_characters]. The visualization
    shows the alignment between each processed reference and hypothesis pair.
    If `show_measures=True`, the output string will also contain all measures in the
    output.

    Args:
        output: The processed output of reference and hypothesis pair(s).
        show_measures: If enabled, the visualization will include measures like the WER
                       or CER
        skip_correct: If enabled, the visualization will exclude correct reference and hypothesis pairs

    Returns:
        (str): The visualization as a string

    Example:
        This code snippet
        ```python
        import jiwer

        out = jiwer.process_words(
            ["short one here", "quite a bit of longer sentence"],
            ["shoe order one", "quite bit of an even longest sentence here"],
        )

        print(jiwer.visualize_alignment(out))
        ```
        will produce this visualization:
        ```txt
        sentence 1
        REF:    # short one here
        HYP: shoe order one    *
                I     S        D

        sentence 2
        REF: quite a bit of  #    #  longer sentence    #
        HYP: quite * bit of an even longest sentence here
                   D         I    I       S             I

        number of sentences: 2
        substitutions=2 deletions=2 insertions=4 hits=5

        mer=61.54%
        wil=74.75%
        wip=25.25%
        wer=88.89%
        ```

        When `show_measures=False`, only the alignment will be printed:

        ```txt
        sentence 1
        REF:    # short one here
        HYP: shoe order one    *
                I     S        D

        sentence 2
        REF: quite a bit of  #    #  longer sentence    #
        HYP: quite * bit of an even longest sentence here
                   D         I    I       S             I
        ```
    """
    references = output.references
    hypothesis = output.hypotheses
    alignment = output.alignments
    is_cer = isinstance(output, CharacterOutput)

    final_str = ""
    for idx, (gt, hp, chunks) in enumerate(zip(references, hypothesis, alignment)):
        if skip_correct and len(chunks) == 1 and chunks[0].type == "equal":
            continue

        final_str += f"sentence {idx+1}\n"
        final_str += _construct_comparison_string(gt, hp, chunks, include_space_separator=not is_cer)
        final_str += "\n"

    if show_measures:
        final_str += f"number of sentences: {len(alignment)}\n"
        final_str += f"substitutions={output.substitutions} "
        final_str += f"deletions={output.deletions} "
        final_str += f"insertions={output.insertions} "
        final_str += f"hits={output.hits}\n"

        if is_cer:
            final_str += f"\ncer={output.cer*100:.2f}%\n"
        else:
            final_str += f"\nmer={output.mer*100:.2f}%"
            final_str += f"\nwil={output.wil*100:.2f}%"
            final_str += f"\nwip={output.wip*100:.2f}%"
            final_str += f"\nwer={output.wer*100:.2f}%\n"
    else:
        # remove last newline
        final_str = final_str[:-1]

    return final_str


def _construct_comparison_string(
    reference: List[str],
    hypothesis: List[str],
    ops: List[AlignmentChunk],
    include_space_separator: bool = False,
) -> str:
    reference_str = "REF: "
    hypothesis_str = "HYP: "
    operation_str = "     "

    reference_words, hypothesis_words, operation_chars = get_alignment_words(reference, hypothesis, ops)

    for reference_word, hypothesis_word, operation_char in zip(reference_words, hypothesis_words, operation_chars):
        word_len = max(len(reference_word), len(hypothesis_word), len(operation_char))

        reference_str += f"{reference_word:>{word_len}}"
        hypothesis_str += f"{hypothesis_word:>{word_len}}"
        operation_str += f"{operation_char:>{word_len}}"

        if include_space_separator:
            reference_str += " "
            hypothesis_str += " "
            operation_str += " "

    if include_space_separator:
        # remove last space
        return f"{reference_str[:-1]}\n{hypothesis_str[:-1]}\n{operation_str[:-1]}\n"
    else:
        return f"{reference_str}\n{hypothesis_str}\n{operation_str}\n"


def get_alignment_words(
    reference: List[str], hypothesis: List[str], operations: List[AlignmentChunk]
) -> Tuple[List[str], List[str], List[str]]:
    """Generate aligned words and operation characters based on reference, hypothesis, and alignment operations.

    Args:
        reference (List[str]): The list of reference words.
        hypothesis (List[str]): The list of hypothesis words.
        operations (List[AlignmentChunk]): The list of alignment operations.

    Returns:
        Tuple[List[str], List[str], List[str]]: A tuple containing three lists:
            - reference_words: The aligned reference words.
            - hypothesis_words: The aligned hypothesis words.
            - operation_chars: The operation characters for each alignment (' ' for equal, 'S' for substitute,
                               'D' for delete, 'I' for insert).

    Raises:
        ValueError: If an unparsable operation type is encountered.
    """
    reference_words, hypothesis_words, operation_chars = [], [], []

    for operation in operations:
        if operation.type == "equal" or operation.type == "substitute":
            ref_chunk_words = reference[operation.ref_start_idx : operation.ref_end_idx]
            hyp_chunk_words = hypothesis[operation.hyp_start_idx : operation.hyp_end_idx]
            operation_char = " " if operation.type == "equal" else "S"
        elif operation.type == "delete":
            ref_chunk_words = reference[operation.ref_start_idx : operation.ref_end_idx]
            hyp_chunk_words = ["*" * len(word) for word in ref_chunk_words]
            operation_char = "D"
        elif operation.type == "insert":
            hyp_chunk_words = hypothesis[operation.hyp_start_idx : operation.hyp_end_idx]
            ref_chunk_words = ["*" * len(word) for word in hyp_chunk_words]
            operation_char = "I"
        else:
            raise ValueError(f"Unparsable operation: {operation.type}")

        operation_chars.extend([operation_char] * len(ref_chunk_words))
        reference_words.extend(ref_chunk_words)
        hypothesis_words.extend(hyp_chunk_words)

    return reference_words, hypothesis_words, operation_chars
