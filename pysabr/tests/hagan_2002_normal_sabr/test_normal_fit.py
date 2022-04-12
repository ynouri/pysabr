import numpy as np
from pysabr import Hagan2002NormalSABR
import logging


def test_normal_calibration_beta_05():
    k = np.array([0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.10])
    v = np.array([116.63, 111.66, 109.96, 113.97, 124.7, 140.04, 157.3, 175.07, 192.78, 210.26, 227.42])
    [t, f, s, beta] = np.array([0.5, 0.07520, 0.0000, 0.5000])
    sabr = Hagan2002NormalSABR(f, s, t, beta=beta)
    sabr_test = sabr.fit(k, v)
    [alpha, rho, volvol] = sabr_test
    logging.debug('\nalpha={:.6f}, rho={:.6f}, volvol={:.6f}'
                  .format(alpha, rho, volvol))
    sabr_target = np.array([0.050394, 0.64125, 0.875235])
    error_max = max(abs(sabr_test - sabr_target))
    assert (error_max < 1e-5)
