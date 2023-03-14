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
Provide a simple CLI wrapper for JiWER. The CLI does not support custom transforms.
"""

import click
import pathlib

import jiwer


@click.command()
@click.option(
    "--gt",
    "ground_truth_file",
    type=pathlib.Path,
    required=True,
    help="Path to new-line delimited text file of ground-truth sentences.",
)
@click.option(
    "--hp",
    "hypothesis_file",
    type=pathlib.Path,
    required=True,
    help="Path to new-line delimited text file of hypothesis sentences.",
)
@click.option(
    "--cer",
    "-c",
    "compute_cer",
    is_flag=True,
    default=False,
    help="Compute CER instead of WER.",
)
@click.option(
    "--align",
    "-a",
    "show_alignment",
    is_flag=True,
    default=False,
    help="Print alignment of each sentence.",
)
@click.option(
    "--global",
    "-g",
    "global_alignment",
    is_flag=True,
    default=False,
    help="Apply a global alignment between ground-truth and hypothesis sentences "
    "before computing the WER.",
)
def cli(
    ground_truth_file: pathlib.Path,
    hypothesis_file: pathlib.Path,
    compute_cer: bool,
    show_alignment: bool,
    global_alignment: bool,
):
    """
    JiWER is a python tool for computing the word-error-rate of ASR systems. To use
    this CLI, store the ground-truth and hypothesis sentences in a text file, where
    each sentence is delimited by a new-line character.
    The text files are expected to have an equal number of lines, unless the `-j` flag
    is used. The `-j` flag joins computation of the WER by doing a global alignment.

    """
    with ground_truth_file.open("r") as f:
        gt_sentences = [ln.strip() for ln in f.readlines() if len(ln.strip()) > 1]

    with hypothesis_file.open("r") as f:
        hp_sentences = [ln.strip() for ln in f.readlines() if len(ln.strip()) > 1]

    if not global_alignment and len(gt_sentences) != len(hp_sentences):
        raise ValueError(
            f"Number of sentences does not match. "
            f"{ground_truth_file} contains {len(gt_sentences)} lines."
            f"{hypothesis_file} contains {len(hp_sentences)} lines."
        )

    if global_alignment and compute_cer:
        raise ValueError("--global and --cer are mutually exclusive.")

    if compute_cer:
        out = jiwer.compute_measures(
            gt_sentences,
            hp_sentences,
            truth_transform=jiwer.cer_default,
            hypothesis_transform=jiwer.cer_default,
        )
        out["cer"] = out["wer"]
        del out["wer"]
    else:
        if global_alignment:
            out = jiwer.compute_measures(
                gt_sentences,
                hp_sentences,
                truth_transform=jiwer.wer_contiguous,
                hypothesis_transform=jiwer.wer_contiguous,
            )
        else:
            out = jiwer.compute_measures(gt_sentences, hp_sentences)

    if show_alignment:
        print(jiwer.visualize_measures(out, visualize_cer=compute_cer))
    else:
        if "wer" in out:
            print(out["wer"])
        elif "cer" in out:
            print(out["cer"])


if __name__ == "__main__":
    cli()
