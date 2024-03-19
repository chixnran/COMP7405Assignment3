from pywebio.input import *
from pywebio.output import *
from pywebio.session import hold
from pywebio import start_server
from BSModel import pricer
from KIKO没改完 import KikoOptionMC


OptionParameters = {
        'European':['S(0)','σ','rf','T','K','type','repo rate q'],  #S(0) | volatility σ | rf rate | T | K | type | repo rate q
        'American':['S(0)','σ','rf','T','K','type','number of steps N'], #the number of steps N
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
                        input('Volatility', name='v'),
                        input('risk free rate', name='rf'),
                        input('Time to maturity',name='T'),
                        input('Strike Price',name='K'),
                        input('Repo rate q',name='q')

                    ])
        S, K, T, v, r, type, q = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
                                  float(Inputparams['v']), float(Inputparams['rf']), Inputparams['type'], float(Inputparams['q']))
        model = pricer(S,K,T,v,r,type)
        P = model.BSM(q)
        put_text("the theoretical price of your option is {}".format(P))

    elif choice == 'B':
        return
    elif choice == 'C':
        return
    elif choice == 'D':
        return
    elif choice == 'E':
        return
    elif choice == 'KIKO put option':
        # # Q6
        # Inputparams = input_group("Please choose/enter your parameters",
        #                           [
        #                               input('S(0)', name='S_0'),
        #                               input('Volatility', name='v'),
        #                               input('risk free rate', name='rf'),
        #                               input('Time to maturity', name='T'),
        #                               input('Strike Price', name='K'),
        #                               input('Repo rate q', name='q')
        #                               input('lower barrier L', name='B_low')
        #                               input('Upper barrier U', name='B_up')
        #                               input('Number of observation times', name='n')
        #                               input('The cash rebate', name='R')
        #
        #                           ])
        # S, K, T, v, r, type, q = (float(Inputparams['S_0']), float(Inputparams['K']), float(Inputparams['T']),
        #                           float(Inputparams['v']), float(Inputparams['rf']), Inputparams['type'],
        #                           float(Inputparams['q']))
        # model = pricer(S, K, T, v, r, type)
        # P = model.BSM(q)
        # put_text("the theoretical price of your option is {}".format(P))
    elif choice == 'G':
        return


if __name__ == '__main__':
    main()
