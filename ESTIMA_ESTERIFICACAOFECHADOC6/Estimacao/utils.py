import numpy as np
from config import *

def leitor_fortran(caminho_arquivo):
    """
    Simula o comportamento do `READ(*,*)` do Fortran.
    Lê o arquivo como um fluxo contínuo de dados, ignorando espaços e quebras de linha.
    Converte automaticamente a notação científica 'd' do Fortran para 'e' do Python.
    """
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            # Ignora comentários se houver
            linha_sem_comentario = linha.split('!')[0] 
            tokens = linha_sem_comentario.split()
            for token in tokens:
                # Troca 'd' ou 'D' por 'e' para o Python entender a notação científica
                token_python = token.lower().replace('d', 'e')
                yield float(token_python)

def ler_dados_experimentais():
    """
    Lê os arquivos dadosexp.dat e exp.dat mantendo a lógica do Leitura.f90 original.
    """
    print("Lendo arquivos de dados experimentais...")
    
    # ---------------------------------------------------------
    # 1. Leitura do dadosexp.dat
    # ---------------------------------------------------------
    leitor_dados = leitor_fortran('dadosexp.dat')
    
    Nexp = int(next(leitor_dados))
    NVsai = int(next(leitor_dados))
    Nx = int(next(leitor_dados))
    dadoMn = int(next(leitor_dados))
    
    # ---------------------------------------------------------
    # 2. Leitura do exp.dat (Experimentos)
    # ---------------------------------------------------------
    leitor_exp = leitor_fortran('exp.dat')
    
    Tempo = np.zeros((Nexp, NVsai))
    YM = np.zeros((Nexp, NVsai))
    EVY = np.zeros((Nexp, NVsai)) # Erro experimental
    
    Tp_inicial = 0.0
    VzN2_inicial = 0.0
    
    for i in range(Nexp):
        Temp_C = next(leitor_exp)
        VzN2_lido = next(leitor_exp)
        mudaC7 = int(next(leitor_exp))
        
        if i == 0:
            Tp_inicial = Temp_C
            VzN2_inicial = VzN2_lido
        
        # Lendo os dados da esterificação (Tempo, Água, EG)
        for j in range(mudaC7 - 1):
            aux = mudaC7 - 1
            
            Tempo[i, j] = next(leitor_exp)
            YM[i, j] = next(leitor_exp)        # Água
            YM[i, aux + j] = next(leitor_exp)  # EG
            
            # Matriz de covariância dos erros experimentais (valores fixos do Fortran)
            EVY[i, j] = 0.281766539**2.0
            EVY[i, aux + j] = 0.281766539**2.0
            
        # Replicando a lógica do Fortran para o restante do vetor de tempo
        Tempo[i, mudaC7-1:] = Tempo[i, :mudaC7-1]
        
    # ---------------------------------------------------------
    # 3. Construção das Condições Iniciais (Y0)
    # ---------------------------------------------------------
    Y0 = np.zeros(13)
    
    VzN2 = VzN2_inicial * rhoN2 / MMN2
    
    # Fase Líquida
    A = 14.0 / MMA
    Ec = A * 2.0
    EG = 22.3 / MMEgE
    
    Y0[0] = Ec      # Ec
    Y0[1] = EG      # EG
    Y0[2] = 0.0     # E_g
    Y0[3] = 0.0     # H2O
    Y0[4] = 0.0     # Z
    Y0[5] = 0.0     # EgOH
    
    V = MMA * A / densA + MMEgE * EG / densEg
    Y0[6] = V       # Volume
    Y0[7] = 0.0     # Mac
    Y0[8] = 0.0     # MacH2O
    
    # Fase Gás
    Y0[9] = 0.0     # nEG
    Y0[10] = 0.0    # nH2O
    Vg = 500.0 - V  
    Y0[11] = 1.0 * Vg / (Rg * (Tp_inicial + acerto)) # nN2
    Y0[12] = 1.01   # beta (Razão V/F)
    
    NA0 = 2.0 * A
    NB0 = 2.0 * EG
    r_razao = NA0 / NB0
    
    print("Leitura concluída com sucesso.")
    
    return {
        'Y0': Y0,
        'Tp': Tp_inicial,
        'VzN2': VzN2,
        'NA0': NA0,
        'r': r_razao,
        'Tempo': Tempo,
        'YM': YM,
        'EVY': EVY,  # <--- CORREÇÃO AQUI
        'Nexp': Nexp,
        't_span': (0, np.max(Tempo[0])) 
    }