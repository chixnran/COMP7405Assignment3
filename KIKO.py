import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import Sobol

class KikoOptionMC(object):
    def __init__(self, option_type, S0, K, B_low, B_up, T, N, r, sigma, M, rebate):
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
            self.rebate = float(rebate)
        except ValueError:
            print('Error passing Options parameters')
            
    def discount_factor(self):
        return np.exp(-self.r * self.T)
    
    def price_path(self, seed=100):
        Dt = self.T / self.N
        sobol = Sobol(d=self.N, scramble=True, seed=seed)
        samples = sobol.random_base2(m=int(np.log2(self.M)))
        Z = norm.ppf(samples)
        price_path = (self.S0 * np.cumprod(np.exp((self.r - 0.5 * self.sigma**2) * Dt + self.sigma * np.sqrt(Dt) * Z), axis=1))
        return price_path

    def KikoPayoff(self, seed=100):
        price_path = self.price_path(seed=seed)
        knocked_in = np.any(price_path <= self.B_low, axis=1)
        knocked_out = np.any(price_path >= self.B_up, axis=1)
        
        active_paths = knocked_in & ~knocked_out
        inactive_paths = ~knocked_in & ~knocked_out
        
        if self.option_type == 'put':
            payoff_active = self.discount_factor() * np.maximum(self.K - price_path[active_paths, -1], 0)
        else:
            payoff_active = self.discount_factor() * np.maximum(price_path[active_paths, -1] - self.K, 0)
        
        payoff_knock_out = self.rebate * np.ones(np.sum(knocked_out))
        payoff_inactive = np.zeros(np.sum(inactive_paths))
        total_payoff = np.concatenate((payoff_active, payoff_knock_out, payoff_inactive))
        
        return total_payoff
    
    def value(self):
        total_payoff = self.KikoPayoff()
        MCvalue = np.mean(total_payoff)
        MCValue_std = np.std(total_payoff)
        upper_bound = MCvalue + 1.96 * MCValue_std / np.sqrt(self.M)
        lower_bound = MCvalue- 1.96 * MCValue_std / np.sqrt(self.M)
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
    
    # option_type = 'put'
    # S0 = 100
    # K = 95
    # B_low = 90
    # B_up = 120
    # T = 1
    # N = 252
    # r = 0.05
    # sigma = 0.2
    # M = 100000
    # rebate = 5
    #
    # kiko_option = KikoOptionMC(option_type, S0, K, B_low, B_up, T, N, r, sigma, M, rebate)
    # kiko_option.value()
    #
    # kiko_option.delta()