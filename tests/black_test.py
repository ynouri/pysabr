from sabr import black_lognormal_call
import numpy as np
import logging

def test_intrinsic_value_on_expiry():
    [k, f, t, v, r, cp] = [2., 3., 0., 0.20, 0.02, 'call']
    pv = black_lognormal_call(k, f, t, r, v, cp) * 1e5
    logging.debug("PV = {}".format(pv))
    assert pv == 1e5

def test_far_itm_call():
    [k, f, t, v, r, cp] = [2., 10., 1.5, 0.60, 0.03, 'call']
    pv = black_lognormal_call(k, f, t, r, v, cp) * 1e5
    logging.debug("PV = {}".format(pv))
    assert pv == 8. * np.exp(-0.03*1.5)

def test_call_pv():
    [k, f, t, v, r, cp] = [0.012, 0.013, 10., 0.20, 0.02, 'call']
    pv = black_lognormal_call(k, f, t, r, v, cp) * 1e5
    logging.debug("PV = {}".format(pv))
    assert pv == 0.
