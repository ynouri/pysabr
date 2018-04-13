import numpy as np
from scipy.stats import norm

def lognormal_call(k, f, t, v, r, cp='call'):
    d1 = (np.log(f/k) + v**2 * t/2) / (v * t**0.5)
    d2 = d1 - v * t**0.5
    if cp == 'call':
        pv = np.exp(-r*t) * (f * norm.cdf(d1) - k * norm.cdf(d2))
    elif cp == 'put':
        pv = np.exp(-r*t) * (-f * norm.cdf(-d1) + k * norm.cdf(-d2))
    else:
        pv = 0
    return pv

def normal_call(k, f, t, v, r, cp='call'):
    d1 = (f - k) / (v * t**0.5)
    cp_sign = {'call': 1., 'put': -1.}[cp]
    pv = np.exp(-r*t) * (
        cp_sign * (f - k) * norm.cdf(cp_sign * d1) +
        v * (t / (2 * np.pi))**0.5 * np.exp(-d1**2 / 2))
    return pv

"""
Public Function BlackNormal_Call(k As Double, f As Double, t As Double, v As Double, r As Double) As Double
    Dim d1 As Double
    d1 = (f - k) / (v * t ^ 0.5)
    BlackNormal_Call = Exp(-r * t) * (

    (f - k) * Application.NormSDist(d1)

    +

    v * (t / (2 * pi)) ^ 0.5 * Exp(-d1 ^ 2 / 2)

    )
End Function
"""
