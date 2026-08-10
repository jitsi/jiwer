import pathlib
import tempfile
import unittest

from click.testing import CliRunner

import jiwer

from jiwer.cli import cli


def write(path, text):
    path.write_text(text, encoding="utf-8")


class TestCli(unittest.TestCase):
    """Conformance tests for the `jiwer` CLI entry point.

    Every expected number below is derived on paper from
    WER = (S + D + I) / N_ref and CER = (S + D + I) / N_ref_chars
    *before* the CLI is run, and cross-checked against the public
    `jiwer.wer` / `jiwer.cer` API in the same test.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = pathlib.Path(self._tmpdir.name)

    def invoke(self, args):
        return CliRunner().invoke(cli, args)

    def test_wer_basic(self):
        # ref: "hello world" "good morning" -> 4 reference words total
        # hyp: "hello duck"  "good morning" -> 1 substitution (world -> duck)
        # WER = 1 / 4 = 0.25
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "hello world\ngood morning\n")
        write(hyp, "hello duck\ngood morning\n")

        result = self.invoke(["-r", str(ref), "-h", str(hyp)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), "0.25")

    def test_cer_basic(self):
        # ref: "abc" (3 characters), hyp: "abd" -> 1 substitution
        # CER = 1 / 3 = 0.3333333333333333
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "abc\n")
        write(hyp, "abd\n")

        result = self.invoke(["-c", "-r", str(ref), "-h", str(hyp)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), repr(1 / 3))

    def test_global_alignment_joins_lines(self):
        # ref: "a b" / "c d" (2 lines), hyp: "a b c d" (1 line): a plain
        # line-count comparison would fail (2 vs 1), but --global joins each
        # side into a single sentence: "a b c d" vs "a b c d" -> 4 hits,
        # 0 errors -> WER = 0.0
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "a b\nc d\n")
        write(hyp, "a b c d\n")

        result = self.invoke(["-g", "-r", str(ref), "-h", str(hyp)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), "0.0")

    def test_unequal_line_counts_without_global_raises(self):
        # Same inputs as above but WITHOUT --global: 2 reference lines
        # against 1 hypothesis line must be rejected with a message naming
        # both counts, per the CLI's documented purpose of the --global flag.
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "a b\nc d\n")
        write(hyp, "a b c d\n")

        result = self.invoke(["-r", str(ref), "-h", str(hyp)])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, ValueError)
        self.assertIn("2", str(result.exception))
        self.assertIn("1", str(result.exception))

    def test_blank_and_whitespace_only_lines_are_skipped(self):
        # A trailing blank line and a whitespace-only line must not change
        # the score: ref/hyp both reduce to "hello world" vs "hello there",
        # 1 substitution over 2 reference words -> WER = 0.5.
        ref_clean = self.tmp_path / "ref_clean.txt"
        hyp_clean = self.tmp_path / "hyp_clean.txt"
        ref_padded = self.tmp_path / "ref_padded.txt"
        hyp_padded = self.tmp_path / "hyp_padded.txt"

        write(ref_clean, "hello world\n")
        write(hyp_clean, "hello there\n")
        write(ref_padded, "hello world\n\n   \n")
        write(hyp_padded, "hello there\n\n   \n")

        result_clean = self.invoke(["-r", str(ref_clean), "-h", str(hyp_clean)])
        result_padded = self.invoke(["-r", str(ref_padded), "-h", str(hyp_padded)])

        self.assertEqual(result_clean.exit_code, 0, result_clean.output)
        self.assertEqual(result_padded.exit_code, 0, result_padded.output)
        self.assertEqual(result_clean.output, result_padded.output)
        self.assertEqual(result_clean.output.strip(), "0.5")

    def test_align_flag_matches_plain_wer(self):
        # --align must print a per-sentence alignment block and a SUMMARY
        # block, and the percentage it prints for "wer=" must equal the
        # plain (non---align) invocation's raw value, expressed as a
        # percentage to 2 decimal places (both come from the same
        # out.wer, so they must agree exactly).
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "hello world\n")
        write(hyp, "hello there\n")

        plain = self.invoke(["-r", str(ref), "-h", str(hyp)])
        aligned = self.invoke(["-a", "-r", str(ref), "-h", str(hyp)])

        self.assertEqual(plain.exit_code, 0, plain.output)
        self.assertEqual(aligned.exit_code, 0, aligned.output)
        self.assertIn("=== SENTENCE 1 ===", aligned.output)
        self.assertIn("=== SUMMARY ===", aligned.output)

        plain_wer = float(plain.output.strip())
        expected_pct = f"wer={plain_wer * 100:.2f}%"
        self.assertIn(expected_pct, aligned.output)

    def test_single_character_lines_are_not_dropped(self):
        # Regression test for the one-character-line filter bug: the CLI
        # used to keep only lines with len(line.strip()) > 1, silently
        # discarding every one-character sentence.
        #
        # ref: "a b" / "c", hyp: "a b" / "d" -> sentence 1 is 2 hits;
        # sentence 2 is 1 substitution (c -> d) over 1 reference word.
        # Corpus WER = 1 / 3 = 0.3333333333333333, matching the public API.
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "a b\nc\n")
        write(hyp, "a b\nd\n")

        expected = jiwer.wer(["a b", "c"], ["a b", "d"])
        result = self.invoke(["-r", str(ref), "-h", str(hyp)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), repr(expected))

    def test_single_cjk_character_cer(self):
        # Same bug, CER path: one reference character vs one substituted
        # character -> CER = 1 / 1 = 1.0, matching jiwer.cer directly.
        ref = self.tmp_path / "ref.txt"
        hyp = self.tmp_path / "hyp.txt"
        write(ref, "日\n")
        write(hyp, "本\n")

        expected = jiwer.cer("日", "本")
        result = self.invoke(["-c", "-r", str(ref), "-h", str(hyp)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output.strip(), repr(expected))


if __name__ == "__main__":
    unittest.main()
