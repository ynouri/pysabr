import logging
import pytest
from pysabr import Hagan2002LognormalSABR


# Max error is 0.05%
MAX_ERROR = 0.0005


def test_vols(vol_cube):
    """Test the full ATM SABR vol chain for Hagan's 2002 Lognormal model."""
    logging.debug(vol_cube)
    (f, s, t, v_atm_n, beta, rho, volvol), target_vols = vol_cube
    sabr = Hagan2002LognormalSABR(f/100, t, s/100, v_atm_n/1e4,
                                  beta, rho, volvol)
    strikes = target_vols.index
    test_vols = [sabr.lognormal_vol(k/100) * 100 for k in strikes]
    assert test_vols == pytest.approx(target_vols.values, MAX_ERROR)


# TODO, premiums are available in premiums.csv
def test_premiums():
    """Test the premiums."""
    assert True
