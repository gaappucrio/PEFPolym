import numpy as np
from dataclasses import dataclass

# ====================================================================
# BANCO DE DADOS DE COMPOSTOS (Unifica C6, C7, C8 e C10)
# ====================================================================
# Dados extraídos de Propriedades.F90 e Parametros.F90
COMPOSTOS = {
    'C6':  {
        'MMA': 146.14, 
        'densA': 1.36,  
        'densP': 1.10,
        'V_reator': 500.0 # Volume genérico do C6
    },
    'C10': {
        'MMA': 156.00,  # [cite: 57]
        'densA': 1.604, # [cite: 58]
        'densP': 1.70,  # [cite: 58]
        'V_reator': 50.0 # [cite: 58]
    },
    # Adicione C7 e C8 aqui seguindo o mesmo padrão quando tiver os dados
}

# SELEÇÃO GLOBAL: Altere aqui para 'C6' ou 'C10' para mudar o projeto inteiro
VERSAO_ATUAL = 'C10' 

# ====================================================================
# PROPRIEDADES FÍSICO-QUÍMICAS (Automáticas)
# ====================================================================
comp = COMPOSTOS[VERSAO_ATUAL]

Rg = 82.06         # [cite: 60]
MMH2O = 18.0       # [cite: 57]
MMEgE = 62.068     # [cite: 57]
MMN2 = 28.0        # [cite: 57]
MMA = comp['MMA']  
densA = comp['densA']
densEg = 1.11      # [cite: 58]
densH2O = 1.0      # [cite: 58]
densP = comp['densP']
rhoN2 = 1.1455e-3  # [cite: 58]
V_reator = comp['V_reator']
acerto = 273.15    # [cite: 60]

@dataclass
class ParametrosReator:
    # Esterificação (MODO 0) -
    EaE: float = 0.8
    AE: float = 0.17 * 2.10e-2
    Tflash: float = 125.0
    xf: float = 0.5
    Pr: float = 760.0
    
    # Transesterificação (MODO 1) -
    EaT: float = 0.45
    AT: float = 5.0
    alpha: float = 0.26
    PC: float = 0.26
    b: float = 0.7
    zz: float = 0.05
    deltaB: float = 220.0
    k_bomba: float = 950.0

params = ParametrosReator()