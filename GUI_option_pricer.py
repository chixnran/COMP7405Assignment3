from pywebio.input import *
from pywebio.output import *
from pywebio.session import hold
from pywebio import start_server
from BSModel import pricer
from Asian_Option import AsianOptionMC
from Basket_Option import BasketOptionMC
from KIKO import KikoOptionMC
from IV import IV
from BiTreeAmericanOption import AmericanOption


OptionParameters = {
        'European':['S(0)','σ','rf','T','K','type','repo rate q'],  #S(0) | volatility σ | rf rate | T | K | type | repo rate q
        'Implied Volatility':['S(0)','rf','T','K','type','the option premium'],
        'American Option':['S(0)','σ','rf','T','K','type','number of steps N'], #the number of steps N
        'Geometric Asian option':['S(0)','σ','rf','T','K','type','number of observation times for the geometric average n'], #the number of observation times for the geometric average n
        'Arithmetic Asian option':['S(0)','σ','rf','T','K','type','number of observation times for the geometric average n',
                                   'number of paths in the Monte Carlo simulation','control variate method'], #Geometric Asian option + the number of paths in the Monte Carlo simulation | control variate method
        'Geometric basket option':['S(0)_i','σ_i','rf','T','K','type','correlation ρ'], #S(0)_i | σ_i | rf rate | T | K | type | the correlation ρ
        'Arithmetic basket option':['S(0)_i','σ_i','rf','T','K','type','correlation ρ',
                                    'number of paths in the Monte Carlo simulation','control variate method'], #the number of paths in the Monte Carlo simulation | control variate method
        'KIKO put option':['S(0)','σ','rf','T','K','lower barrier L','upper barrier U',
                           'number of observation times n','cash rebate R'] # lower barrier L | upper barrier U | the number of observation times n | and the cash rebate R
        }
Classes = list(OptionParameters.keys())


def main():
    # input
    choice = select("Please choose the option class you want to price", options=Classes)

    if choice == 'European':
        # Q1
        Inputparams=input_group("Please choose/enter your parameters",
                    [
                        select('Option Type', options=['Call', 'Put'], name='type'),
                        input('S(0)', name='S_0'),
                        input('Volatility (v in float format, eg. 0.2)', name='v'),
                        input('risk free rate (in float format, eg. 0.05)', name='rf'),
                        input('Time to maturity (T)',name='T'),
                        input('Strike Price (K)',name='K'),
                        input('Repo rate q',name='q')

                    ])
        S, K, T, v, r, type, q = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
                                  float(Inputparams['v']), float(Inputparams['rf']), Inputparams['type'], float(Inputparams['q']))
        model = pricer(S,K,T,v,r,type)
        P = model.BSM(q)
        put_markdown('## Result')
        put_text("the theoretical price of your option is {:4f}".format(P))

    # Q2
    elif choice == 'Implied Volatility':
        # Q2 iv
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      input('S(0)', name='S_0'),
                                      input('True Price', name='C_true'),
                                      input('risk free rate (in float format, eg. 0.05)', name='rf'),
                                      input('Time to maturity (T)', name='T'),
                                      input('Strike Price (K)', name='K'),

                                  ])
        S, K, C_true, T, cp_flag, r = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['C_true']),
                                  float(Inputparams['T']), Inputparams['type'], Inputparams['rf'])
        iv = IV(S, K, C_true, T, cp_flag,r).find_imp_vol()
        put_markdown('## Result')
        put_text("the implied volatility is {:4f}".format(iv))

    # Q3-a
    elif choice == 'Geometric Asian option':
        # Q3 geometric asian
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      input('S(0)', name='S_0'),
                                      input('Volatility (in float format, eg. 0.2)', name='v'),
                                      input('risk free rate (in float format,eg. 0.05)', name='rf'),
                                      input('Time to maturity (in year)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input( 'Number of observation times for the geometric average n', name='n'),
                                      input('Number of samples', name='M', decription='we will not use M in geometric calculation')
                                  ])
        S0, K, T, v, r, option_type, N, M = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
                                  float(Inputparams['v']), float(Inputparams['rf']), Inputparams['type'],
                                  float(Inputparams['n']), float(Inputparams['M']))
        asian_option = AsianOptionMC(option_type, S0, K, T, N, r, v, M)
        P = asian_option.GeometricAsianOption
        put_markdown('## Result')
        put_text("the theoretical price of your option is {:4f}".format(P))

    # Q3-b
    elif choice == 'Geometric basket option':
        # Q3 geometric basket
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      input('S0_1', name='S0_1'),
                                      input('S0_2', name='S0_2'),
                                      input('Volatility_1 (v in float format, eg. 0.2)', name='v1'),
                                      input('Volatility_2 (v in float format, eg. 0.2)', name='v2'),
                                      input('risk free rate (in float format, eg. 0.05)', name='rf'),
                                      input('Time to maturity (T in year)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input('Correlation', name='rho'),
                                      input('Number of observation times for the geometric average n', name='n'),
                                      input('Number of samples', name='M', decription='we will not use M in geometric calculation')

                                  ])

        S0_1, S0_2, K, T, v1, v2, r, option_type, rho, n, M= (
        float(Inputparams['S0_1']), float(Inputparams['S0_2']), float(Inputparams['K']), float(Inputparams['T']),
        float(Inputparams['v1']), float(Inputparams['v2']), float(Inputparams['rf']), Inputparams['type'],
        float(Inputparams['rho']), float(Inputparams['n']), float(Inputparams['M']))

        basket_option = BasketOptionMC(option_type, S0_1, S0_2, K, T, n, r, rho, v1, v2, M)
        P = float(basket_option.GeometricBasketOption())
        put_markdown('## Result')
        put_text("the theoretical price of your option is {:4f}".format(P))

    # Q4
    elif choice == 'Arithmetic Asian option':
        # Q4 MC arithmatic asian option
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      select('Control Variate Method', options=['no control variate', 'geometric Asian option'], name='cv_method'),
                                      input('S(0)', name='S_0'),
                                      input('Volatility (in float format, eg. 0.2)', name='v'),
                                      input('risk free rate (in float format,eg. 0.05)', name='rf'),
                                      input('Time to maturity (in year)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input('Number of observation times for the geometric average n', name='n'),
                                      input('Number of samples', name='M')
                                  ])
        S0, K, T, v, r, option_type, N, M, cv_method = (
        float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
        float(Inputparams['v']), float(Inputparams['rf']), Inputparams['type'],
        float(Inputparams['n']), float(Inputparams['M']), Inputparams['cv_method'])

        asian_option = AsianOptionMC(option_type, S0, K, T, N, r, v, M)
        if cv_method == 'no control variate':
            values = list(asian_option.value)
            P, lower_bound, upper_bound = values[0], values[1], values[2]
            put_markdown('## Result')
            put_text("The value with control variate is {:.4f}".format(P))
            put_text("The lower bound is {:.4f}".format(lower_bound))
            put_text("The upper bound is {:.4f}".format(upper_bound))
        else:
            values = list(asian_option.value_with_control_variate())
            P, lower_bound, upper_bound = values[0], values[1], values[2]
            put_markdown('## Result')
            put_text("The value with control variate is {:.4f}".format(P))
            put_text("The lower bound is {:.4f}".format(lower_bound))
            put_text("The upper bound is {:.4f}".format(upper_bound))

    # Q5
    elif choice == 'Arithmetic basket option':
        # Q5 arithmetic basket
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      select('Control Variate Method',
                                             options=['no control variate', 'geometric Asian option'],
                                             name='cv_method'),
                                      input('S0_1', name='S0_1'),
                                      input('S0_2', name='S0_2'),
                                      input('Volatility_1 (v in float format, eg. 0.2)', name='v1'),
                                      input('Volatility_2 (v in float format, eg. 0.2)', name='v2'),
                                      input('risk free rate (in float format, eg. 0.05)', name='rf'),
                                      input('Time to maturity (T in year)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input('Correlation', name='rho'),
                                      input('Number of observation times for the geometric average n', name='n'),
                                      input('Number of samples', name='M')

                                  ])
        S0_1, S0_2, K, T, v1, v2, r, option_type, rho, n, M, cv_method = (
            float(Inputparams['S0_1']), float(Inputparams['S0_2']), float(Inputparams['K']), float(Inputparams['T']),
            float(Inputparams['v1']), float(Inputparams['v2']), float(Inputparams['rf']), Inputparams['type'],
            float(Inputparams['rho']), float(Inputparams['n']), float(Inputparams['M']), Inputparams['cv_method'])

        basket_option = BasketOptionMC(option_type, S0_1, S0_2, K, T, n, r, rho, v1, v2, M)
        if cv_method == 'no control variate':
            values = list(basket_option.value())
            P, lower_bound, upper_bound = values[0], values[1], values[2]
            put_markdown('## Result')
            put_text("The value with control variate is {:.4f}".format(P))
            put_text("The lower bound is {:.4f}".format(lower_bound))
            put_text("The upper bound is {:.4f}".format(upper_bound))
        else:
            values = list(basket_option.value_with_control_variate())
            P, lower_bound, upper_bound = values[0], values[1], values[2]
            put_markdown('## Result')
            put_text("The value with control variate is {:.4f}".format(P))
            put_text("The lower bound is {:.4f}".format(lower_bound))
            put_text("The upper bound is {:.4f}".format(upper_bound))

    # Q6
    elif choice == 'KIKO put option':
        # Q6
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Put'], name='type'),
                                      input('S(0)', name='S_0'),
                                      input('Volatility (v)', name='v'),
                                      input('risk free rate (in float format, eg.0.05)', name='rf'),
                                      input('Time to maturity (year)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input('lower barrier L', name='B_low'),
                                      input('Upper barrier U', name='B_up'),
                                      input('Number of observation times', name='n'),
                                      input('The cash rebate', name='R'),
                                      input('Number of samples', name='M')

                                  ])

        option_type, S0, K, T, v, r, B_low, B_up, M, rebate, N = (Inputparams['type'], float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
                                  float(Inputparams['v']), float(Inputparams['rf']), float(Inputparams['B_low']), float(Inputparams['B_up']),
                                  float(Inputparams['M']), float(Inputparams['R']), float(Inputparams['n']))

        kiko = KikoOptionMC(option_type, S0, K, B_low, B_up, T, N, r, v, M, rebate)
        values = list(kiko.value())
        P, lower_bound, upper_bound = values[0], values[1], values[2]
        put_markdown('## Result')
        put_text("The theoretical price of your option is {:.4f}".format(P))
        put_text("The lower bound is {:.4f}".format(lower_bound))
        put_text("The upper bound is {:.4f}".format(upper_bound))
        #put_text(option_type, S0, K, B_low, B_up, T, N, r, v, M, rebate)

    # Q7
    elif choice == 'American Option':
        Inputparams = input_group("Please choose/enter your parameters",
                                  [
                                      select('Option Type', options=['Call', 'Put'], name='type'),
                                      input('S(0)', name='S_0'),
                                      input('Volatility (v in float format, eg. 0.2)', name='v'),
                                      input('risk free rate (in float format, eg. 0.05)', name='rf'),
                                      input('Time to maturity (T)', name='T'),
                                      input('Strike Price (K)', name='K'),
                                      input('Number of steps ', name='N')

                                  ])
        S0, K, T, v, r, N, option_type = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
                                  float(Inputparams['v']), float(Inputparams['rf']), int(Inputparams['N']), Inputparams['type'])
        model = AmericanOption()
        P = model.BiTreeAmericanOption(S0, v, r, T, K, N, option_type)
        put_markdown('## Result')
        put_text("the theoretical price of your option is {:4f}".format(P))


if __name__ == '__main__':
    main()
