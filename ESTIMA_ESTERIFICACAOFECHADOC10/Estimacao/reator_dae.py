import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from config import *
import termodinamica
import cinetica

def taxa_reacao(Temp, Y, Rpar, imod):
    """
    Substitui a SUBROUTINE TAXAREAC.
    Calcula as taxas específicas de reação (mol/min).
    """
    k1d = 10.0 ** Rpar[0]
    kDEG = 0.0 # Conforme Fortran original
    k2d = 0.0  # Conforme Fortran original

    Ec, EG, V = Y[0], Y[1], Y[6]

    if imod == 0:
        E_g = Y[2]
        EgOH = Y[5]
        
        if (Ec / V < 0.0) or (EG / V < 0.0):
            Taxa = 0.0
            Taxa2 = 0.0
            Taxa3 = 0.0
        else:
            Taxa = k1d * (Ec / V) * (EG / V)
            Taxa2 = k1d * (Ec / V) * (EgOH / V)
            Taxa3 = kDEG * (EG / V) * (EgOH / V)
            
    elif imod == 1:
        EgOH = Y[7] # Na transesterificação, a posição muda no Fortran
        
        if EgOH < 0.0:
            Taxa = 0.0
        else:
            Taxa = k2d * ((EgOH / V) ** 2.0)
        Taxa2 = 0.0
        Taxa3 = 0.0

    return Taxa, Taxa2, Taxa3

def equacoes_diferenciais(t, Y, Rpar, Tp, VzN2, imod, NA0, r):
    """
    Substitui a SUBROUTINE RES.
    Retorna as derivadas dY/dt para o solve_ivp.
    """
    dYdt = np.zeros_like(Y)
    
    # Parâmetros
    kl_G = 10.0 ** Rpar[1]
    kl_A = 10.0 ** Rpar[2]
    alphaa = 0.0
    
    # Variáveis de Estado (Fase Líquida)
    Ec, EG, E_g, H2O, Z, EgOH, V = Y[0:7]
    Mac, MacH2O = Y[7:9]

    if imod == 0:
        # Variáveis de Estado (Fase Gás)
        nEG, nH2O, nN2 = Y[9], Y[10], Y[11]
        
        # O solver lidará com o 'beta' na etapa algébrica, então nós o passamos 
        # como Y[12] mas ele será corrigido no loop de otimização interno, se necessário.
        beta = Y[12]

        # Frações molares
        ntot = nEG + nH2O + nN2
        # Evitando divisão por zero
        ntot = max(ntot, 1e-12) 
        zEG, zH2O, zN2 = nEG / ntot, nH2O / ntot, nN2 / ntot

        # NOTA: Você precisará trazer a função 'Volume' (Vpar) para cá.
        # Simulando o retorno de Vpar = [VH2O, VEG, Vp]
        Vpar = np.array([0.1 * V, 0.4 * V, 0.5 * V]) 
        
        Phi_H2O = Vpar[0] / V
        Phi_EG = Vpar[1] / V
        Phi_pol = Vpar[2] / V

        # Cinética e Termodinâmica
        Mn, Xn = cinetica.propriedades_polimero(Ec, r, NA0, imod)
        Taxa, Taxa2, Taxa3 = taxa_reacao(Tp, Y, Rpar, imod)
        Phi_int = termodinamica.calcular_equilibrio(Xn, Tp, zH2O, zEG, Phi_pol)
        
        PhiH2O_int, PhiEG_int = Phi_int[0], Phi_int[1]

        # Transferência de Massa
        termo_exp = np.exp((1.0 - (1.0 / Xn)) * Phi_pol + params.xf * Phi_pol**2.0)
        nEG_l = kl_G * termo_exp * (Phi_EG - PhiEG_int)
        nH2O_l = kl_A * termo_exp * (Phi_H2O - PhiH2O_int)

        Ftot = VzN2 + nEG_l + nH2O_l

        # Coluna de Flash
        PsatEG, PsatH2O = termodinamica.pressao_saturacao_antoine(params.Tflash)
        Keg = PsatEG / params.Pr
        KH2O = PsatH2O / params.Pr
        
        xEG = zEG / (beta * (Keg - 1.0) + 1.0)
        xH2O = zH2O / (beta * (KH2O - 1.0) + 1.0)
        
        Fv = beta * Ftot
        L = Ftot - Fv

        # Balanços Diferenciais (Fase Líquida)
        dYdt[0] = -Taxa*V - Taxa2*V + Taxa3*V                     # Ec
        dYdt[1] = -Taxa*V - Taxa3*V - nEG_l + L*xEG               # EG
        dYdt[2] = 2.0 * Taxa2 * V                                 # E_g
        dYdt[3] = Taxa*V + Taxa2*V - nH2O_l + L*xH2O              # H2O
        dYdt[4] = Taxa3*V                                         # Z
        dYdt[5] = Taxa*V - Taxa2*V - Taxa3*V                      # EgOH
        dYdt[6] = -nEG_l*(MMEgE/densEg) - nH2O_l*(MMH2O/densH2O)  # V

        # Balanço de Massas Acumuladas
        FH2O = zH2O * Ftot * MMH2O
        FEG = zEG * Ftot * MMEgE
        dYdt[7] = FH2O + FEG                                      # Mac
        dYdt[8] = FH2O                                            # MacH2O

        # Balanços Diferenciais (Fase Gás)
        dYdt[9] = nEG_l - zEG*Ftot                                # nEG
        dYdt[10] = nH2O_l - zH2O*Ftot + alphaa*VzN2               # nH2O
        dYdt[11] = (1.0 - alphaa)*VzN2 - zN2*Ftot                 # nN2
        
        # Derivada da algébrica (dummy, resolvido externamente ou via DAE radau)
        dYdt[12] = 0.0

    elif imod == 1:
        # Transesterificação: Maioria das derivadas zeradas conforme Fortran
        dYdt[:] = 0.0
        
    return dYdt

def resolver_reator(t_span, Y0, Rpar, Tp, VzN2, imod, NA0, r, t_eval=None):
    solucao = solve_ivp(
        fun=lambda t, y: equacoes_diferenciais(t, y, Rpar, Tp, VzN2, imod, NA0, r),
        t_span=t_span,
        y0=Y0,
        method='BDF',
        t_eval=t_eval, # <-- Adicionamos isso aqui!
        rtol=1e-5,
        atol=1e-5
    )
    return solucao