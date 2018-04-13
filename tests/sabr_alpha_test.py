import pysabr.sabr as sabr
import logging
import pytest
from pytest import approx

ERROR_TOLERANCE = 0.001 # 0.1% error is tolerated

test_data = {
    'Beta=1 flat lognormal': [
        [0.60, 0.02, 1.5, 1.0, 0.0, 0.0],
        0.60
    ],
    'Beta=0 flat normal': [
        [0.60, 2.0, 1.5, 0.0, 0.0, 0.0],
        1.1746
    ],
    'Beta=0.5, 10y': [
        [0.20, 0.015, 10., 0.5, -0.2, 0.3],
        0.02310713
    ]
}

@pytest.fixture(scope="module",
                params=test_data.values(),
                ids=list(test_data.keys()))
def sabr_data(request):
    yield request.param


def test_calibration(sabr_data):
    [atm_vol, f, t, beta, rho, volvol], target_alpha = sabr_data
    test_alpha = sabr.alpha(atm_vol, f, t, beta, rho, volvol)
    logging.debug("Test alpha = {}".format(test_alpha))
    logging.debug("Target alpha = {}".format(target_alpha))
    assert test_alpha == approx(target_alpha, ERROR_TOLERANCE)


def test_atm_vol_repricing(sabr_data):
    [target_atm_vol, f, t, beta, rho, volvol], _ = sabr_data
    alpha = sabr.alpha(target_atm_vol, f, t, beta, rho, volvol)
    test_atm_vol = sabr.lognormal_vol(f, f, t, alpha, beta, rho, volvol)
    assert test_atm_vol == approx(target_atm_vol, ERROR_TOLERANCE)
