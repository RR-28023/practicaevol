import random
import copy
import matplotlib.pyplot as plt
import numpy as np

class genotipo():

    def __init__(self, inputs: dict):

        self.inputs = inputs
        self.cod = self.generar_genotipo()
        #self.plot_genotipo()
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

    def calcular_fitness(self):
        dias = ['L', 'M', 'X', 'J', 'V']
        contador_hard = 0
        contador_soft = 0

        for i, clase in enumerate(self.inputs['clases']):
            for j, franja in enumerate(self.inputs['franjas']):
                asign = self.cod[i][j] -1
                if asign != -1:
                    # restriccion hard 1
                    profesor_asign = self.inputs['PCA'][i][asign]
                    if self.inputs['DPF'][profesor_asign - 1][j] == 0:
                        contador_hard += 1

                    # restriccion hard 3
                    profesores_otras_clases = []
                    for c, clase in enumerate(self.inputs['clases']):
                        if c != i and self.cod[c][j] != 0:
                            profesores_otras_clases.append(self.inputs['PCA'][c][self.cod[c][j]-1])
                    if profesor_asign in profesores_otras_clases:
                        contador_hard += 1

            for ndia in range(len(dias)):
                horas_en_dia = sum(dias[ndia] in f for f in self.inputs['franjas'])
                clases_dia = self.cod[i][ndia*6:(ndia*6)+horas_en_dia]
                if 0 in clases_dia[1:-1]: contador_hard += 1  # restriccion hard 6
                if len(clases_dia) != len(set(clases_dia)):  contador_soft += 1 # restriccion soft 5

        peso_rhard = 10
        peso_rsoft = 1
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
            ax.set_ylim(14.1, 7.9)
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

            plt.title(clase_label)#, y=1.15)

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


    return hijo1, hijo2