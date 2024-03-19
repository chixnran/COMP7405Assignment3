import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import Sobol


class KikoOptionMC(object):
    def __init__(self, option_type, S0, K, B_low, B_up, T, N, r, sigma, M):
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
            self.B_low = float(B_low)
            self.B_up = float(B_up)
        except ValueError:
            print('Error passing Options parameters')

    def discount_factor(self):
        return np.exp(-self.r * self.T)

    def price_path(self, seed=100):
        Dt = self.T / self.N
        sobol = Sobol(d=self.N, scramble=True, seed=seed)
        samples = sobol.random_base2(m=int(np.log2(self.M)))
        Z = norm.ppf(samples)
        price_path = (self.S0 * np.cumprod(np.exp((self.r - 0.5 * self.sigma ** 2) * Dt + self.sigma * np.sqrt(Dt) * Z),
                                           axis=1))
        return price_path

    def KikoPayoff(self):
        knocked_in = np.any(self.price_path() <= self.B_low, axis=1)
        knocked_out = np.any(self.price_path() >= self.B_up, axis=1)
        active_paths = knocked_in & ~knocked_out
        if self.option_type == 'put':
            payoff = self.discount_factor() * np.maximum(self.K - np.mean(self.price_path()[active_paths], axis=1), 0)
        else:
            payoff = self.discount_factor() * np.maximum(np.mean(self.price_path()[active_paths], axis=1) - self.K, 0)
        return payoff

    def value(self):
        MCvalue = np.mean(self.KikoPayoff())
        MCValue_std = np.std(self.KikoPayoff())
        upper_bound = MCvalue + 1.96 * MCValue_std / np.sqrt(self.M)
        lower_bound = MCvalue - 1.96 * MCValue_std / np.sqrt(self.M)
        return MCvalue, lower_bound, upper_bound

    def delta(self, dS=1.0, seed=100):
        np.random.seed(seed)
        original_S0 = self.S0
        original_price_path = self.price_path()
        original_payoff = self.KikoPayoff()
        V_S0 = np.mean(original_payoff)
        self.S0 += dS
        upper_price_path = self.price_path()
        upper_payoff = self.KikoPayoff()
        V_S0_up = np.mean(upper_payoff)
        self.S0 -= 2 * dS
        lower_price_path = self.price_path()
        lower_payoff = self.KikoPayoff()
        V_S0_down = np.mean(lower_payoff)

        self.S0 = original_S0
        estimated_delta = (V_S0_up - V_S0_down) / (2 * dS)

        return estimated_delta

# option = KikoOptionMC(option_type='put', S0=100, K=100, B_low=90, B_up=120, T=1, N=100, r=0.03, sigma=0.2, M=100000)
# option.value()
# option.delta()