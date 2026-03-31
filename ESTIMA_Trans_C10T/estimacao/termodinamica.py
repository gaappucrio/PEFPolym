import numpy as np
import config

def pressao_saturacao_antoine(Temp_C):
    AHT, BHT, CHT = 16.3872, 3885.70, 230.17
    AET, BET, CET = 15.7567, 4187.46, 178.650

    PsatH2O_kPa = np.exp(AHT - (BHT / (CHT + Temp_C)))
    PsatEG_kPa  = np.exp(AET - (BET / (CET + Temp_C)))

    fator_conv = 760.0 * 0.986923 / 100.0
    return PsatEG_kPa * fator_conv, PsatH2O_kPa * fator_conv

def calcular_equilibrio(Xn, Temp_C, yH2O, yEG, Phi_pol):
    PsatEG, PsatH2O = pressao_saturacao_antoine(Temp_C)
    
    # Travas para evitar overflow numérico
    Phi_pol = np.clip(Phi_pol, 0.0, 1.0)
    expoente = np.clip((1.0 - (1.0 / Xn)) * Phi_pol + config.params.xf * (Phi_pol ** 2.0), -700.0, 700.0)
    
    termo_fh = np.exp(expoente)
    PhiH2O_int = (yH2O * config.params.Pr) / (termo_fh * PsatH2O)
    PhiEG_int  = (yEG * config.params.Pr) / (termo_fh * PsatEG)
    return np.array([PhiH2O_int, PhiEG_int, 0.0, 0.0])

def equilibrio_trans(Tp, Phi_pol, Phi_EG, xf):
    PsatEG_mmHg, _ = pressao_saturacao_antoine(Tp)
    
    # Travas físicas e matemáticas para o 'exp' não explodir
    Phi_pol = np.clip(Phi_pol, 0.0, 1.0)
    Phi_EG = np.clip(Phi_EG, 0.0, 1.0)
    expoente = np.clip(Phi_pol + xf * (Phi_pol ** 2.0), -700.0, 700.0)
    
    fEG_bulk_mmHg = Phi_EG * np.exp(expoente) * PsatEG_mmHg
    return fEG_bulk_mmHg / 760.0

def calcular_volume_parcial(Y, densA, densEg, MMA, MMEgE):
    Ec, EG = max(Y[0], 0.0), max(Y[1], 0.0)
    VEG = (EG * MMEgE) / densEg
    Vp = ((Ec / 2.0) * MMA) / densA
    return np.array([0.0, VEG, Vp])