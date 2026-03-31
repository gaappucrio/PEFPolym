import numpy as np
from config import params

def propriedades_polimero(Y_S, r, NA0, imod):
    """
    Substitui a SUBROUTINE Mnpolimero.
    Y_S é a variável de conversão (Y[0] ou Y[7] no Fortran, dependendo da etapa).
    """
    MMmma = 100.12 # Massa molar (g/mol)
    
    p = (NA0 - Y_S) / NA0 # Conversão
    
    if imod == 0:
        # Esterificação
        Xn = (r + 1.0) / (r + 1.0 - 2.0 * r * p)
    else:
        # Transesterificação
        Xn = 1.0 / (1.0 - p) if p != 1.0 else 1e6 # Evita divisão por zero
        
    Mn = Xn * MMmma
    return Mn, Xn

def modifica_kl(EgOH, NA0, kl_GT0):
    """
    Substitui a SUBROUTINE Modificakl.
    """
    p = (NA0 - EgOH) / NA0
    Xn = 1.0 / (1.0 - p) if p != 1.0 else 1e6
    
    kl_GT = kl_GT0 * np.exp(-params.alpha * Xn)
    return kl_GT