import numpy as np
from pysabr import black
from pytest import approx


MAX_ABS_ERROR_VOL = 0.000001  # Max error is 0.01bp


def test_hagan_conversion_round_trip():
    """Convert N to SLN, then SLN to N, using Hagan's formula."""
    f, s, t, v_atm_n = (0.02, 0.025, 1.0, 0.0040)
    n_strikes = 200
    strikes = np.linspace(-1.99, 6.00, n_strikes) / 100
    target_vols = np.ones(n_strikes) * v_atm_n
    # Hagan Normal to Lognormal conversion (solve for polynomial roots)
    sln_vols = [black.hagan_normal_to_lognormal(k, f, s, t, v_n)
                for (k, v_n) in zip(strikes, target_vols)]
    # Hagan Lognormal to Normal conversion (direct formula)
    test_hagan_vols = [black.hagan_lognormal_to_normal(k, f, s, t, v_sln)
                       for (k, v_sln) in zip(strikes, sln_vols)]
    assert test_hagan_vols == approx(target_vols, abs=MAX_ABS_ERROR_VOL)
