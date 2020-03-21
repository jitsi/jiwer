import time
import numpy

from jiwer import wer


def execute_test(num_executions, num_sentences):
    truth = ["this is a speed test" for _ in range(0, num_sentences)]
    hypo = ["this is not a speed test" for _ in range(0, num_sentences)]

    times = []
    for _ in range(num_executions):
        start = time.monotonic()
        wer(truth, hypo)
        end = time.monotonic()

        times.append(end - start)

    times = numpy.array(times)
    mean = numpy.mean(times)
    var = numpy.std(times)

    return mean, var


def test_with_n_sentences(num_sentences):
    print("executing wer with {} sentences:".format(num_sentences))
    mean, std = execute_test(10, num_sentences)
    print("\tmean={:.4f} sec std={:.4f} sec".format(mean, std))


def main():
    for n in [1, 10, 50, 100]:
        test_with_n_sentences(n)


if __name__ == "__main__":
    main()
