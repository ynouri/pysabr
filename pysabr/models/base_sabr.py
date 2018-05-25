from abc import ABCMeta, abstractmethod
from pysabr import black
import numpy as np


class BaseSABR(metaclass=ABCMeta):
    """Base class for SABR models."""

    def __init__(self, f=0.01, shift=0., t=1.0, v_atm_n=0.0010,
                 beta=1., rho=0., volvol=0.):
        self.f = f
        self.t = t
        self.shift = shift
        self.v_atm_n = v_atm_n
        self.beta = beta
        self.rho = rho
        self.volvol = volvol
        self.params = dict()

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
        """Compute the probability density function from call prices."""
        std_dev = self.v_atm_n * np.sqrt(self.t)
        dk = 1e-4 * std_dev
        d2call = self.call(k+dk) - 2 * self.call(k) + self.call(k-dk)
        return d2call / dk**2

    def get_params(self):
        """Get parameters for this SABR model."""
        return self.__dict__

    def __repr__(self):
        class_name = self.__class__.__name__
        return (class_name, _pprint(self.__dict__))


def _pprint(params):
    """Pretty print the dictionary 'params'."""
    params_list = list()
    for i, (k, v) in enumerate(params):
        if type(v) is float:
            this_repr = '{}={:.4f}'.format(k, v)
        else:
            this_repr = '{}={}'.format(k, v)
        params_list.append(this_repr)
    return params_list


class BaseLognormalSABR(BaseSABR):
    """Base SABR class for lognormal expansions with some generic methods."""

    def normal_vol(self, k):
        """Return normal volatility for a given strike."""
        f, s, t = self.f, self.shift, self.t
        v_sln = self.lognormal_vol(k)
        v_n = black.shifted_lognormal_to_normal(k, f, s, t, v_sln)
        return v_n

    def call(self, k, cp='call'):
        """Return call price."""
        f, s, t = self.f, self.shift, self.t
        v_sln = self.lognormal_vol(k)
        pv = black.shifted_lognormal_call(k, f, s, t, v_sln, 0., cp)
        return pv


class BaseNormalSABR(BaseSABR):
    """Base SABR class for normal expansions with some generic methods."""

    def lognormal_vol(self, k):
        """Return lognormal volatility for a given strike."""
        f, s, t = self.f, self.shift, self.t
        v_n = self.normal_vol(k)
        v_sln = black.normal_to_shifted_lognormal(k, f, s, t, v_n)
        return v_sln

    def call(self, k, cp='call'):
        """Return call price."""
        f, t = self.f, self.t
        v_n = self.lognormal_vol(k)
        pv = black.normal_call(k, f, t, v_n, 0., cp)
        return pv
