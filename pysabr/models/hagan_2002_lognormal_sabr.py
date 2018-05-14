from abstract_sabr import AbstractSABR


class Hagan2002LognormalSABR(AbstractLognormalSABR):
    """Hagan's 2002 SABR lognormal vol expansion model. ATM normal vol input."""



def _lognormal_vol(k, f, t, alpha, beta, rho, volvol):
    """
    Hagan's 2002 SABR lognormal vol expansion.
    The strike k can be a scalar or an array, the function will return an array
    of lognormal vols.
    """
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
    # if |z| > eps
    vz = np.divide(
        alpha * z * (1 + (a + b + c) * t),
        (d * (1 + v + w) * _x(rho, z)),
        where=(abs(z) > eps)
        )
    # if |z| <= eps
    v0 = alpha * (1 + (a + b + c) * t) / (d * (1 + v + w))
    return np.where(abs(z) > eps, vz, v0)


def _x(rho, z):
    """x function used in Hagan's 2002 SABR lognormal vol expansion"""
    a = (1 - 2*rho*z + z**2)**.5 + z - rho
    b = 1 - rho
    return np.log(a / b)



def alpha(atm_vol, f, t, beta, rho, volvol):
    """
    Calibrate SABR parameter alpha to match an ATM lognormal volatility. To do
    so it computes the roots of a 3rd degree polynomial.
    Returns a single scalar alpha
    """
    f_ = f ** (beta - 1)
    p = [
        t * f_**3 * (1 - beta)**2 / 24,
        t * f_**2 * rho * beta * volvol / 4,
        (1 + t * volvol**2 * (2 - 3*rho**2) / 24) * f_,
        -atm_vol
    ]
    roots = np.roots(p)
    roots_real = np.extract(np.isreal(roots), np.real(roots))
    # Note: the double real roots case is not tested
    alpha_first_guess = atm_vol * f**(1-beta)
    i_min = np.argmin(np.abs(roots_real - alpha_first_guess))
    return roots_real[i_min]
