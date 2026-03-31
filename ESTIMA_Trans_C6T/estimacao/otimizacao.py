import numpy as np
from scipy.optimize import differential_evolution, least_squares
import reator_dae

def funcao_objetivo_residuos(parametros, dados_exp, imod):
    if imod == 0:
        tempos_exp = dados_exp['Tempo'][0]
        tempos_validos = np.unique(tempos_exp[tempos_exp > 0])
        if len(tempos_validos) == 0: return np.ones(10) * 1e6
            
        solucao = reator_dae.resolver_reator(
            t_span=(0, tempos_validos[-1]), Y0=dados_exp['Y0'], Rpar=parametros,
            Tp=dados_exp['Tp'], VzN2=dados_exp['VzN2'], imod=imod, NA0=dados_exp['NA0'],
            r=dados_exp['r'], tempofinal=dados_exp['tempofinal'], t_eval=tempos_validos
        )
        if not solucao.success: return np.ones(len(tempos_validos) * 2) * 1e6
            
        EG_calc = solucao.y[7, :] - solucao.y[8, :]
        meio = len(tempos_validos)
        H2O_calc = solucao.y[8, :]
        H2O_medido = dados_exp['YM'][0, :meio]
        EG_medido = dados_exp['YM'][0, meio:2*meio]
        
        if len(H2O_calc) != len(H2O_medido): return np.ones(meio * 2) * 1e6
        
        e_H2O = np.where(np.sqrt(dados_exp['EVY'][0, :meio]) == 0, 1e-8, np.sqrt(dados_exp['EVY'][0, :meio]))
        e_EG = np.where(np.sqrt(dados_exp['EVY'][0, meio:2*meio]) == 0, 1e-8, np.sqrt(dados_exp['EVY'][0, meio:2*meio]))
        
        return np.concatenate(((H2O_calc - H2O_medido) / e_H2O, (EG_calc - EG_medido) / e_EG))
        
    else:
        # Pega o maior tempo entre a simulação e os dados do lab
        t_max = max(np.max(dados_exp['Tempo'][0]), np.max(dados_exp['Tempos_Medidos']))
        
        solucao = reator_dae.resolver_reator(
            t_span=(0, t_max), Y0=dados_exp['Y0'], Rpar=parametros,
            Tp=dados_exp['Tp'], VzN2=dados_exp['VzN2'], imod=imod, NA0=dados_exp['NA0'],
            r=dados_exp['r'], tempofinal=dados_exp['tempofinal']
        )
        if not solucao.success: return np.ones(dados_exp['Nx_val']) * 1e6
        
        # Extrai a resposta contínua exatamente nos segundos coletados no laboratório
        Y_calc_nos_pontos = solucao.sol(dados_exp['Tempos_Medidos'])
        EG_calc = Y_calc_nos_pontos[7, :] - Y_calc_nos_pontos[8, :]
        
        Nx = dados_exp['Nx_val']
        calc_val = EG_calc[:Nx]
        medido = dados_exp['YM'][0, :Nx]
        erro = np.where(np.sqrt(dados_exp['EVY'][0, :Nx]) == 0, 1e-8, np.sqrt(dados_exp['EVY'][0, :Nx]))
        
        return (calc_val - medido) / erro

def estimar_parametros(limites_parametros, estimativa_inicial, dados_experimentais, imod):
    print("\n-> Iniciando busca global (Enxame de Partículas)...")
    res_global = differential_evolution(
        lambda p: np.sum(funcao_objetivo_residuos(p, dados_experimentais, imod)**2),
        bounds=limites_parametros, strategy='best1bin', maxiter=30, disp=True 
    )
    print("-> Iniciando refino local (Gauss-Newton/Levenberg-Marquardt)...")
    res_final = least_squares(
        funcao_objetivo_residuos, x0=res_global.x, bounds=list(zip(*limites_parametros)),
        method='trf', verbose=2, args=(dados_experimentais, imod)
    )
    return res_final.x, res_final.jac