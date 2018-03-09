import numpy as np
from scipy.stats import norm

"""

Public Function BlackLogNormal_Call(k As Double, f As Double, t As Double, ByVal v As Double, r As Double, Optional Cp = "Call") As Double
    Dim d1 As Double
    Dim d2 As Double
    v = v / 100
    d1 = (Log(f / k) + v ^ 2 * t / 2) / (v * t ^ 0.5)
    d2 = d1 - v * t ^ 0.5
    If Cp = "Put" Then
        BlackLogNormal_Call = Exp(-r * t) * (-f * Application.NormSDist(-d1) + k * Application.NormSDist(-d2))
    Else
        BlackLogNormal_Call = Exp(-r * t) * (f * Application.NormSDist(d1) - k * Application.NormSDist(d2))
    End If
End Function

"""

def black_lognormal_call(k, f, t, v, r, cp='call'):
    d1 = (np.log(f/k) + v**2 * t/2) / (v * t**0.5)
    d2 = d1 - v * t**0.5
    if cp == 'call':
        pv = np.exp(-r*t) * (f * norm.cdf(d1) - k * norm.cdf(d2))
    elif cp == 'put':
        pv = np.exp(-r*t) * (-f * norm.cdf(-d1) + k * norm.cdf(-d2))
    else:
        pv = 0
    return pv
