import numpy as np
import matplotlib.pyplot as plt
import utils
import otimizacao
import reator_dae

def main():
    print("==========================================================")
    print(" ESTIMAÇÃO DE PARÂMETROS - REATOR DE POLICONDENSAÇÃO")
    print("==========================================================")
    
    # ---------------------------------------------------------
    # CONFIGURAÇÃO DA ETAPA DO PROCESSO
    # 0 = Esterificação
    # 1 = Transesterificação
    # ---------------------------------------------------------
    imod = 0  
    print(f"Modo selecionado: {'Esterificação' if imod == 0 else 'Transesterificação'}")
    
    dados_exp = utils.ler_dados_experimentais()
    
    limites_parametros = [
        (-10.0, 0.0), 
        (-5.0, 5.0),  
        (-5.0, 5.0)   
    ]
    chute_inicial = [-5.0, 0.0, 0.0]
    
    parametros_otimos, jacobiana = otimizacao.estimar_parametros(
        limites_parametros, chute_inicial, dados_exp, imod
    )
    
    print("\n==========================================================")
    print(" OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f" Parâmetros Ótimos: {parametros_otimos}")
    
    # ---------------------------------------------------------
    # CÁLCULO DE ESTATÍSTICAS (Matriz de Covariância)
    # ---------------------------------------------------------
    # A Hessiana é aproximada por (Jacobiana Transposta * Jacobiana)
    Hessiana = jacobiana.T @ jacobiana
    try:
        CovPar = np.linalg.inv(Hessiana)
        desvio_padrao = np.sqrt(np.diag(CovPar))
        print(f" Desvio Padrão:     {desvio_padrao}")
    except np.linalg.LinAlgError:
        print(" Aviso: Matriz singular. Não foi possível calcular o desvio padrão exato.")
    print("==========================================================")
    
    
    print("Gerando gráfico de validação...")
    tempos_exp = dados_exp['Tempo'][0]
    tempos_validos = np.unique(tempos_exp[tempos_exp > 0])
    meio = len(tempos_validos)
    
    H2O_medido = dados_exp['YM'][0, :meio]
    EG_medido = dados_exp['YM'][0, meio:2*meio]
    
    sol_otima = reator_dae.resolver_reator(
        t_span=(0, tempos_validos[-1]),
        Y0=dados_exp['Y0'], Rpar=parametros_otimos, Tp=dados_exp['Tp'],
        VzN2=dados_exp['VzN2'], imod=imod, NA0=dados_exp['NA0'],
        r=dados_exp['r'], t_eval=tempos_validos
    )
    
    H2O_calc = sol_otima.y[8, :]
    EG_calc = sol_otima.y[7, :] - sol_otima.y[8, :]
    
    plt.figure(figsize=(10, 6))
    plt.plot(tempos_validos, H2O_medido, 'bo', label='H2O (Experimental)')
    plt.plot(tempos_validos, H2O_calc, 'b-', label='H2O (Modelo)')
    
    plt.plot(tempos_validos, EG_medido, 'ro', label='EG (Experimental)')
    plt.plot(tempos_validos, EG_calc, 'r-', label='EG (Modelo)')
    
    plt.title('Validação do Modelo: Condensados Acumulados')
    plt.xlabel('Tempo (min)')
    plt.ylabel('Massa Acumulada (g)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()