from sabr import black_lognormal_call
import logging

def test_call_pv():
    [k, f, t, v, r, cp] = [0.012, 0.013, 10., 0.20, 0.02, 'call']
    pv = black_lognormal_call(k, f, t, r, v, cp) * 1e5
    logging.debug("PV = {}".format(pv))
    assert pv == 0.
