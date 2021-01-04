import random

class genotipo():

    def __init__(self, inputs: dict):

        self.inputs = inputs
        self.cod = self.generar_genotipo()
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
        HCA_disp = self.inputs['HCA'] # Se usa para ir restando horas a medida que se asignan
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
        '''
        Calcular fitness del genotipo
        :return:
        '''
        # TODO: completar
        pass



def mutar_genotipo(genotipo_a_mutar: genotipo):
    genotipo_mutado = genotipo_a_mutar
    # TODO: completar
    return genotipo_mutado

def combinar_genotipo(padre1: genotipo, padre2: genotipo):
    hijo = padre1 + padre2
    # TODO: completar
    return hijo