from pytest import approx
from pysabr import Hagan2002LognormalSABR
import numpy as np
from scipy.stats import norm

MAX_ABS_ERROR = 0.003


def test_standard_normal_density():
    """
    Test the density of a degenerated SABR model.

    Should converge towards the pdf of the standard normal distribution.
    """
    sabr = Hagan2002LognormalSABR(f=0, shift=100, t=1, v_atm_n=1,
                                  beta=1, rho=0, volvol=0)
    std_dev = sabr.v_atm_n * np.sqrt(sabr.t)  # = 1.0
    k = np.linspace(sabr.f - 5 * std_dev, sabr.f + 5 * std_dev, 100)
    sabr_density = [sabr.density(x) for x in k]
    std_normal_density = norm.pdf(k)
    assert sabr_density == approx(std_normal_density, abs=MAX_ABS_ERROR)
