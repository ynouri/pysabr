import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize

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

def shifted_lognormal_call(k, f, s, t, v, r, cp='call'):
    return lognormal_call(k+s, f+s, t, v, r, cp)

def normal_call(k, f, t, v, r, cp='call'):
    d1 = (f - k) / (v * t**0.5)
    cp_sign = {'call': 1., 'put': -1.}[cp]
    pv = np.exp(-r*t) * (
        cp_sign * (f - k) * norm.cdf(cp_sign * d1) +
        v * (t / (2 * np.pi))**0.5 * np.exp(-d1**2 / 2))
    return pv

def normal_to_shifted_lognormal(k, f, s, t, v_n):
    target_premium = normal_call(k, f, t, v_n, 0.)
    v_sln_0 = v_n / (f + s)
    fun = lambda v_sln : 1e5 * (
        shifted_lognormal_call(k, f, s, t, v_sln, 0.) -
        target_premium) ** 2
    res = minimize(fun, v_sln_0, method='BFGS')
    return res.x[0]

"""
Public Function NormalToShiftedLognormal(k As Double, f As Double, t As Double, v_n As Double, shift As Double)
    Dim r               As Double
    Dim v_sln           As Double
    Dim premium         As Double
    Dim targetPremium   As Double
    Dim eps             As Double
    Dim err             As Double
    Dim errMax          As Double
    Dim iterations      As Integer
    Dim iterationsMax   As Integer
    Dim delta           As Double

    r = 0
    errMax = 0.00000001
    iterationsMax = 100
    eps = 0.01

    targetPremium = BlackNormal_Call(k, f, t, v_n, 0)
    v_sln = v_n / (f + shift) * 100
    premium = BlackLogNormal_Call(k + shift, f + shift, t, v_sln, 0, "Call")
    err = premium - targetPremium
    Debug.Print err
    iterations = 0

    While (Abs(err) > errMax) And (iterations < iterationsMax)
        delta = (BlackLogNormal_Call(k + shift, f + shift, t, v_sln + eps, 0, "Call") - BlackLogNormal_Call(k + shift, f + shift, t, v_sln, 0, "Call")) / eps
        v_sln = Application.Max(v_sln - err / delta, 0)
        premium = BlackLogNormal_Call(k + shift, f + shift, t, v_sln, 0, "Call")
        err = premium - targetPremium
        Debug.Print err
        iterations = iterations + 1
    Wend

    NormalToShiftedLognormal = v_sln

End Function
"""
