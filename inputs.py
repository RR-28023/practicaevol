import pandas as pd


def codificar_inputs():
    clases_df, profes_df, horas_df = extraer_inputs()
    clases, asignaturas, profesores = generar_clases_asignaturas_profesores(clases_df, profes_df)
    HCA, PCA = generar_HCA_PCA(clases_df, clases, asignaturas)


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

def generar_clases_asignaturas_profesores(clases_df, profes_df):

    clases = [col for col in clases_df['id_clase']]
    asignaturas = [col.replace('horas_', '') for col in clases_df.columns[1::2]]
    profesores = [col for col in profes_df['id_profe']]

    return clases, asignaturas, profesores

def generar_HCA_PCA(clases_df, clases, asignaturas):

    HCA = []
    PCA = []
    for i, clase in enumerate(clases):
        HCA.append([])
        for j, asignatura in enumerate(asignaturas):
            HCA[i].append(clases_df.loc[clases_df['id_clase'] == clase, 'horas_' + asignatura][i])

    #TODO: Falta generar la mariz PCA

    return HCA, PCA
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