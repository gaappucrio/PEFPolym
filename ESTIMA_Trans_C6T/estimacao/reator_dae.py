import numpy as np
from scipy.integrate import solve_ivp
import config
import termodinamica
import cinetica

def taxa_reacao(Tp, Y, Rpar_ativo, imod_local):
    Ec, EG, V = max(Y[0], 0.0), max(Y[1], 0.0), max(Y[6], 1e-6)
    if imod_local == 0:
        k1d = 10.0 ** Rpar_ativo[0]
        EgOH = max(Y[5], 0.0)
        return k1d * (Ec / V) * (EG / V), k1d * (Ec / V) * (EgOH / V), 0.0
    else:
        k2d = 10.0 ** Rpar_ativo[0]
        EgOH = max(Y[5], 0.0)
        return k2d * ((EgOH / V) ** 2.0), 0.0, 0.0

def equacoes_diferenciais(t, Y, Rpar, Tp, VzN2, imod_global, NA0, r, tempofinal=0.0):
    dYdt = np.zeros_like(Y)
    
    # Mágica Dinâmica: Transição contínua entre Fase 1 e Fase 2 no tempo correto
    if imod_global == 1 and t <= tempofinal:
        imod_local = 0
        Rpar_ativo = config.params.Epar  
    else:
        imod_local = imod_global
        Rpar_ativo = Rpar               
        
    Ec, EG, E_g, H2O, Z, EgOH, V = Y[0:7]
    nEG, nH2O, nN2 = Y[9], Y[10], Y[11]

    # Prevenção numérica absoluta (trava de segurança)
    Ec, EG, EgOH, V = max(Ec, 0.0), max(EG, 0.0), max(EgOH, 0.0), max(V, 1e-6)

    # Cálculo dos volumes parciais
    Vpar = termodinamica.calcular_volume_parcial(Y, config.densA, config.densEg, config.MMA, config.MMEgE)
    Phi_H2O = np.clip(Vpar[0] / V, 0.0, 1.0)
    Phi_EG  = np.clip(Vpar[1] / V, 0.0, 1.0)
    
    # Adaptação crucial do VolumeTrans.f90 / RES.f90
    if imod_local == 0:
        Phi_pol = np.clip(Vpar[2] / V, 0.0, 1.0)
    else:
        # Na transesterificação, o volume do polímero é calculado por diferença
        Phi_pol = np.clip(1.0 - Phi_EG, 0.0, 1.0)
    
    Mn, Xn = cinetica.propriedades_polimero(Ec if imod_local==0 else EgOH, r, NA0, imod_local)
    Taxa, Taxa2, Taxa3 = taxa_reacao(Tp, Y, Rpar_ativo, imod_local)

    if imod_local == 0:
        kl_G, kl_A = 10.0 ** Rpar_ativo[1], 10.0 ** Rpar_ativo[2]
        ntot = max(nEG + nH2O + nN2, 1e-12)
        zEG, zH2O, zN2 = nEG / ntot, nH2O / ntot, nN2 / ntot

        Phi_int = termodinamica.calcular_equilibrio(Xn, Tp, zH2O, zEG, Phi_pol)
        termo_exp = np.exp(np.clip((1.0 - (1.0 / Xn)) * Phi_pol + config.params.xf * Phi_pol**2.0, -700.0, 700.0))
        nEG_l = kl_G * termo_exp * max(Phi_EG - Phi_int[1], 0.0)
        nH2O_l = kl_A * termo_exp * max(Phi_H2O - Phi_int[0], 0.0)

        Ftot = VzN2 + nEG_l + nH2O_l
        PsatEG, PsatH2O = termodinamica.pressao_saturacao_antoine(config.params.Tflash)
        Keg, KH2O = PsatEG / config.params.Pr, PsatH2O / config.params.Pr
        xEG = zEG / (Y[12] * (Keg - 1.0) + 1.0)
        xH2O = zH2O / (Y[12] * (KH2O - 1.0) + 1.0)
        L = Ftot - (Y[12] * Ftot)

        dYdt[0] = -Taxa*V - Taxa2*V + Taxa3*V
        dYdt[1] = -Taxa*V - Taxa3*V - nEG_l + L*xEG
        dYdt[2] = 2.0 * Taxa2 * V
        dYdt[3] = Taxa*V + Taxa2*V - nH2O_l + L*xH2O
        dYdt[4] = Taxa3*V
        dYdt[5] = Taxa*V - Taxa2*V - Taxa3*V
        dYdt[6] = -nEG_l*(config.MMEgE/config.densEg) - nH2O_l*(config.MMH2O/config.densH2O)
        dYdt[7] = (zH2O * Ftot * config.MMH2O) + (zEG * Ftot * config.MMEgE)
        dYdt[8] = (zH2O * Ftot * config.MMH2O)
        dYdt[9], dYdt[10], dYdt[11] = nEG_l - zEG*Ftot, nH2O_l - zH2O*Ftot, VzN2 - zN2*Ftot

    elif imod_local == 1:
        nEGm, nH2O, nN2 = max(Y[9], 1e-40), max(Y[10], 0.0), max(Y[11], 0.0)
        ntot = max(nEGm + nH2O + nN2, 1e-12)
        yEG, yH2O, yN2 = nEGm / ntot, nH2O / ntot, nN2 / ntot

        Vg = max(config.V_reator - V, 1e-6)
        Ptot = ntot * config.Rg * (Tp + config.acerto) / Vg
        kl_GT = cinetica.modifica_kl_trans(EgOH, NA0, 10.0 ** Rpar_ativo[1], 10.0 ** Rpar_ativo[2])

        fEG_bulk = termodinamica.equilibrio_trans(Tp, Phi_pol, Phi_EG, config.params.xf)
        nEG_evap = kl_GT * max(fEG_bulk - (yEG * Ptot), 0.0)

        ff = 1.0 / (1.0 + np.exp(-config.params.zz * (t - tempofinal - config.params.deltaB)))
        nb = (Ptot / (config.Rg * (Tp + config.acerto))) * (config.params.k_bomba * ff * Ptot)

        dYdt[1] = Taxa * V - nEG_evap
        dYdt[4] = Taxa * V
        dYdt[5] = -2.0 * Taxa * V
        dYdt[6] = -nEG_evap * (config.MMEgE / config.densEg)
        dYdt[7] = (yH2O * nb * config.MMH2O) + (yEG * nb * config.MMEgE)
        dYdt[8] = (yH2O * nb * config.MMH2O)
        dYdt[9], dYdt[10], dYdt[11] = nEG_evap - yEG * nb, -yH2O * nb, -yN2 * nb

    return dYdt

def resolver_reator(t_span, Y0, Rpar, Tp, VzN2, imod, NA0, r, tempofinal=0.0, t_eval=None):
    return solve_ivp(
        fun=lambda t, y: equacoes_diferenciais(t, y, Rpar, Tp, VzN2, imod, NA0, r, tempofinal),
        t_span=t_span, y0=Y0, method='BDF', t_eval=t_eval, dense_output=True, rtol=1e-5, atol=1e-5
    )