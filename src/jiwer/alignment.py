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

from typing import List, Union

from jiwer.process import CharacterOutput, WordOutput, AlignmentChunk

__all__ = ["visualize_alignment"]


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
        final_str += _construct_comparison_string(
            gt, hp, chunks, include_space_seperator=not is_cer
        )
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
    include_space_seperator: bool = False,
) -> str:
    ref_str = "REF: "
    hyp_str = "HYP: "
    op_str = "     "

    for op in ops:
        if op.type == "equal" or op.type == "substitute":
            ref = reference[op.ref_start_idx : op.ref_end_idx]
            hyp = hypothesis[op.hyp_start_idx : op.hyp_end_idx]
            op_char = " " if op.type == "equal" else "s"
        elif op.type == "delete":
            ref = reference[op.ref_start_idx : op.ref_end_idx]
            hyp = ["*" for _ in range(len(ref))]
            op_char = "d"
        elif op.type == "insert":
            hyp = hypothesis[op.hyp_start_idx : op.hyp_end_idx]
            ref = ["*" for _ in range(len(hyp))]
            op_char = "i"
        else:
            raise ValueError(f"unparseable op name={op.type}")

        op_chars = [op_char for _ in range(len(ref))]
        for rf, hp, c in zip(ref, hyp, op_chars):
            str_len = max(len(rf), len(hp), len(c))

            if rf == "*":
                rf = "".join(["*"] * str_len)
            elif hp == "*":
                hp = "".join(["*"] * str_len)

            ref_str += f"{rf:>{str_len}}"
            hyp_str += f"{hp:>{str_len}}"
            op_str += f"{c.upper():>{str_len}}"

            if include_space_seperator:
                ref_str += " "
                hyp_str += " "
                op_str += " "

    if include_space_seperator:
        # remove last space
        return f"{ref_str[:-1]}\n{hyp_str[:-1]}\n{op_str[:-1]}\n"
    else:
        return f"{ref_str}\n{hyp_str}\n{op_str}\n"
