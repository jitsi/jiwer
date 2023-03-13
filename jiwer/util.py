from typing import Dict, List, Tuple

__all__ = ["visualize_measures"]


def visualize_measures(measure_output: Dict):
    truth = measure_output["truth"]
    hypo = measure_output["hypothesis"]
    ops = measure_output["ops"]

    final_str = ""
    for idx, (gt, hp, ops) in enumerate(zip(truth, hypo, ops)):
        final_str += f"sentence {idx+1}\n"
        final_str += alignment_as_str(gt, hp, ops)

    final_str += f"\nmer={measure_output['mer']*100:.2f}%"
    final_str += f"\nwil={measure_output['wil']*100:.2f}%"
    final_str += f"\nwip={measure_output['wip']*100:.2f}%"
    final_str += f"\nwer={measure_output['wer'] * 100:.2f}%"
    print(final_str)


def alignment_as_str(
    truth: List[str], hypothesis: List[str], ops: List[Tuple[str, int, int, int, int]]
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

            ref_str += f"{gt:>{str_len}} "
            hyp_str += f"{hp:>{str_len}} "
            op_str += f"{c.upper():>{str_len}} "

    return f"{ref_str}\n{hyp_str}\n{op_str}\n"
