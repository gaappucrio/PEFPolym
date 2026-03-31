import numpy as np
import matplotlib.pyplot as plt
import utils
import otimizacao
import reator_dae
import config

def main():
    print("==========================================================")
    print(f" ESTIMAÇÃO DE PARÂMETROS - REATOR {config.VERSAO_ATUAL}")
    print("==========================================================")
    imod = config.IMOD_ATUAL
    print(f"Modo selecionado: {'Esterificação' if imod == 0 else 'Transesterificação'}")
    
    dados_exp = utils.ler_dados_experimentais()
    
    limites_parametros = [(-10.0, 0.0), (-5.0, 5.0), (-5.0, 5.0)] if imod == 0 else [(-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)]
    chute_inicial = [-5.0, 0.0, 0.0] if imod == 0 else [0.0, 0.0, 0.0]
    
    par_otimos, jacobiana = otimizacao.estimar_parametros(limites_parametros, chute_inicial, dados_exp, imod)
    
    print("\n==========================================================")
    print(f" Parâmetros Ótimos: {par_otimos}")
    try:
        desvio_padrao = np.sqrt(np.diag(np.linalg.inv(jacobiana.T @ jacobiana)))
        print(f" Desvio Padrão:     {desvio_padrao}")
    except np.linalg.LinAlgError:
        print(" Aviso: Matriz singular. Estatística exata indisponível.")
    print("==========================================================")
    
    plt.figure(figsize=(10, 6))
    
    if imod == 0:
        tempos_validos = np.unique(dados_exp['Tempo'][0][dados_exp['Tempo'][0] > 0])
        sol_otima = reator_dae.resolver_reator(
            (0, tempos_validos[-1]), dados_exp['Y0'], par_otimos, dados_exp['Tp'],
            dados_exp['VzN2'], imod, dados_exp['NA0'], dados_exp['r'], dados_exp['tempofinal'], tempos_validos
        )
        meio = len(tempos_validos)
        plt.plot(tempos_validos, dados_exp['YM'][0, :meio], 'bo', label='H2O Exp')
        plt.plot(tempos_validos, sol_otima.y[8, :], 'b-', label='H2O Mod')
        plt.plot(tempos_validos, dados_exp['YM'][0, meio:2*meio], 'ro', label='EG Exp')
        plt.plot(tempos_validos, sol_otima.y[7, :] - sol_otima.y[8, :], 'r-', label='EG Mod')
    else:
        t_max = max(np.max(dados_exp['Tempo'][0]), np.max(dados_exp['Tempos_Medidos']))
        sol_otima = reator_dae.resolver_reator(
            (0, t_max), dados_exp['Y0'], par_otimos, dados_exp['Tp'],
            dados_exp['VzN2'], imod, dados_exp['NA0'], dados_exp['r'], dados_exp['tempofinal']
        )
        
        # Plota a linha do modelo de forma suave
        t_plot = sol_otima.t
        EG_calc_plot = sol_otima.y[7, :] - sol_otima.y[8, :]
        plt.plot(t_plot, EG_calc_plot, 'r-', label='EG Destilado Mod')
        
        # Plota apenas os pontos coletados pelo laboratório
        Nx = dados_exp['Nx_val']
        tempos_medidos = dados_exp['Tempos_Medidos'][:Nx]
        EG_medido = dados_exp['YM'][0, :Nx]
        plt.plot(tempos_medidos, EG_medido, 'ro', label='EG Destilado Exp')

    plt.title(f'Validação: {config.VERSAO_ATUAL} (Fase {imod})')
    plt.xlabel('Tempo (min)')
    plt.ylabel('Massa Acumulada (g)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()