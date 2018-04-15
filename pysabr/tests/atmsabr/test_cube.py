import logging
import pytest
from pysabr import atmsabr


# Max error is 0.05%
MAX_ERROR = 0.0005


def test_vols(vol_cube):
    logging.debug(vol_cube)
    (f, s, t, v_atm_n, beta, rho, volvol), target_vols = vol_cube
    k = 2.0
    test_vol = atmsabr.shifted_lognormal_vol(
        k/100, f/100, s/100, t, v_atm_n/1e4, beta, rho, volvol
    ) * 100
    target_vol = target_vols[k]
    assert test_vol == pytest.approx(target_vol, MAX_ERROR)


# To implement, premiums are available in premiums.csv
def test_premiums():
    assert True
