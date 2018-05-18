import numpy as np
import pysabr.sabr as sabr
import logging


def test_calibration_beta_05():
    k = np.array([-0.4729, 0.5271, 1.0271, 1.5271, 1.7771, 2.0271, 2.2771,
                  2.4021, 2.5271, 2.6521, 2.7771, 3.0271, 3.2771, 3.5271,
                  4.0271, 4.5271, 5.5271])
    v = np.array([19.641923, 15.785344, 14.305103, 13.073869,
                  12.550007, 12.088721, 11.691661, 11.517660,
                  11.360133, 11.219058, 11.094293, 10.892464,
                  10.750834, 10.663653, 10.623862, 10.714479,
                  11.103755])
    [t, f, s, beta] = np.array([10.0000, 2.5271, 3.0000, 0.5000])
    k = (k + s) / 100
    f = (f + s) / 100
    sabr_test = sabr.calibration(k, v, f, t, beta)
    [alpha, rho, volvol] = sabr_test
    logging.debug('\nalpha={:.6f}, rho={:.6f}, volvol={:.6f}'
                  .format(alpha, rho, volvol))
    sabr_target = np.array([0.0253, -0.2463, 0.2908])
    error_max = max(abs(sabr_test - sabr_target))
    assert (error_max < 1e-5)
