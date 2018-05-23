from pysabr import hagan_2002_normal_sabr as sabr
import pytest
from pytest import approx


ERROR_TOLERANCE = 0.00001  # 0.01bps error is tolerated

# [k, f, t, alpha, beta, rho, volvol]
test_data = {
    'Beta=1.0 OTMF (float division by zero fix)': [
        [0.010, 0.025, 2., 0.118054435871, 1.0, 0.2, 0.3],
        0.001959886074
    ]
}


@pytest.fixture(scope="module",
                params=test_data.values(),
                ids=list(test_data.keys()))
def sabr_data(request):
    yield request.param


def test_interpolation(sabr_data):
    [k, f, t, alpha, beta, rho, volvol], v_n_target = sabr_data
    v_n_test = sabr.normal_vol(k, f, t, alpha, beta, rho, volvol)
    assert v_n_test == approx(v_n_target, ERROR_TOLERANCE)
