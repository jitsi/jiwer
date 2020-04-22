from jiwer import wer


def perform_computation(num_sentences):
    truth = ["this is a speed test" for _ in range(0, num_sentences)]
    hypo = ["this is not a speed test" for _ in range(0, num_sentences)]

    wer(truth, hypo)


def test_speed_n1(benchmark):
    benchmark(perform_computation, 1)


def test_speed_n10(benchmark):
    benchmark(perform_computation, 10)


def test_speed_n100(benchmark):
    benchmark(perform_computation, 100)


def test_speed_n1000(benchmark):
    benchmark(perform_computation, 1000)
