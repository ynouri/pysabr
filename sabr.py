import numpy as np

def lognormal_SABR(k, f, t, alpha, beta, rho, volvol):
    eps = 1e-07
    logfk = np.log(f / k)
    fkbeta = (f*k)**(1 - beta)
    a = (1 - beta)**2 * alpha**2 / (24 * fkbeta)
    b = 0.25 * rho * beta * volvol * alpha / fkbeta**0.5
    c = (2 - 3*rho**2) * volvol**2 / 24
    d = fkbeta**0.5
    v = (1 - beta)**2 * logfk**2 / 24
    w = (1 - beta)**4 * logfk**4 / 1920
    z = volvol * fkbeta**0.5 * logfk / alpha
    if z > eps:
        return alpha * z * (1 + (a + b + c) * t) \
        / (d * (1 + v + w) * lognormal_x(rho, z))
    else:
        return alpha * (1 + (a + b + c) * t) / (d * (1 + v + w))
                                                
                                
def lognormal_x(rho, z):
    a = (1 - 2*rho*z + z**2)**.5 + z - rho
    b = 1 - rho
    return np.log(a / b)