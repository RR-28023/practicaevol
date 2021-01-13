import random
import copy
import matplotlib.pyplot as plt
import numpy as np

class genotipo():

    def __init__(self, inputs: dict):

        self.inputs = inputs
        self.cod = self.generar_genotipo()
        self.apf = self.generar_horario_profesores() # Matriz AsignaturaProfesorFranja
        self.fitness = self.calcular_fitness()

    def generar_genotipo(self):
        '''
        Función que inicializa el genotipo definiendo la matriz genotipo.cod (m x t),
        donde el elemento ij representa la asignatura asignada a la clase i en la franja j.
        :return:
        '''
        n_clases = len(self.inputs['clases']) # numero clases
        n_franjas = len(self.inputs['franjas']) # numero horas lectivas
        cod = [[0]*n_franjas for _ in range(n_clases)] # Inicializamos matriz del genotipo
        f_disp_clases = [[i for i in range(n_franjas)] for _ in range(n_clases)] # Franjas que quedan sin asignar a cada clase
        HCA_disp = copy.deepcopy(self.inputs['HCA']) # Se usa para ir restando horas a medida que se asignan
        h_pend_clases = [sum(horas) for horas in HCA_disp]
        while sum(h_pend_clases) > 0:
            for clase in range(n_clases):
                for asign in range(len(self.inputs['asignaturas'])):
                    if HCA_disp[clase][asign] != 0:
                        franja = random.choice(f_disp_clases[clase]) # Se escoge franja random entre las que quedan sin asignar
                        cod[clase][franja] = asign + 1 # Se asigna la asignatura a esa franja
                        f_disp_clases[clase].remove(franja)
                        HCA_disp[clase][asign] += -1
            h_pend_clases = [sum(horas) for horas in HCA_disp] # Horas que quedan por asignar a cada clase
        return cod

    def generar_horario_profesores(self):
        '''
        Genera la matriz AsignaturaProfesorFranja, en la que el elemento ij representa la asignatura asignada al
        profesor i en la franja j. Si no hay asignatura asignada, ij valdrá 0. Si hay más de una asignatura asignada, ij
        valdrá -1. Esta matriz no añade información adicional y se deduce enteramente de self.cod, pero se crea por
        conveniencia para simplificar ciertos cálculos.
        :return:
        '''
        n_franjas = len(self.inputs['franjas'])
        apf = [[0]*n_franjas for _ in self.inputs['profesores']]
        for clase, franjas in enumerate(self.cod):
            for franja, asignatura in enumerate(franjas):
                profe = self.inputs['PCA'][clase][asignatura - 1]
                apf[profe - 1][franja] = asignatura if apf[profe - 1][franja] == 0 else -1

        return apf



    def calcular_fitness(self, display=False):

        self.apr = self.generar_horario_profesores() # Necesario si el genotipo se ha copiado en lugar de inicializarse.

        dias = ['L', 'M', 'X', 'J', 'V']
        contador_hard = np.zeros(3)
        contador_soft = np.zeros(5)

        for i, clase in enumerate(self.inputs['clases']):
            for j, franja in enumerate(self.inputs['franjas']):
                asign = self.cod[i][j] -1
                if asign != -1:
                    # restriccion hard 1 (disp. profesor)
                    profesor_asign = self.inputs['PCA'][i][asign]
                    if self.inputs['DPF'][profesor_asign - 1][j] == 0:
                        contador_hard[0] += 1

                    # restriccion hard 3 (dos asignaturas a la vez mismo profesor)
                    profesores_otras_clases = []
                    for c, _ in enumerate(self.inputs['clases']):
                        if c != i and self.cod[c][j] != 0:
                            profesores_otras_clases.append(self.inputs['PCA'][c][self.cod[c][j]-1])
                    if profesor_asign in profesores_otras_clases:
                        contador_hard[1] += 1

            horas_acum = 0
            for ndia in range(len(dias)):
                horas_en_dia = sum(dias[ndia] in f for f in self.inputs['franjas'])
                asig_dia = self.cod[i][horas_acum:horas_acum+horas_en_dia]

                # restriccion hard 6 (huecos entre medias para las clases)
                i_primera_asign = next((i for i, asig in enumerate(asig_dia) if asig != 0),0)
                i_ultima_asign = next((i for i, asig in reversed(list(enumerate(asig_dia))) if asig != 0),len(asig_dia))
                huecos = asig_dia[i_primera_asign:i_ultima_asign + 1].count(0)
                contador_hard[2] += 1*huecos

                # restriccion soft 5 (misma asignatura en el día) - Penaliza más si hay más asignaturas repes
                n_repeticiones = len(asig_dia) - len(set(asig_dia) -{0}) - asig_dia.count(0)
                if n_repeticiones != 0:
                    contador_soft[4] += 1*n_repeticiones

                # restriccion soft 1 (huecos entre medias para los profes)
                asig_dia_profe = self.apf[i][horas_acum:horas_acum + horas_en_dia]
                i_primera_asign_profe = next((i for i, asig in enumerate(asig_dia_profe) if asig != 0), 0)
                i_ultima_asign_profe = next((i for i, asig in reversed(list(enumerate(asig_dia_profe))) if asig != 0),
                                        len(asig_dia))
                huecos = asig_dia_profe[i_primera_asign_profe:i_ultima_asign_profe + 1].count(0)
                #contador_soft[0] += 1 * huecos

                horas_acum += horas_en_dia



        if display == True:
            print("Solución - Restricción hard ", 1, ":", contador_hard[0])
            print("Solución - Restricción hard ", 3, ":", contador_hard[1])
            print("Solución - Restricción hard ", 6, ":", contador_hard[2])
            for i, r in enumerate(contador_soft):
                print("Solución - Restricción soft", i+1, ":", r)

        peso_rhard = 10
        peso_rsoft = 1
        contador_hard = int(np.sum(contador_hard))
        contador_soft = int(np.sum(contador_soft))

        fitness = peso_rhard*contador_hard + peso_rsoft*contador_soft
        return fitness

    def plot_genotipo(self):
        dias = ['L', 'M', 'X', 'J', 'V']
        n_clases = len(self.inputs['clases'])
        fig = plt.figure(figsize=(25, 13))
        colors = plt.cm.tab20.colors

        for c in range(1,n_clases + 1):
            ax = fig.add_subplot(round(n_clases/2.0), round(n_clases/2.0), c)
            ax.yaxis.grid()
            ax.set_xlim(0.5, len(dias) + 0.5)
            horas_dia = []
            for ndia in range(len(dias)):
                horas_dia.append(sum(dias[ndia] in f for f in self.inputs['franjas']))
            max_horas_dia = max(horas_dia)
            ax.set_ylim(7.9+max_horas_dia+0.2, 7.9)
            ax.set_xticks(range(1, len(dias) + 1))
            ax.set_xticklabels(dias)
            ax.set_ylabel('Hora')
            clase_label = self.inputs['clases'][c - 1]
            horas_acum = 0
            for ndia in range(len(dias)):
                horas_en_dia = sum(dias[ndia] in f for f in self.inputs['franjas'])
                asignaturas_en_dia = self.cod[c - 1][horas_acum:horas_en_dia + horas_acum]
                for franja, asign in enumerate(asignaturas_en_dia):
                    if asign != 0:
                        ax.fill_between([ndia + 0.5, ndia + 1.46], [franja + 8, franja + 8], [franja + 9, franja + 9],
                                         color=colors[asign], edgecolor='k',linewidth=0.5)
                        asign_label = self.inputs['asignaturas'][asign - 1]
                        ax.text(ndia + 1.00, franja + 8.5, asign_label, ha='center', va='center', fontsize=12)

                horas_acum += horas_en_dia

            plt.title(clase_label)

        fig.show()

def mutar_genotipo(genotipo_a_mutar: genotipo):
    n, m = np.shape(genotipo_a_mutar.cod)
    posn = random.randint(0, n-1)
    pos1m = random.randint(0, m-1)
    pos2m = random.randint(0, m-1)
    genotipo_mutado = copy.deepcopy(genotipo_a_mutar)
    value = genotipo_mutado.cod[posn][pos1m]
    genotipo_mutado.cod[posn][pos1m] = genotipo_mutado.cod[posn][pos2m]
    genotipo_mutado.cod[posn][pos2m] = value
    genotipo_mutado.fitness = genotipo_mutado.calcular_fitness()
    return genotipo_mutado

def recombinar_genotipos(padre1: genotipo, padre2: genotipo):
    n_clases = len(padre1.cod)
    clases_idx = [i for i in range(n_clases)]
    mitad = int(n_clases/2)
    clases_a_cambiar_idx = random.sample(clases_idx, mitad)
    hijo1, hijo2 = copy.deepcopy(padre1), copy.deepcopy(padre2)

    for clase in clases_a_cambiar_idx:
        hijo1.cod[clase] = padre2.cod[clase]
        hijo2.cod[clase] = padre1.cod[clase]

    hijo1.fitness = hijo1.calcular_fitness()
    hijo2.fitness = hijo2.calcular_fitness()

    """
    #Otra posible propuesta de recombinación
    n_clases = len(padre1.cod)
    mitad = int(n_clases / 2)
    hijo1, hijo2 = copy.deepcopy(padre1), copy.deepcopy(padre2)

    for clase in range(mitad, n_clases):
        hijo1.cod[clase] = padre2.cod[clase]
        hijo2.cod[clase] = padre1.cod[clase]

    hijo1.fitness = hijo1.calcular_fitness()
    hijo2.fitness = hijo2.calcular_fitness()
    """
    return hijo1, hijo2