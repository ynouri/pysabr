from abc import ABCMeta, abstractmethod
import black

class AbstractSABR(ABCMeta):
    """Abstract class for SABR models."""


    def __init__(self):
        pass


    @abstractmethod
    def alpha(self):
        """Implies alpha parameter from the ATM normal volatility."""


    @abstractmethod
    def fit(self, k, v):
        """Best fit the model to a discrete volatility smile."""


    @abstractmethod
    def lognormal_vol(self, k):
        """Return lognormal volatility for a given strike."""


    @abstractmethod
    def normal_vol(self, k):
        """Return normal volatility for a given strike."""


    @abstractmethod
    def call(self, k, cp='Call'):
        """Abstract method for call prices."""


    def density(self, k):
        """Computes the probability density f unction from call prices."""
        pass


class AbstractLognormalSABR(AbstractSABR, ABCMeta):
    """
    Abstract SABR class for lognormal expansions with some generic methods
    implementations.
    """

    def __init__(self, f, t, shift=0., v_atm_n=0., beta=1., rho=0.
                      volvol=0.):
        self.f = f
        self.t = t
        self.shift = shift
        self.v_atm_n = v_atm_n
        self.beta = beta
        self.rho = rho
        self.volvol = volvol


    def fit(k, v):
        """
        Calibrates SABR parameters alpha, rho and volvol to best fit a smile of
        lognormal volatilities passed through arrays k and v.
        Returns a tuple of SABR params (alpha, rho, volvol)
        """

        f, t, beta = self.f, self.t, self.beta

        def vol_square_error(x):
            vols = lognormal_vol(k, f, t, x[0], beta, x[1], x[2]) * 100
            return sum((vols - v)**2)

        x0 = np.array([0.01, 0.00, 0.10])
        bounds = [(0.0001, None), (-0.9999, 0.9999), (0.0001, None)]
        res = minimize(vol_square_error, x0, method='L-BFGS-B', bounds=bounds)
        return res.x


    def normal_vol(self, k):
        """Return normal volatility for a given strike."""
        v_sln = self.lognormal_vol(k)
        v_n = black.shifted_lognormal_to_normal(k, f, s, t, v_sln)
        return v_n


    def call(self, k, cp='Call'):
        """Return call price."""
        f, s, t = self.f, self.shift, self.t
        v_sln = self.lognormal_vol(k)
        pv = black.shifted_lognormal_call(k, f, s, t, v_sln, 0., cp)
        return pv


class AbstractNormalSABR(AbstractSABR, ABCMeta):
    """
    Abstract SABR class for normal expansions with some generic methods
    implementations.
    """
    pass
