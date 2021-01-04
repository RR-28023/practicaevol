import pandas as pd


def codificar_inputs():
    inputs_codificados = {}
    clases_df, profes_df, horas_df = extraer_inputs()
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


    return inputs_codificados

def extraer_inputs(filepath='.\\datos\\Generador inputs horarios.xlsx'):
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
            PCA[i].append(profesores.index(clases_df.loc[clases_df['id_clase'] == clase, 'profesor_' + asignatura][i]))

    return HCA, PCA


def generar_DPF(profes_df, horas_df, franjas, profesores):
    DPF = []

    for i, profesor in enumerate(profesores):
        DPF.append([])
        for j, franja in enumerate(franjas):
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
#
# def extraer_tuplas_profe_asignatura(clases_df):
#
#     asignaturas = [col.replace('horas_','') for col in clases_df.columns[1::2]]
#     tuplas = set()
#     for asignatura in asignaturas:
#         for profe in clases_df['profesor_' + asignatura].unique():
#             tuplas.add((asignatura,profe))
#
#     return tuplas