from .base_sabr import BaseNormalSABR
import numpy as np


class Hagan2002NormalSABR(BaseNormalSABR):

    def alpha(self):
        """Implies alpha parameter from the ATM normal volatility."""
        f, s, t, v_atm_n = self.f, self.shift, self.t, self.v_atm_n
        beta, rho, volvol = self.beta, self.rho, self.volvol
        # Convert ATM normal vol to ATM shifted lognormal
        return alpha(f+s, t, v_atm_n, beta, rho, volvol)

    def normal_vol(self, k):
        """Return normal volatility for a given strike."""
        f, s, t = self.f, self.shift, self.t
        beta, rho, volvol = self.beta, self.rho, self.volvol
        alpha = self.alpha()
        v_n = normal_vol(k+s, f+s, t, alpha, beta, rho, volvol)
        return v_n

    def fit(self, k, v_sln):
        """Calibrate SABR parameters alpha, rho and volvol."""
        raise NotImplementedError("To be implemented")


def normal_vol(k, f, t, alpha, beta, rho, volvol):
    """Hagan's 2002 SABR normal vol expansion - formula (B.67a)."""
    # We break down the complex formula into simpler sub-components
    f_av = np.sqrt(f * k)
    A = - beta * (2 - beta) * alpha**2 / (24 * f_av**(2 - 2 * beta))
    B = rho * alpha * volvol * beta / (4 * f_av**(1 - beta))
    C = (2 - 3 * rho**2) * volvol**2 / 24
    FMKR = _f_minus_k_ratio(f, k, beta)
    ZXZ = _zeta_over_x_of_zeta(k, f, t, alpha, beta, rho, volvol)
    # Aggregate all components into actual formula (B.67a)
    v_n = alpha * FMKR * ZXZ * (1 + (A + B + C) * t)
    return v_n


def _f_minus_k_ratio(f, k, beta):
    """Hagan's 2002 f minus k ratio - formula (B.67a)."""
    eps = 1e-07  # Numerical tolerance for f-k and beta
    if abs(f-k) > eps:
        if abs(1-beta) > eps:
            return (1 - beta) * (f - k) / (f**(1-beta) - k**(1-beta))
        else:
            return (f - k) / np.log(f / k)
    else:
        return k**beta


def _zeta_over_x_of_zeta(k, f, t, alpha, beta, rho, volvol):
    """Hagan's 2002 zeta / x(zeta) function - formulas (B.67a)-(B.67b)."""
    eps = 1e-07  # Numerical tolerance for zeta
    f_av = np.sqrt(f / k)
    zeta = volvol * (f - k) / (alpha * f_av**beta)
    if abs(zeta) > eps:
        return zeta / _x(rho, zeta)
    else:
        # The ratio converges to 1 when zeta approaches 0
        return 1.


def _x(rho, z):
    """Hagan's 2002 x function - formula (B.67b)."""
    a = (1 - 2*rho*z + z**2)**.5 + z - rho
    b = 1 - rho
    return np.log(a / b)


def alpha(f, t, v_atm_n, beta, rho, volvol):
    """
    Compute SABR parameter alpha from an ATM normal volatility.

    Alpha is determined as the root of a 3rd degree polynomial. Return a single
    scalar alpha.
    """
    f_ = f ** (1 - beta)
    p = [
        - beta * (2 - beta) / (24 * f_**2) * t * f**beta,
        t * f**beta * rho * beta * volvol / (4 * f_),
        (1 + t * volvol**2 * (2 - 3*rho**2) / 24) * f**beta,
        -v_atm_n
    ]
    roots = np.roots(p)
    roots_real = np.extract(np.isreal(roots), np.real(roots))
    # Note: the double real roots case is not tested
    alpha_first_guess = v_atm_n * f**(-beta)
    i_min = np.argmin(np.abs(roots_real - alpha_first_guess))
    return roots_real[i_min]


def polynom(v_atm_n, f, t, alpha, beta, rho, volvol):
    """Debug function - to remove"""
    f_ = f ** (1 - beta)
    p = [
        - beta * (2 - beta) / (24 * f_**2) * t * f**beta,
        t * f**beta * rho * beta * volvol / (4 * f_),
        (1 + t * volvol**2 * (2 - 3*rho**2) / 24) * f**beta,
        -v_atm_n
    ]
    return p[0] * alpha**3 + p[1] * alpha**2 + p[2] * alpha + p[3]


def v_atm_n(f, t, alpha, beta, rho, volvol):
    """Debug function - to remove"""
    f_av = f
    A = - beta * (2 - beta) * alpha**2 / (24 * f_av**(2 - 2 * beta))
    B = rho * alpha * volvol * beta / (4 * f_av**(1 - beta))
    C = (2 - 3 * rho**2) * volvol**2 / 24
    v_atm_n = alpha * f**beta * (1 + (A + B + C) * t)
    return v_atm_n
