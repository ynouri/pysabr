import numpy as np
from pysabr import black
from pytest import approx


MAX_ABS_ERROR_VOL = 0.01e-4  # Max error is 0.01bp


def conversion_round_trip(fun_n_to_sln, fun_sln_n):
    """Generic function for conversion round trip test."""
    f, s, t, v_atm_n = (0.02, 0.025, 1.0, 0.0040)
    n_strikes = 200
    strikes = np.linspace(-1.99, 6.00, n_strikes) / 100
    target_vols = np.ones(n_strikes) * v_atm_n
    # Normal to Lognormal conversion
    sln_vols = [fun_n_to_sln(k, f, s, t, v_n)
                for (k, v_n) in zip(strikes, target_vols)]
    # Lognormal to Normal conversion
    test_vols = [fun_sln_n(k, f, s, t, v_sln)
                 for (k, v_sln) in zip(strikes, sln_vols)]
    assert test_vols == approx(target_vols, abs=MAX_ABS_ERROR_VOL)


def test_hagan_conversion_round_trip():
    """Convert N to SLN, then SLN to N, using Hagan's formula."""
    fun_n_to_sln = black.hagan_normal_to_lognormal
    fun_sln_n = black.hagan_lognormal_to_normal
    conversion_round_trip(fun_n_to_sln, fun_sln_n)


def test_premium_based_conversion_round_trip():
    """Convert N to SLN, then SLN to N, using premium based conversion."""
    fun_n_to_sln = black.normal_to_shifted_lognormal
    fun_sln_n = black.shifted_lognormal_to_normal
    conversion_round_trip(fun_n_to_sln, fun_sln_n)
