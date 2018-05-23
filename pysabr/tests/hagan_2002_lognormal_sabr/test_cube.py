import logging
import pytest
from pysabr import Hagan2002LognormalSABR


# Max error is 0.05%
MAX_ERROR = 0.0005


def test_vols(vol_cube):
    """Test the full ATM SABR vol chain for Hagan's 2002 Lognormal model."""
    logging.debug(vol_cube)
    (f, s, t, v_atm_n, beta, rho, volvol), _, vols_target, _ = vol_cube
    sabr = Hagan2002LognormalSABR(f/100, t, s/100, v_atm_n/1e4,
                                  beta, rho, volvol)
    strikes = vols_target.index
    vols_test = [sabr.lognormal_vol(k/100) * 100 for k in strikes]
    assert vols_test == pytest.approx(vols_target.values, MAX_ERROR)


def test_premiums(vol_cube):
    """Test the premiums."""
    (f, s, t, v_atm_n, beta, rho, volvol), df, _, premiums_target = vol_cube
    sabr = Hagan2002LognormalSABR(f/100, t, s/100, v_atm_n/1e4,
                                  beta, rho, volvol)
    strikes = premiums_target.index[premiums_target.index + s > 0.]
    # TODO: strikes = premiums_target.index
    premiums_test = [sabr.call(k/100) * 100 for k in strikes]
    premiums_target = premiums_target[strikes].values
    assert premiums_test == pytest.approx(premiums_target, MAX_ERROR)
