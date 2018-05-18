from pysabr import hagan_2002_lognormal_sabr as sabr
import pytest
import numpy as np


def test_lognormal_beta_05():
    s = 3 / 100
    k = 3.02715567337258000 / 100
    f = 2.52715567337258000 / 100
    t = 10.00000000000000000
    alpha = 0.0252982247897366000
    beta = 0.5000000000000000000
    rho = -0.2463339754454810000
    volvol = 0.2908465632529730000
    v_test = sabr.lognormal_vol(k+s, f+s, t, alpha,
                                      beta, rho, volvol) * 100
    v_target = 10.8917434151064000
    assert v_test == pytest.approx(v_target, 1e-7)


def test_lognormal_beta_0():
    k = 0.01
    f = 0.03
    t = 10
    alpha = 0.02
    beta = 1.00
    rho = 0.00
    volvol = 0.00
    v_test = sabr.lognormal_vol(k, f, t, alpha, beta, rho, volvol)
    v_target = 0.02
    assert v_test == pytest.approx(v_target, 1e-7)


def test_lognormal_beta_05_smile():
    k = np.array([-0.4729, 0.5271, 1.0271, 1.5271, 1.7771, 2.0271, 2.2771,
                  2.4021, 2.5271, 2.6521, 2.7771, 3.0271, 3.2771, 3.5271,
                  4.0271, 4.5271, 5.5271])
    [t, f, s, alpha, beta, rho, volvol] = np.array(
        [10.0000, 2.5271, 3.0000, 0.0253, 0.5000, -0.2463, 0.2908])
    k = (k + s) / 100
    f = (f + s) / 100
    vols_test = [sabr.lognormal_vol(k_, f, t, alpha, beta, rho, volvol) * 100
                 for k_ in k]
    vols_target = np.array([19.641923, 15.785344, 14.305103, 13.073869,
                            12.550007, 12.088721, 11.691661, 11.517660,
                            11.360133, 11.219058, 11.094293, 10.892464,
                            10.750834, 10.663653, 10.623862, 10.714479,
                            11.103755])
    error_max = max(abs(vols_test - vols_target))
    assert (error_max < 1e-5)
