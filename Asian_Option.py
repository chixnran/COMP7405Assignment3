import numpy as np
from scipy.special import erf

class AsianOptionMC(object):
    def __init__(self, option_type, S0, K, T, N, r, sigma, M):
        try:
            self.option_type = option_type
            assert isinstance(option_type, str)
            self.S0 = float(S0)
            self.K = float(K)
            self.T = float(T)
            self.N = int(N)
            self.r = float(r)
            self.sigma = float(sigma)
            self.M = int(M)
        except ValueError:
            print('Error passing Options parameters')

        if option_type != 'call' and option_type != 'put':
            raise ValueError("Error: option type not valid. Enter 'call' or 'put'")
        if S0 < 0 or K < 0 or T <= 0 or r < 0 or sigma < 0:
            raise ValueError('Error: Negative inputs not allowed')

        self.Dt = self.T / float(self.N)
        self.discount = np.exp(- self.r * self.T)

    @property
    def GeometricAsianOption(self):
        sigsqT = ((self.sigma ** 2 * self.T * (self.N + 1) * (2 * self.N + 1)) / (6 * self.N * self.N))
        muT = (0.5 * sigsqT + (self.r - 0.5 * self.sigma ** 2) * self.T * (self.N + 1) / (2 * self.N))
        d1 = ((np.log(self.S0 / self.K) + (muT + 0.5 * sigsqT)) / np.sqrt(sigsqT))
        d2 = d1 - np.sqrt(sigsqT)
        if self.option_type == 'call':
            N1 = 0.5 * (1 + erf(d1 / np.sqrt(2)))
            N2 = 0.5 * (1 + erf(d2 / np.sqrt(2)))
            geometric_value = self.discount * (self.S0 * np.exp(muT) * N1 - self.K * N2)
        else:
            N1 = 0.5 * (1 - erf(d1 / np.sqrt(2)))
            N2 = 0.5 * (1 - erf(d2 / np.sqrt(2)))
            geometric_value = self.discount * (self.K * N2 - self.S0 * np.exp(muT) * N1)
        return geometric_value

    @property
    def price_path(self, seed=100):
        np.random.seed(seed)
        price_path = (self.S0 * np.cumprod(np.exp(
            (self.r - 0.5 * self.sigma ** 2) * self.Dt + self.sigma * np.sqrt(self.Dt) * np.random.randn(self.M,
                                                                                                         self.N)), 1))
        return price_path

    @property
    def ArithPayoff(self):
        if self.option_type == 'call':
            ArithPayoff = self.discount \
                          * np.maximum(np.mean(self.price_path, 1) - self.K, 0)
        else:
            ArithPayoff = self.discount \
                          * np.maximum(self.K - np.mean(self.price_path, 1), 0)
        return ArithPayoff

    @property
    def GeoPayoff(self):
        geometric_average = np.exp((1 / float(self.N)) * np.sum(np.log(self.price_path), 1))
        if self.option_type == 'call':
            payoff_geometric = self.discount * np.maximum(geometric_average - self.K, 0)
        else:
            payoff_geometric = self.discount * np.maximum(self.K - geometric_average, 0)
            return payoff_geometric

    @property
    def value(self):
        MCvalue = np.mean(self.ArithPayoff)
        MCValue_std = np.std(self.ArithPayoff)
        upper_bound = MCvalue + 1.96 * MCValue_std / np.sqrt(self.M)
        lower_bound = MCvalue - 1.96 * MCValue_std / np.sqrt(self.M)
        return MCvalue, lower_bound, upper_bound

    @property
    def value_with_control_variate(self):
        value_with_CV = self.ArithPayoff + self.GeometricAsianOption - self.GeoPayoff
        value_with_control_variate = np.mean(value_with_CV, 0)
        value_with_control_variate_std = np.std(value_with_CV, 0)
        upper_bound_CV = value_with_control_variate + 1.96 * value_with_control_variate_std / np.sqrt(self.M)
        lower_bound_CV = value_with_control_variate - 1.96 * value_with_control_variate_std / np.sqrt(self.M)
        return value_with_control_variate, lower_bound_CV, upper_bound_CV