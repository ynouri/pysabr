import numpy as np
from .base_sabr import BaseLognormalSABR
from pysabr import black
from scipy.optimize import minimize


class Hagan2002LognormalSABR(BaseLognormalSABR):
    """Hagan 2002 SABR lognormal vol expansion model - ATM normal vol input."""

    def alpha(self):
        """Implies alpha parameter from the ATM normal volatility."""
        f, s, t, v_atm_n = self.f, self.shift, self.t, self.v_atm_n
        beta, rho, volvol = self.beta, self.rho, self.volvol
        # Convert ATM normal vol to ATM shifted lognormal
        v_atm_sln = black.normal_to_shifted_lognormal(f, f, s, t, v_atm_n)
        return alpha(v_atm_sln, f+s, t, beta, rho, volvol)

    def lognormal_vol(self, k):
        """Return lognormal volatility for a given scalar strike."""
        f, s, t = self.f, self.shift, self.t
        beta, rho, volvol = self.beta, self.rho, self.volvol
        alpha = self.alpha()
        v_sln = lognormal_vol(k+s, f+s, t, alpha, beta, rho, volvol)
        return v_sln

    def fit(self, k, v_sln, initial_guess = [0.01, 0.00, 0.10]):
        """
        Calibrate SABR parameters alpha, rho and volvol.

        Best fit a smile of shifted lognormal volatilities passed through
        arrays k and v. Returns a tuple of SABR params (alpha, rho,
        volvol)
        """
        f, s, t, beta = self.f, self.shift, self.t, self.beta

        def vol_square_error(x):
            vols = [lognormal_vol(k_+s, f+s, t, x[0], beta, x[1],
                                  x[2]) * 100 for k_ in k]
            return sum((vols - v_sln)**2)

        x0 = np.array(initial_guess)
        bounds = [(0.0001, None), (-0.9999, 0.9999), (0.0001, None)]
        res = minimize(vol_square_error, x0, method='L-BFGS-B', bounds=bounds)
        alpha, self.rho, self.volvol = res.x
        return [alpha, self.rho, self.volvol]


def lognormal_vol(k, f, t, alpha, beta, rho, volvol):
    """
    Hagan's 2002 SABR lognormal vol expansion.

    The strike k can be a scalar or an array, the function will return an array
    of lognormal vols.
    """
    # Negative strikes or forwards
    if k <= 0 or f <= 0:
        return 0.
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
    if abs(z) > eps:
        vz = alpha * z * (1 + (a + b + c) * t) / (d * (1 + v + w) * _x(rho, z))
        return vz
    # if |z| <= eps
    else:
        v0 = alpha * (1 + (a + b + c) * t) / (d * (1 + v + w))
        return v0


def _x(rho, z):
    """Return function x used in Hagan's 2002 SABR lognormal vol expansion."""
    a = (1 - 2*rho*z + z**2)**.5 + z - rho
    b = 1 - rho
    return np.log(a / b)


# TODO: refactor the interface to make it compliant with normal interface
def alpha(v_atm_ln, f, t, beta, rho, volvol):
    """
    Compute SABR parameter alpha to an ATM lognormal volatility.

    Alpha is determined as the root of a 3rd degree polynomial. Return a single
    scalar alpha.
    """
    f_ = f ** (beta - 1)
    p = [
        t * f_**3 * (1 - beta)**2 / 24,
        t * f_**2 * rho * beta * volvol / 4,
        (1 + t * volvol**2 * (2 - 3*rho**2) / 24) * f_,
        -v_atm_ln
    ]
    roots = np.roots(p)
    roots_real = np.extract(np.isreal(roots), np.real(roots))
    # Note: the double real roots case is not tested
    alpha_first_guess = v_atm_ln * f**(1-beta)
    i_min = np.argmin(np.abs(roots_real - alpha_first_guess))
    return roots_real[i_min]
