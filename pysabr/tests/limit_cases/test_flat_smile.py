import numpy as np
from pysabr import Hagan2002LognormalSABR
from pysabr import Hagan2002NormalSABR
from pytest import approx


MAX_ABS_ERROR_VOL = 0.05e-4  # Max error is 0.05bps


def test_flat_normal_smile():
    f, s, t, v_atm_n, beta, rho, volvol = (0.02, 0.025, 1.0, 0.0040,
                                           0.0, 0.0, 0.0)
    sabr_ln = Hagan2002LognormalSABR(f, s, t, v_atm_n, beta, rho, volvol)
    sabr_n = Hagan2002NormalSABR(f, s, t, v_atm_n, beta, rho, volvol)
    n_strikes = 20
    strikes = np.linspace(-1.99, 6.00, n_strikes) / 100
    sabr_ln_vols = [sabr_ln.normal_vol(k) for k in strikes]
    sabr_n_vols = [sabr_n.normal_vol(k) for k in strikes]
    target_vols = np.ones(n_strikes) * v_atm_n
    target_vols_approx = approx(target_vols, abs=MAX_ABS_ERROR_VOL)
    assert (
        sabr_n_vols == target_vols_approx
        and sabr_ln_vols == target_vols_approx
    )
