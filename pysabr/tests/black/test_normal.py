import pysabr.black as black
import numpy as np
import logging
import pytest
from pytest import approx


MAX_ERROR_PRICE = 1e-4  # 1bp error is tolerated. TODO: refine this
MAX_ERROR_CONVERSION = 1e-8  # ie 0.0001bp
MAX_ERROR_HAGAN_CONVERSION = 1e-4  # ie 1bp

test_data = {
    '1y6m 800bps itm call 50bps N vol': [
        1e5,
        [2., 10., 1.5, 0.10, 0.03, 'call'],
        1e5 * (10. - 2.) * np.exp(-0.03*1.5)
    ],
    '10y 10bps itm call 30bps N vol': [
        1e5,
        [0.012, 0.013, 10., 0.0030, 0.02, 'call'],
        352.52
    ],
    '6m 20bps otm call 100bps N vol': [
        1e5,
        [0.028, 0.030, 0.5, 0.01, 0.04, 'call'],
        385.52
    ],
    '2y atm put 80bps N vol': [
        1e5,
        [0.005, 0.005, 2., 0.0080, 0.10, 'put'],
        1e5 * np.exp(-0.10*2.) * 0.0080 * (2. / (2 * np.pi))**0.5
    ],
    '30y atm call 40bps N vol': [
        1e9,  # ie $100M 10Y swap
        [0.025, 0.025, 30., 0.0040, 0., 'call'],
        8740387.44
    ]
}


@pytest.fixture(scope="module",
                params=test_data.values(),
                ids=list(test_data.keys()))
def option_data(request):
    yield request.param


def test_pv(option_data):
    """Test the Black normal formula against an expected target PV."""
    n, [k, f, t, v, r, cp], target_pv = option_data
    pv = n * black.normal_call(k, f, t, v, r, cp)
    logging.debug("PV = {}".format(pv))
    logging.debug("Target PV = {}".format(target_pv))
    assert pv == approx(target_pv, MAX_ERROR_PRICE)


def test_call_put_parity(option_data):
    """Test the Black normal call put parity relationship."""
    n, [k, f, t, v, r, _], _ = option_data
    call = n * black.normal_call(k, f, t, v, r, cp='call')
    put = n * black.normal_call(k, f, t, v, r, cp='put')
    target = n * np.exp(-r*t) * (f - k)
    logging.debug("Call - Put = {}".format(call - put))
    logging.debug("DF * (F -K) = {}".format(target))
    assert call - put == approx(target, MAX_ERROR_PRICE)


def test_hagan_normal_to_lognormal(option_data):
    """Test N to SLN conversion using Hagan formula root solving."""
    n, [k, f, t, v_n, r, cp], _ = option_data
    # We assume a shift of 2% for the test
    s = 0.02
    v_sln = black.hagan_normal_to_lognormal(k, f, s, t, v_n)
    pv_normal = n * black.normal_call(k, f, t, v_n, r, cp)
    pv_lognormal = n * black.shifted_lognormal_call(k, f, s, t, v_sln, r, cp)
    assert pv_lognormal == approx(pv_normal, MAX_ERROR_HAGAN_CONVERSION)


def test_normal_to_shifted_lognormal(option_data):
    """Test the conversion from normal vol to shifted lognormal."""
    n, [k, f, t, v_n, r, cp], _ = option_data
    # We assume a shift of 2% for the test
    s = 0.02
    v_sln = black.normal_to_shifted_lognormal(k, f, s, t, v_n)
    pv_normal = n * black.normal_call(k, f, t, v_n, r, cp)
    pv_lognormal = n * black.shifted_lognormal_call(k, f, s, t, v_sln, r, cp)
    assert pv_lognormal == approx(pv_normal, MAX_ERROR_CONVERSION)
