JiWER provides a simple CLI, which should be available after installation. 

For details, see `jiwer --help`.

```text
$ jiwer --help
Usage: jiwer [OPTIONS]

  JiWER is a python tool for computing the word-error-rate of ASR systems. To
  use this CLI, store the reference and hypothesis sentences in a text file,
  where each sentence is delimited by a new-line character. The text files are
  expected to have an equal number of lines, unless the `-g` flag is used. The
  `-g` flag joins computation of the WER by doing a global minimal alignment.

Options:
  -r, --reference PATH   Path to new-line delimited text file of reference
                         sentences.  [required]
  -h, --hypothesis PATH  Path to new-line delimited text file of hypothesis
                         sentences.  [required]
  -c, --cer              Compute CER instead of WER.
  -a, --align            Print alignment of each sentence.
  -g, --global           Apply a global minimal alignment between reference
                         and hypothesis sentences before computing the WER.
  --help                 Show this message and exit.
```

Note that the CLI does not support custom pre-processing. Any pre-processing
should be done on the text files manually before calling JiWER when using the CLI. 
