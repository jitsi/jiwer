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
Utility method to visualize the alignment as returned by `jiwer.compute_measures()`.
"""

from typing import Dict, List, Tuple

__all__ = ["visualize_measures"]


def visualize_measures(measure_output: Dict, visualize_cer: bool = False) -> str:
    """
    Given the output dictionary of `jiwer.compute_measures()`, construct a string which
    visualizes the alignment between all pairs of ground-truth and hypothesis pairs.

    The constructed string also include the values of all measures. If `visualize_cer`
    is given, the output dictionary is expected to have come from the `jiwer.cer()`
    method instead.
    """
    if visualize_cer and "cer" not in measure_output:
        raise ValueError(
            f"visualize_cer={visualize_cer} while measure dictionary does not contain CER"
        )
    if not visualize_cer and "cer" in measure_output:
        raise ValueError(f"visualize_cer={visualize_cer} while measure dictionary contains CER")

    truth = measure_output["truth"]
    hypo = measure_output["hypothesis"]
    ops = measure_output["ops"]

    final_str = ""
    for idx, (gt, hp, o) in enumerate(zip(truth, hypo, ops)):
        final_str += f"sentence {idx+1}\n"
        final_str += _construct_comparison_string(
            gt, hp, o, visualize_cer=visualize_cer
        )
        final_str += "\n"

    final_str += f"number of sentences: {len(ops)}\n"
    final_str += f"substitutions={measure_output['substitutions']} "
    final_str += f"deletions={measure_output['deletions']} "
    final_str += f"insertions={measure_output['insertions']} "
    final_str += f"hits={measure_output['hits']}\t\n"

    if visualize_cer:
        final_str += f"\ncer={measure_output['cer']*100:.2f}%"
    else:
        final_str += f"\nmer={measure_output['mer']*100:.2f}%"
        final_str += f"\nwil={measure_output['wil']*100:.2f}%"
        final_str += f"\nwip={measure_output['wip']*100:.2f}%"
        final_str += f"\nwer={measure_output['wer']*100:.2f}%"

    return final_str


def _construct_comparison_string(
    truth: List[str],
    hypothesis: List[str],
    ops: List[Tuple[str, int, int, int, int]],
    visualize_cer: bool = False,
) -> str:
    ref_str = "REF: "
    hyp_str = "HYP: "
    op_str = "     "

    for op in ops:
        name, gt_start, gt_end, hp_start, hp_end = op

        if name == "equal" or name == "replace":
            ref = truth[gt_start:gt_end]
            hyp = hypothesis[hp_start:hp_end]
            op_char = " " if name == "equal" else "s"
        elif name == "delete":
            ref = truth[gt_start:gt_end]
            hyp = ["*" for _ in range(len(ref))]
            op_char = "d"
        elif name == "insert":
            hyp = hypothesis[hp_start:hp_end]
            ref = ["#" for _ in range(len(hyp))]
            op_char = "i"
        else:
            raise ValueError(f"unparseable op {name=}")

        op_chars = [op_char for _ in range(len(ref))]
        for gt, hp, c in zip(ref, hyp, op_chars):
            str_len = max(len(gt), len(hp), len(c))

            ref_str += f"{gt:>{str_len}}"
            hyp_str += f"{hp:>{str_len}}"
            op_str += f"{c.upper():>{str_len}}"

            if not visualize_cer:
                ref_str += " "
                hyp_str += " "
                op_str += " "

    return f"{ref_str}\n{hyp_str}\n{op_str}\n"
