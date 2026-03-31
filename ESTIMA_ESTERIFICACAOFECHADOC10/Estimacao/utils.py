import numpy as np
import config

def leitor_fortran(caminho_arquivo):
    """Lê arquivos .dat ignorando espaços e tratando notação 'd' do Fortran."""
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            tokens = linha.split('!')[0].split()
            for token in tokens:
                yield float(token.lower().replace('d', 'e'))

def ler_dados_experimentais():
    """Substitui a SUBROUTINE Leitura[cite: 1]."""
    print(f"Lendo dados para a versão: {config.VERSAO_ATUAL}")
    
    # Leitura de dimensões (dadosexp.dat) [cite: 8]
    leitor_dados = leitor_fortran('dadosexp.dat')
    Nexp = int(next(leitor_dados))
    NVsai_lido = int(next(leitor_dados))
    Nx_val = int(next(leitor_dados))
    dadoMn_val = int(next(leitor_dados))
    
    # Leitura de experimentos (exp.dat) [cite: 13]
    leitor_exp = leitor_fortran('exp.dat')
    NVsai = 2 * Nx_val + dadoMn_val
    
    Tempo = np.zeros((Nexp, NVsai))
    YM = np.zeros((Nexp, NVsai))
    EVY = np.zeros((Nexp, NVsai))
    
    Tp_inicial = next(leitor_exp)   # [cite: 14]
    VzN2_bruto = next(leitor_exp)   # [cite: 15]
    mudaC7_val = int(next(leitor_exp)) # [cite: 16]
    
    # Loop de leitura dos dados [cite: 17, 18]
    aux = mudaC7_val - 1
    for j in range(aux):
        Tempo[0, j] = next(leitor_exp)
        YM[0, j] = next(leitor_exp)        # Água
        YM[0, aux + j] = next(leitor_exp)  # EG
        # Erros experimentais [cite: 19]
        EVY[0, j] = 0.281766539**2.0
        EVY[0, aux + j] = 0.841766539**2.0
    
    # Condições Iniciais baseadas no config.py [cite: 25]
    VzN2 = VzN2_bruto * config.rhoN2 / config.MMN2 # [cite: 26]
    
    A_mol = 14.0 / config.MMA     # [cite: 27]
    EG_mol = 22.3 / config.MMEgE   # [cite: 29]
    Ec = A_mol * 2.0               # [cite: 28]
    
    Y0 = np.zeros(13)
    Y0[0], Y0[1] = Ec, EG_mol      # [cite: 39]
    Y0[6] = (config.MMA * A_mol / config.densA) + (config.MMEgE * EG_mol / config.densEg) # [cite: 36]
    
    Vg = config.V_reator - Y0[6]   # [cite: 41]
    Y0[11] = 1.0 * Vg / (config.Rg * (Tp_inicial + config.acerto)) # [cite: 41]
    Y0[12] = 1.01                  # beta [cite: 41]
    
    return {
        'Y0': Y0, 'Tp': Tp_inicial, 'VzN2': VzN2, 
        'NA0': 2.0 * A_mol, 'r': (2.0 * A_mol) / (2.0 * EG_mol),
        'Tempo': Tempo, 'YM': YM, 'EVY': EVY, 'Nexp': Nexp
    }