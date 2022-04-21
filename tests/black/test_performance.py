import timeit
from pysabr import black
import logging


def test_normal_to_shifted_lognormal():
    """Test N to SLN conversion performance."""
    def slow_conversion():
        [k, f, s, t, v_n] = [0.025, 0.025, 0.02, 30.0, 0.0040]
        v_sln = black.normal_to_shifted_lognormal(k, f, s, t, v_n)
        return v_sln
    nb_iterations = 100
    time = timeit.timeit(slow_conversion, number=nb_iterations)
    logging.debug(
        "Time for {} iterations = {:2f}s".format(nb_iterations, time))
    # TODO: 100 conversions should take less than 0.1s
    assert time <= 2.0  # failures on CI with times around 0.7s
