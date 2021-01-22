import pandas as pd
import numpy as np


def codificar_inputs(filepath=None):
    inputs_codificados = {}
    clases_df, profes_df, horas_df = extraer_inputs(filepath=filepath) if filepath else extraer_inputs()
    clases, asignaturas, profesores, franjas = \
        generar_clases_asignaturas_profesores_franjas(clases_df, profes_df, horas_df)
    HCA, PCA = generar_HCA_PCA(clases_df, clases, asignaturas, profesores)
    DPF = generar_DPF(profes_df, horas_df, franjas, profesores)

    inputs_codificados['clases'] = clases
    inputs_codificados['asignaturas'] = asignaturas
    inputs_codificados['profesores'] = profesores
    inputs_codificados['franjas'] = franjas
    inputs_codificados['HCA'] = HCA
    inputs_codificados['PCA'] = PCA
    inputs_codificados['DPF'] = DPF

    # Muevo algunos cálculos aquí para evitar calcularlo en cada genotipo varias veces
    inputs_codificados['horas_clase'] = [sum(clase) for clase in HCA]
    dias = ['L', 'M', 'X', 'J', 'V']
    inputs_codificados['horas_por_dia'] = [sum([dias[i] in f for f in franjas]) for i in range(len(dias))]
    inputs_codificados['max_dias_libres'] = max_dias_libres_clases(inputs_codificados['horas_por_dia'],
                                                                  inputs_codificados['horas_clase'])

    inputs_codificados['reparto_ideal_huecos_clases'] = reparto_ideal_huecos_clases(inputs_codificados['horas_por_dia'],
                                                                  inputs_codificados['horas_clase'],
                                                                  inputs_codificados['max_dias_libres'])

    horas_profe = [0 for _ in profesores]
    for a, asign in enumerate(asignaturas):
        for c, clase in enumerate(HCA):
            horas_asign_clase = clase[a]
            idx_profe = PCA[c][a] - 1
            horas_profe[idx_profe] += horas_asign_clase

    inputs_codificados['reparto_ideal_huecos_profe'] = reparto_ideal_huecos_profes(inputs_codificados['horas_por_dia'],
                                                                                   horas_profe, profes_df)

    return inputs_codificados

def extraer_inputs(filepath='.\\datos\\Generador inputs horarios 4.xlsx'):
    '''
    Extrae inputs del excel, eliminando filas y columnas vacías.
    Devuelve tres dataframes
    '''
    input_clases = pd.read_excel(filepath, sheet_name='Clases', engine='openpyxl')
    input_clases = input_clases[pd.isna(input_clases.id_clase) == False]
    input_clases = input_clases.loc[:, :'horas_'].iloc[:, :-1]

    input_profes = pd.read_excel(filepath, sheet_name='Profesores', engine='openpyxl')
    input_profes = input_profes[pd.isna(input_profes.id_profe) == False]

    input_horas = pd.read_excel(filepath, sheet_name='Horas', engine='openpyxl')

    return input_clases, input_profes, input_horas

def generar_clases_asignaturas_profesores_franjas(clases_df, profes_df, horas_df):

    clases = [col for col in clases_df['id_clase']]
    asignaturas = [col.replace('horas_', '') for col in clases_df.columns[1::2]]
    profesores = [col for col in profes_df['id_profe']]
    franjas = []
    for i, day in enumerate(list(horas_df)):
        for h in range(int(horas_df.iloc[0, i]), int((horas_df.iloc[1, i]))):
            franjas.append(day + " " + str(h) + "-" + str(h+1))

    return clases, asignaturas, profesores, franjas

def generar_HCA_PCA(clases_df, clases, asignaturas, profesores):

    HCA = []
    PCA = []
    for i, clase in enumerate(clases):
        HCA.append([])
        for j, asignatura in enumerate(asignaturas):
            HCA[i].append(clases_df.loc[clases_df['id_clase'] == clase, 'horas_' + asignatura][i])

    for i, clase in enumerate(clases):
        PCA.append([])
        for j, asignatura in enumerate(asignaturas):
            PCA[i].append(profesores.index(clases_df.loc[clases_df['id_clase'] == clase, 'profesor_' + asignatura][i]) + 1)

    return HCA, PCA


def generar_DPF(profes_df, horas_df, franjas, profesores):
    DPF = []

    for i, _ in enumerate(profesores):
        DPF.append([])
        for _ in franjas:
            DPF[i].append(1)

    disponibilidad_df = profes_df.iloc[:, 1:]

    horas_acum = 0
    for j in range(disponibilidad_df.shape[1]):
        horas_j = (horas_df.iloc[1,j] - horas_df.iloc[0,j]) # Horas lectivas en el día j
        for i in range(disponibilidad_df.shape[0]):
            value = disponibilidad_df.iloc[i, j]
            if value != 0:
                DPF[i][horas_acum:horas_acum + horas_j] = [0]*horas_j

        horas_acum += horas_j
    return DPF

def max_dias_libres_clases(horas_dia: list, horas_clase: list):
    '''
    Calcular cuál es el máximo número de días libres que una clase puede tener dado su númro total de horas y el
    horario lectivo
    Devuelve ese número para cada clase
    '''
    horas_dia_ord = sorted(horas_dia, reverse=True)
    max_dias_libres = []
    for i in range(len(horas_clase)): # len(horas_clase) = número de clases
        tot_huecos_semana = sum(horas_dia) - horas_clase[i]
        for i, h in enumerate(horas_dia_ord):
            if tot_huecos_semana < 0:
                break
            tot_huecos_semana -= h
        max_dias_libres.append(i-1)

    return max_dias_libres

def reparto_ideal_huecos_profes(horas_dia: list, horas_profe: list, profes_df):
    '''
    Calcular cuál es el reparto ideal de horas libres cada dia que un profe puede tener si se reparten todas sus horas
    libres lo más uniformemente posible a lo largo de la semana.
    Devuelve una lista con una lista cada profesorm con el reparto ideal ordenado de más horas a menos
    '''
    reparto_ideal_profes = []
    for i in range(len(horas_profe)): # len(horas_profe) = número de profesores
        dias_no_disp = profes_df.iloc[i,1:].tolist()
        horas_no_disp = [x1*x2 for (x1, x2) in zip(dias_no_disp, horas_dia)]
        tot_huecos_semana = sum(horas_dia) - sum(horas_no_disp) - horas_profe[i]
        reparto_ideal = [0]*5
        i = 0
        while tot_huecos_semana > 0:
            if dias_no_disp[i] == 1:
                i += -4 if i == 4 else 1
                continue
            reparto_ideal[i] +=1
            tot_huecos_semana += -1
            i += -4 if i == 4 else 1
        reparto_ideal_profes.append(sorted(reparto_ideal, reverse=True))
    return reparto_ideal_profes

def reparto_ideal_huecos_clases(horas_dia: list, horas_clase: list, max_dias_libres_clase: list):
    '''
    Calcular cuál es el reparto ideal de horas libres que una clase puede tener de acuerdo con las restricciones
    soft de tener el número máximo de días libres y despúes.
    Devuelve una lista con una lista cada profesorm con el reparto ideal ordenado de más horas a menos
    '''
    reparto_ideal_huecos_clases = []
    for i in range(len(horas_clase)): # len(horas_clase) = número de clases
        tot_huecos_semana = sum(horas_dia) - horas_clase[i]
        reparto_ideal = [0]*5
        num_dias_libres_ideal = max_dias_libres_clase[i]
        i = 0
        while tot_huecos_semana > 0:
            if i < num_dias_libres_ideal:
                reparto_ideal[i] = sorted(horas_dia, reverse=True)[i]
                tot_huecos_semana += -1*reparto_ideal[i]
                i += -4 if i == 4 else 1
                continue
            reparto_ideal[i] +=1
            tot_huecos_semana += -1
            i += -4 if i == 4 else 1
        reparto_ideal_huecos_clases.append(sorted(reparto_ideal, reverse=True))
    return reparto_ideal_huecos_clases