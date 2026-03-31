import numpy as np
from scipy.optimize import differential_evolution, least_squares
import reator_dae

def funcao_objetivo_residuos(parametros, dados_exp, imod):
    """
    Calcula os resíduos ponderados (Máxima Verossimilhança).
    """
    tempos_exp = dados_exp['Tempo'][0]
    tempos_validos = np.unique(tempos_exp[tempos_exp > 0])
    
    if len(tempos_validos) == 0:
        return np.ones(10) * 1e6 # Penalidade alta se não houver tempo válido
        
    # Roda o reator (EDO)
    solucao = reator_dae.resolver_reator(
        t_span=(0, tempos_validos[-1]),
        Y0=dados_exp['Y0'],
        Rpar=parametros,
        Tp=dados_exp['Tp'],
        VzN2=dados_exp['VzN2'],
        imod=imod,
        NA0=dados_exp['NA0'],
        r=dados_exp['r'],
        t_eval=tempos_validos
    )
    
    if not solucao.success:
        return np.ones(len(tempos_validos) * 2) * 1e6
        
    H2O_calc = solucao.y[8, :]                   
    EG_calc = solucao.y[7, :] - solucao.y[8, :]  
    
    meio = len(tempos_validos)
    H2O_medido = dados_exp['YM'][0, :meio]
    EG_medido = dados_exp['YM'][0, meio:2*meio]
    
    if len(H2O_calc) != len(H2O_medido):
        return np.ones(meio * 2) * 1e6
        
    # -------------------------------------------------------------
    # PONDERAÇÃO ESTATÍSTICA (Equivalente ao EVYinv do Fortran)
    # -------------------------------------------------------------
    # Extrai a variância lida do arquivo .dat e tira a raiz (desvio padrão)
    erro_H2O = np.sqrt(dados_exp['EVY'][0, :meio])
    erro_EG = np.sqrt(dados_exp['EVY'][0, meio:2*meio])
    
    # Previne divisão por zero caso algum erro venha zerado do .dat
    erro_H2O = np.where(erro_H2O == 0, 1e-8, erro_H2O)
    erro_EG = np.where(erro_EG == 0, 1e-8, erro_EG)
    
    # Diferença PONDERADA (Máxima Verossimilhança)
    residuos_H2O = (H2O_calc - H2O_medido) / erro_H2O
    residuos_EG = (EG_calc - EG_medido) / erro_EG
    
    return np.concatenate((residuos_H2O, residuos_EG))

def estimar_parametros(limites_parametros, estimativa_inicial, dados_experimentais, imod):
    print("\n-> Iniciando busca global (Enxame de Partículas)...")
    print("   (Isso pode levar alguns minutos. Acompanhe a convergência abaixo:)")
    
    resultado_global = differential_evolution(
        lambda p: np.sum(funcao_objetivo_residuos(p, dados_experimentais, imod)**2),
        bounds=limites_parametros,
        strategy='best1bin',
        maxiter=30,
        disp=True 
    )
    
    print(f"\n-> Melhor parâmetro global encontrado: {resultado_global.x}")
    print("-> Iniciando refino local (Gauss-Newton/Levenberg-Marquardt)...")
    
    resultado_final = least_squares(
        funcao_objetivo_residuos,
        x0=resultado_global.x, 
        bounds=list(zip(*limites_parametros)),
        method='trf', 
        verbose=2,    
        args=(dados_experimentais, imod)
    )
    
    return resultado_final.x, resultado_final.jac