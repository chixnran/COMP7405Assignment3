import numpy as np
from scipy.stats import norm
n = norm.pdf
N = norm.cdf
class pricer:
    def __init__(self, S, K, T, v, r,  type, t=0):
        self.S = S  # Underlying asset price
        self.K = K  # Option strike price
        self.t = t  # Time to expiration in year
        self.T = T  # Option maturity
        self.v = v  # Volatility of the underlying asset
        self.r = r  # Risk-free interest rate
        self.type = type

    def BSM(self, q):
        d1 = (np.log(self.S / self.K) + (self.r - q) * (self.T - self.t)) / (self.v * np.sqrt(self.T - self.t)) + 0.5 * self.v * np.sqrt(self.T - self.t)
        d2 = d1 - self.v * np.sqrt(self.T - self.t)
        if type == 'Call':
            V = self.S * np.exp(-q * (self.T - self.t)) * N(d1) - self.K * np.exp(-self.r * (self.T - self.t)) * N(d2)
        else:
            V = self.K * np.exp(-self.r * (self.T - self.t)) * N(-d2) - self.S * np.exp(-q * (self.T - self.t)) * N(-d1)
        return V