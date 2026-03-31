import numpy as np
from dataclasses import dataclass

# ====================================================================
# CONFIGURAÇÃO GLOBAL DO EXPERIMENTO
# ====================================================================
VERSAO_ATUAL = 'C10'  
IMOD_ATUAL = 1       

COMPOSTOS = {
    'C6':  {'MMA': 146.14, 'densA': 1.360, 'densP': 1.10, 'V_reator': 500.0, 'zz': 0.050, 'deltaB': 220.0, 'k_bomba': 950.0},
    'C7':  {'MMA': 156.00, 'densA': 1.604, 'densP': 1.70, 'V_reator': 50.0,  'zz': 0.050, 'deltaB': 170.0, 'k_bomba': 950.0},
    'C8':  {'MMA': 156.00, 'densA': 1.604, 'densP': 1.70, 'V_reator': 50.0,  'zz': 0.035, 'deltaB': 225.0, 'k_bomba': 950.0},
    'C10': {'MMA': 156.00, 'densA': 1.604, 'densP': 1.70, 'V_reator': 50.0,  'zz': 0.035, 'deltaB': 225.0, 'k_bomba': 950.0},
}

comp = COMPOSTOS[VERSAO_ATUAL]

Rg, MMH2O, MMEgE, MMN2 = 82.06, 18.0, 62.068, 28.0         
MMA, densA, densP = comp['MMA'], comp['densA'], comp['densP']
densEg, densH2O = 1.11, 1.0      
rhoN2, V_reator, acerto = 1.1455e-3, comp['V_reator'], 273.15    

@dataclass
class ParametrosReator:
    xf: float = 0.5
    Pr: float = 760.0
    Tflash: float = 125.0
    EaE: float = 0.8
    AE: float = 0.17 * 2.10e-2
    EaT: float = 0.45
    AT: float = 5.0
    alpha: float = 0.26
    PC: float = 0.26
    b: float = 0.7
    zz: float = comp['zz']
    deltaB: float = comp['deltaB']
    k_bomba: float = comp['k_bomba']
    
    # "Memória" da Fase 1: Parâmetros ótimos encontrados na Esterificação!
    Epar: tuple = (-9.9998, -2.9976, -2.1089)

params = ParametrosReator()