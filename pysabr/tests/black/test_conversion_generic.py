from pysabr import black
import pytest
from pytest import approx


MAX_ERROR_PREMIUM = 0.001  # 0.1% error is tolerated
N = 1e5  # Default notional proxies annuity of $100M 10Y swap

# Test case should be defined as follow:
# 'Test case name': [
#     [k, f, u, t, v, cp],  # u=0% for LN vol, u='N'' for N vol
#     s  # s=0% to convert to LN vol, s='N"' to convert to N vol
# ],

test_data_dict = {
    '1y6m 800bps otm put 10% 2%-SLN vol to LN': [
        [0.02, 0.10, 0.02, 1.5, 0.10, 'put'], 0.00
    ],
    '10y 10bps otm put 20% LN vol to 3% SLN vol': [
        [0.012, 0.013, 10., 0.20, 0.00, 'put'], 0.03
    ],
    '1y atm 30% 2%-SLN vol to 2%-SLN vol': [
        [0.03, 0.03, 1., 0.30, 0.02, 'call'], 0.02
    ],
    '1y atm 30% 2%-SLN vol to LN vol': [
        [0.03, 0.03, 1., 0.30, 0.02, 'call'], 0.00
    ],
    '1y atm 30% 2%-SLN vol to 4%-SLN vol': [
        [0.03, 0.03, 1., 0.30, 0.02, 'call'], 0.04
    ],
    '6m 20bps otm put 50% LN vol to 1% SLN vol': [
        [0.030, 0.028, 0.5, 0.50, 0.00, 'put'], 0.01
    ]
}


@pytest.fixture(scope="module",
                params=test_data_dict.values(),
                ids=list(test_data_dict.keys()))
def test_data(request):
    yield request.param


def test_conversion(test_data):
    """Test the conversion from one vol type to another."""
    [k, f, u, t, v, cp], s = test_data
    r = 0.  # Assume a discount rate of 0% for the test.
    # SLN to SLN case
    if not u == 'N' and not u == 'N':
        pv_target = N * black.shifted_lognormal_call(k, f, u, t, v, r, cp)
        v_sln = black.lognormal_to_lognormal(k, f, s, t, v, u)
        pv_test = N * black.shifted_lognormal_call(k, f, s, t, v_sln, r, cp)
    # Other cases TODO
    else:
        assert False
    assert pv_target == approx(pv_test, MAX_ERROR_PREMIUM)
