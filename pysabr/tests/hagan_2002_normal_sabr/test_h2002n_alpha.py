from pysabr import hagan_2002_normal_sabr as sabr
import logging
import pytest
from pytest import approx


ERROR_TOLERANCE = 0.00001  # 0.01bps error is tolerated

# [f, t, v_atm_n, beta, rho, volvol]
test_data = {
    'Beta=0.5, No Rho No Volvol': [
        [2., 1.0, 1.0, 0.5, 0.0, 0.0],
        0.712764724868
    ],
    'Flat normal smile 20bps (beta=0)': [
        [0.030, 5.0, 0.0020, 0., 0., 0.],
        0.002
    ],
    'Flat lognormal smile 30% (beta=1, fwd 2%, vol 60bps)': [
        [0.020, 0.5, 0.0060, 1., 0., 0.],
        0.300565687999
    ],
    'Beta=0, 40bps normal vol': [
        [0.025, 10.0, 0.0040, 0., -0.2, 0.3],
        0.003736571695
    ],
    'Low rates (0.1%) high vol (100bps) long dated (30y)': [
        [0.001, 30.0, 0.010, 0.7, 0.8, 0.5],
        -0.214685033491  # TODO: ALPHA NEGATIVE! What does that mean?
    ],
    'Regular case': [
        [0.025, 0.75, 0.0040, 0.5, -0.2, 0.3],
        0.025202566661
    ]
}


@pytest.fixture(scope="module",
                params=test_data.values(),
                ids=list(test_data.keys()))
def sabr_data(request):
    yield request.param


def test_calibration(sabr_data):
    [f, t, v_atm_n, beta, rho, volvol], target_alpha = sabr_data
    test_alpha = sabr.alpha(f, t, v_atm_n, beta, rho, volvol)
    logging.debug("Test alpha = {}".format(test_alpha))
    logging.debug("Target alpha = {}".format(target_alpha))
    assert test_alpha == approx(target_alpha, ERROR_TOLERANCE)


def test_atm_vol_repricing(sabr_data):
    [f, t, v_atm_n_target, beta, rho, volvol], _ = sabr_data
    alpha = sabr.alpha(f, t, v_atm_n_target, beta, rho, volvol)
    v_atm_n_test = sabr.normal_vol(f, f, t, alpha, beta, rho, volvol)
    assert v_atm_n_test == approx(v_atm_n_target, ERROR_TOLERANCE)
