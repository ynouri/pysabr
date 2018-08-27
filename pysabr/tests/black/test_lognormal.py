import pysabr.black as black
import numpy as np
import logging
import pytest
from pytest import approx


ERROR_TOLERANCE = 0.001  # 0.1% error is tolerated

test_data = {
    '1y6m 800bps itm call 10% LN vol': [
        1e5,
        [2., 10., 1.5, 0.10, 0.03, 'call'],
        1e5 * (10. - 2.) * np.exp(-0.03*1.5)
    ],
    '10y 10bps itm call 20% LN vol': [
        1e5,
        [0.012, 0.013, 10., 0.20, 0.02, 'call'],
        296.88
    ],
    '6m 20bps otm put 50% LN vol': [
        1e5,
        [0.030, 0.028, 0.5, 0.50, 0.04, 'put'],
        504.37
    ],
    '2y atm put 100% LN vol': [
        1e5,
        [0.005, 0.005, 2., 1., 0.10, 'put'],
        213.07
    ]
}


@pytest.fixture(scope="module",
                params=test_data.values(),
                ids=list(test_data.keys()))
def option_data(request):
    yield request.param


def test_pv(option_data):
    """Tests the Black lognormal formula against an expected target PV."""
    n, [k, f, t, v, r, cp], target_pv = option_data
    pv = n * black.lognormal_call(k, f, t, v, r, cp)
    logging.debug("PV = {}".format(pv))
    logging.debug("Target PV = {}".format(target_pv))
    assert pv == approx(target_pv, ERROR_TOLERANCE)


def test_call_put_parity(option_data):
    """Tests the Black lognormal call put parity relationship."""
    n, [k, f, t, v, r, _], _ = option_data
    call = n * black.lognormal_call(k, f, t, v, r, cp='call')
    put = n * black.lognormal_call(k, f, t, v, r, cp='put')
    target = n * np.exp(-r*t) * (f - k)
    logging.debug("Call - Put = {}".format(call - put))
    logging.debug("DF * (F -K) = {}".format(target))
    assert call - put == approx(target, ERROR_TOLERANCE)


def test_shifted_lognormal_to_normal(option_data):
    """ Tests the conversion from shifted lognormal vol to normal."""
    n, [k, f, t, v_sln, r, cp], _ = option_data
    # We assume a shift of 2% for the test
    s = 0.02
    v_n = black.shifted_lognormal_to_normal(k, f, s, t, v_sln)
    pv_lognormal = n * black.shifted_lognormal_call(k, f, s, t, v_sln, r, cp)
    pv_normal = n * black.normal_call(k, f, t, v_n, r, cp)
    assert pv_normal == approx(pv_lognormal, ERROR_TOLERANCE)
