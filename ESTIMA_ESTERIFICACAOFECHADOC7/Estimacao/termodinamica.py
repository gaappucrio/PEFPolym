import numpy as np
from config import params

def pressao_saturacao_antoine(Temp_C):
    """
    Substitui a SUBROUTINE Antoine.
    Retorna as pressões de saturação (PsatEG, PsatH2O) em mmHg.
    """
    # Constantes de Antoine para H2O e EgE
    AHT, BHT, CHT = 16.3872, 3885.70, 230.17
    AET, BET, CET = 15.7567, 4187.46, 178.650

    # Pressão em kPa
    PsatH2O_kPa = np.exp(AHT - (BHT / (CHT + Temp_C)))
    PsatEG_kPa  = np.exp(AET - (BET / (CET + Temp_C)))

    # Conversão kPa para mmHg
    fator_conv = 760.0 * 0.986923 / 100.0
    PsatH2O_mmHg = PsatH2O_kPa * fator_conv
    PsatEG_mmHg  = PsatEG_kPa * fator_conv

    return PsatEG_mmHg, PsatH2O_mmHg

def calcular_equilibrio(Xn, Temp_C, yH2O, yEG, Phi_pol):
    """
    Substitui a SUBROUTINE Equilibrio.
    Retorna as frações volumétricas na interface do líquido.
    """
    PsatEG, PsatH2O = pressao_saturacao_antoine(Temp_C)
    
    # Cálculo do denominador comum (Flory-Huggins)
    expoente = (1.0 - (1.0 / Xn)) * Phi_pol + params.xf * (Phi_pol ** 2.0)
    termo_fh = np.exp(expoente)
    
    PhiH2O_int = (yH2O * params.Pr) / (termo_fh * PsatH2O)
    PhiEG_int  = (yEG * params.Pr) / (termo_fh * PsatEG)
    
    # Retorna Phi_int = [PhiH2O, PhiEG, 0, 0] como no Fortran original
    return np.array([PhiH2O_int, PhiEG_int, 0.0, 0.0])

def calcular_volume_parcial(Y, densA, densEg, MMA, MMEgE):
    """
    Substitui a SUBROUTINE Volume e VolumeTrans.
    Calcula os volumes parciais dos componentes no líquido.
    Y[0] = Ec (Ácido), Y[1] = EG (Etilenoglicol)
    """
    Ec = Y[0]
    EG = Y[1]
    
    # Volume parcial da Água (VH2O) - Assumido 0 inicial se não houver água líquida acumulada
    VH2O = 0.0 
    
    # Volume parcial do EG (VEG)
    VEG = (EG * MMEgE) / densEg
    
    # Volume do Polímero (Vp) baseado no ácido adípico (Ec / 2 = A)
    A = Ec / 2.0
    Vp = (A * MMA) / densA
    
    # Retorna o vetor Vpar equivalente ao Fortran: [VH2O, VEG, Vp]
    return np.array([VH2O, VEG, Vp])