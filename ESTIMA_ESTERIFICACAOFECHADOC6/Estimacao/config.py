import numpy as np
from dataclasses import dataclass

# ==========================================
# PROPRIEDADES FÍSICO-QUÍMICAS
# ==========================================
Rg = 82.05746      # atm.cm3/mol.K
MMN2 = 28.0134     # Massa Molar N2 (g/mol)
MMA = 146.14       # Massa Molar Ácido Adípico (g/mol)
MMEgE = 62.07      # Massa Molar Etilenoglicol (g/mol)
MMH2O = 18.015     # Massa Molar Água (g/mol)
densA = 1.36       # Densidade Ácido Adípico (g/cm3)
densEg = 1.11      # Densidade Etilenoglicol (g/cm3)
densH2O = 1.00     # Densidade da Água (g/cm3)  <--- A correção vital aqui
acerto = 273.15    # Conversão Celsius para Kelvin
rhoN2 = 1.139      # Densidade N2 a 1 atm e 25°C (g/L)

# ==========================================
# PARÂMETROS DO PROCESSO
# ==========================================
@dataclass
class ParametrosReator:
    EaE: float = 0.8
    AE: float = 0.17 * 2.10e-2
    Tflash: float = 125.0
    zz: float = 0.05
    deltaB: float = 220.0
    k_bomba: float = 950.0
    b: float = 0.7
    PC: float = 0.26
    EaT: float = 0.45
    AT: float = 5.0
    alpha: float = 0.26
    xf: float = 0.5
    Pr: float = 760.0 # mmHg

params = ParametrosReator()