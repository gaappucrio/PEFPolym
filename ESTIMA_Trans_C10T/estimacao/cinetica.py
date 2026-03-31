import numpy as np
import config

def propriedades_polimero(Y_S, r, NA0, imod):
    MMmma = 100.12
    Y_S = max(Y_S, 0.0) # Trava física: Moles não podem ser negativos
    p = (NA0 - Y_S) / NA0
    p = min(p, 0.999999) # Trava física: Conversão máxima de 99.9999%
    
    if imod == 0:
        Xn = (r + 1.0) / (r + 1.0 - 2.0 * r * p)
    else:
        Xn = 1.0 / (1.0 - p)
    return Xn * MMmma, Xn

def modifica_kl(EgOH, NA0, kl_GT0):
    EgOH = max(EgOH, 0.0)
    p = (NA0 - EgOH) / NA0
    p = min(p, 0.999999)
    Xn = 1.0 / (1.0 - p)
    return kl_GT0 * np.exp(np.clip(-config.params.alpha * Xn, -700.0, 700.0))

def modifica_kl_trans(EgOH, NA0, kl_GT0, theta):
    EgOH = max(EgOH, 0.0)
    p = (NA0 - EgOH) / NA0
    p = min(p, 0.999999)
    Xn = 1.0 / (1.0 - p)
    # Trava matemática para evitar o erro de Overflow no 'exp'
    argumento = np.clip(-theta * Xn, -700.0, 700.0)
    return kl_GT0 * np.exp(argumento)