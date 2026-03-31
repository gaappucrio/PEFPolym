import numpy as np
import config

def leitor_fortran(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            for token in linha.split('!')[0].split():
                yield float(token.lower().replace('d', 'e'))

def ler_dados_experimentais():
    imod = config.IMOD_ATUAL
    leitor_dados = leitor_fortran('dadosexp.dat')
    Nexp = int(next(leitor_dados))
    
    Nx_val, dadoMn_val = 0, 0
    
    if imod == 0:
        NVsai = 2 * int(next(leitor_dados)) + int(next(leitor_dados))
    else:
        Nx_val = int(next(leitor_dados))
        dadoMn_val = int(next(leitor_dados))
        Nest = int(next(leitor_dados))
        Ntempao = int(next(leitor_dados))
        NVsai = Nx_val + dadoMn_val

    leitor_exp = leitor_fortran('exp.dat')
    Tp_inicial = next(leitor_exp)
    VzN2_bruto = next(leitor_exp)
    mudaC7_val = int(next(leitor_exp))

    Tempo = np.zeros((1, NVsai if imod == 0 else max(Ntempao, NVsai)))
    YM, EVY = np.zeros((1, NVsai)), np.zeros((1, NVsai))
    Tempos_Medidos = np.zeros(NVsai)  # Novo vetor específico para os dados do Lab
    tempofinal = 0.0

    if imod == 0:
        aux = mudaC7_val - 1
        for j in range(aux):
            Tempo[0, j] = next(leitor_exp)
            YM[0, j], YM[0, aux + j] = next(leitor_exp), next(leitor_exp)
            EVY[0, j], EVY[0, aux + j] = 0.281766539**2.0, 0.841766539**2.0
    else:
        for j in range(Ntempao):
            Tempo[0, j] = next(leitor_exp)
        
        tempofinal = Tempo[0, max(0, mudaC7_val - 2)]
        
        for j in range(Nx_val):
            Tempos_Medidos[j] = next(leitor_exp) 
            YM[0, j] = next(leitor_exp)
            EVY[0, j] = 0.801766539**2.0
            
        for j in range(dadoMn_val):
            Tempos_Medidos[Nx_val + j] = next(leitor_exp)
            YM[0, Nx_val + j] = next(leitor_exp)
            EVY[0, Nx_val + j] = 35.0**2.0

    A_mol = 14.0 / config.MMA
    EG_mol = 22.3 / config.MMEgE
    
    Y0 = np.zeros(13)
    Y0[0], Y0[1] = A_mol * 2.0, EG_mol
    Y0[6] = (config.MMA * A_mol / config.densA) + (config.MMEgE * EG_mol / config.densEg)
    Y0[11] = 1.0 * (config.V_reator - Y0[6]) / (config.Rg * (Tp_inicial + config.acerto))
    Y0[12] = 1.01

    return {
        'Y0': Y0, 'Tp': Tp_inicial, 'VzN2': VzN2_bruto * config.rhoN2 / config.MMN2,
        'NA0': 2.0 * A_mol, 'r': (2.0 * A_mol) / (2.0 * EG_mol),
        'Tempo': Tempo, 'YM': YM, 'EVY': EVY, 'Nexp': Nexp, 'tempofinal': tempofinal,
        'Tempos_Medidos': Tempos_Medidos, 'Nx_val': Nx_val, 'dadoMn_val': dadoMn_val
    }