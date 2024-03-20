import numpy as np
from scipy.stats import norm
n = norm.pdf
N = norm.cdf

class IV:

    def __init__(self, S, K, C_true, T, cp_flag, r, q=0, t=0, initial_sigma=0.0, iterations=1000,
                 precision=1.0e-7):
        '''
        s=stock pric，k=strike price，market_price=market price of option，T=maturity，r=risk free rate，
        cp_flag=option type，initial_value=initial guess of volatility，iteration，precision
        '''
        self.S = float(S)  # Underlying asset price
        self.K = float(K)  # Option strike price
        self.C_true = float(C_true)  # market true price of the option
        self.T = float(T)  # Option maturity
        self.t = float(t)  # Time to expiration in year
        self.r = float(r)  # Risk-free interest rate
        self.q = float(q)  # repo rate
        self.cp_flag = cp_flag  # Type of option: C for call option & P for put
        self.initial_sigma = initial_sigma
        self.iterations = iterations
        self.precision = precision

    def bs_price(self, v):
        '''
        cp_flag - type of option
        q - repo rate
        '''

        d1 = (np.log(self.S / self.K) + (self.r - self.q) * (self.T - self.t)) / (
                    v * np.sqrt(self.T - self.t)) + 0.5 * v * np.sqrt(self.T - self.t)
        d2 = d1 - v * np.sqrt(self.T - self.t)
        if self.cp_flag == 'Call':
            V = self.S * np.exp(-self.q * (self.T - self.t)) * N(d1) - self.K * np.exp(-self.r * (self.T - self.t)) * N(d2)
        else:
            V = self.K * np.exp(-self.r * (self.T - self.t)) * N(-d2) - self.S * np.exp(-self.q * (self.T - self.t)) * N(-d1)
        return V

    def bs_vega(self, v):
        d1 = (np.log(self.S / self.K) + (self.r - self.q) * (self.T - self.t)) / (
                    v * np.sqrt(self.T - self.t)) + 0.5 * v * np.sqrt(self.T - self.t)
        return self.S * np.exp(-self.q * (self.T - self.t)) * np.sqrt(self.T - self.t) * n(d1)

    def find_imp_vol(self):
        # starting value of sigma
        initial_sigma1 = np.sqrt(
            2 * abs((np.log(self.S / self.K) + (self.r - self.q) * (self.T - self.t)) / (self.T - self.t)))
        for i in range(self.iterations):

            # stop if the new sigma is negative
            if initial_sigma1 < 0:
                break
            model_price = self.bs_price(initial_sigma1)
            vega = self.bs_vega(initial_sigma1)
            diff = self.C_true - model_price

            if abs(diff) < self.precision and model_price > 0:
                return initial_sigma1
            initial_sigma1 += diff / vega
        if initial_sigma1 > 0:
            return initial_sigma1
