import numpy as np
from scipy.special import erf

class BasketOptionMC(object):
    def __init__(self, option_type, S0_1, S0_2, K, T, N, r, rho, sigma_1, sigma_2, M):
        try:
            self.option_type = option_type
            assert isinstance(option_type, str)
            self.S0_1 = float(S0_1)
            self.S0_2 = float(S0_2)
            self.K = float(K)
            self.T = float(T)
            self.N = int(N)
            self.r = float(r)
            self.sigma_1 = float(sigma_1)
            self.sigma_2 = float(sigma_2)
            self.rho = float(rho)
            self.M = int(M)
        except ValueError:
            print('Error passing Options parameters')

    def discount_factor(self):
        return np.exp(-self.r * self.T)

    def GeometricBasketOption(self):
        sigma_B = np.sqrt((self.sigma_1 ** 2) + (2 * self.sigma_1 * self.sigma_2 * self.rho) + (self.sigma_2 ** 2)) / 2
        mu = self.r - (1 / 2) * ((self.sigma_1 ** 2 + self.sigma_2 ** 2) / 2) + (1 / 2) * sigma_B ** 2
        Bg = np.sqrt(self.S0_1 * self.S0_2)
        d1 = (np.log(Bg / self.K) + (mu + (1 / 2) * sigma_B ** 2) * self.T) / (sigma_B * np.sqrt(self.T))
        d2 = d1 - sigma_B * np.sqrt(self.T)
        if self.option_type == 'Call':
            N1 = 0.5 * (1 + erf(d1 / np.sqrt(2)))
            N2 = 0.5 * (1 + erf(d2 / np.sqrt(2)))
            geometric_value = self.discount_factor() * (Bg * np.exp(mu * self.T) * N1 - self.K * N2)
        else:
            N1 = 0.5 * (1 - erf(d1 / np.sqrt(2)))
            N2 = 0.5 * (1 - erf(d2 / np.sqrt(2)))
            geometric_value = self.discount_factor() * (self.K * N2 - Bg * np.exp(mu * self.T) * N1)
        return geometric_value

    def price_path(self):
        Dt = self.T / self.N
        correl_matrix = np.array([[1, self.rho], [self.rho, 1]])
        L = np.linalg.cholesky(correl_matrix)
        seed = 100
        np.random.seed(seed)
        Z_uncorr = np.random.randn(self.M, self.N, 2)
        Z_corr = np.einsum('ijk,kl->ijl', Z_uncorr, L)
        price_path_1 = (self.S0_1 * np.cumprod(np.exp((self.r - 0.5 * self.sigma_1 ** 2) * Dt +
                                                      self.sigma_1 * np.sqrt(Dt) * Z_corr[:, :, 0]), axis=1))
        price_path_2 = (self.S0_2 * np.cumprod(np.exp((self.r - 0.5 * self.sigma_2 ** 2) * Dt +
                                                      self.sigma_2 * np.sqrt(Dt) * Z_corr[:, :, 1]), axis=1))

        price_paths = np.stack((price_path_1, price_path_2), axis=-1)

        return price_paths

    def Arith_payoff(self):
        price_paths = self.price_path()
        arithMean = np.mean(price_paths, axis=2)
        if self.option_type == 'Call':
            ArithPayoff = self.discount_factor() \
                          * np.maximum(np.mean(arithMean, 1) - self.K, 0)
        else:
            ArithPayoff = self.discount_factor() \
                          * np.maximum(self.K - np.mean(arithMean, 1), 0)
        return ArithPayoff

    def geometric_payoff(self):
        price_paths = self.price_path()
        geoMean = np.sqrt(np.prod(price_paths, axis=2))
        geometric_average = np.exp((1 / float(self.N)) * np.sum(np.log(self.geoMean), 1))
        if self.option_type == 'Call':
            payoffs = np.maximum(geometric_average - self.K, 0)
        else:
            payoffs = np.maximum(self.K - geometric_average, 0)
        return self.discount_factor() * payoffs

    def value(self):
        payoffs = self.Arith_payoff()
        MCvalue = np.mean(payoffs)
        MCValue_std = np.std(payoffs)
        upper_bound = MCvalue + 1.96 * MCValue_std / np.sqrt(self.M)
        lower_bound = MCvalue - 1.96 * MCValue_std / np.sqrt(self.M)
        return MCvalue, lower_bound, upper_bound

    def value_with_control_variate(self):
        arith_payoffs = self.Arith_payoff()
        geom_option_value = self.GeometricBasketOption()
        geom_payoffs = self.geometric_payoff()
        adjusted_geom_value = np.full_like(arith_payoffs, geom_option_value)
        value_with_CV = arith_payoffs + adjusted_geom_value - geom_payoffs  # check

        value_with_control_variate = np.mean(value_with_CV)
        value_with_control_variate_std = np.std(value_with_CV)
        upper_bound_CV = value_with_control_variate + 1.96 * value_with_control_variate_std / np.sqrt(self.M)
        lower_bound_CV = value_with_control_variate - 1.96 * value_with_control_variate_std / np.sqrt(self.M)
        return value_with_control_variate, lower_bound_CV, upper_bound_CV