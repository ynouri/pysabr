import logging
import pytest
from pysabr import Hagan2002LognormalSABR


N = 1e9  # We assume BPV = $100,000 (= 1e9 / 1e4)
MAX_ABS_ERROR_PREMIUM = 10.0  # Max absolute error on premium is $10.0
MAX_ERROR_VOL = 0.0005  # Max error is 0.05%


def test_vols(vol_cube):
    """Test the full ATM SABR vol chain for Hagan's 2002 Lognormal model."""
    logging.debug(vol_cube)
    (f, s, t, v_atm_n, beta, rho, volvol), vols_target, _ = vol_cube
    sabr = Hagan2002LognormalSABR(f/100, s/100, t, v_atm_n/1e4,
                                  beta, rho, volvol)
    strikes = vols_target.index
    vols_test = [sabr.lognormal_vol(k/100) * 100 for k in strikes]
    assert vols_test == pytest.approx(vols_target.values, MAX_ERROR_VOL)


def test_premiums(vol_cube):
    """Test the premiums."""
    (f, s, t, v_atm_n, beta, rho, volvol), _, premiums_target = vol_cube
    sabr = Hagan2002LognormalSABR(f/100, s/100, t, v_atm_n/1e4,
                                  beta, rho, volvol)
    strikes = premiums_target.index[premiums_target.index + s > 0.]
    # TODO: strikes = premiums_target.index
    premiums_test = [sabr.call(k/100) * N for k in strikes]
    premiums_target = premiums_target[strikes].values * N / 100
    assert premiums_test == pytest.approx(premiums_target,
                                          abs=MAX_ABS_ERROR_PREMIUM)
