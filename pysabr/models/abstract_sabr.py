from abc import ABCMeta, abstractmethod

class AbstractSABR(ABCMeta):
    """Abstract class for SABR models."""

    def self.__init__(self):
        pass

    @abstractmethod
    def self.lognormal_vol(self, k, f):
        """Abstract method for (shifted) lognormal volatility."""

    @abstractmethod
    def self.normal_vol(self, k, f):
        """Abstract method for normal volatility."""

    @abstractmethod
    def self.call(self, k, f, cp='Call'):
        """Abstract method for call prices."""

    def self.density(k, f):
        """Computes the probability density function from call prices."""
        pass
