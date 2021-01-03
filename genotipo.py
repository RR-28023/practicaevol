import random

class genotipo():

    def __init__(self, inputs: dict):

        self.inputs = inputs
        self.cod = self.generar_codificacion_genotipo()
        self.fitness = self.calcular_fitness()

    def generar_codificacion_genotipo(self):
        '''
        Función que inicializa el genotipo definiendo la matriz genotipo.cod (m x t),
        donde el elemento ij representa la asignatura asignada a la clase i en la franja j.
        :return:
        '''
        cod = []
        h_disp_profes =  [sum(horas) for horas in self.inputs['DPF']] # Horas que le quedan disponibles a cada profesor
        x = self.inputs
        for clase in range(len(self.inputs['franjas'])):
            for franja in range(len(self.inputs['franjas'])):
                profe = random.randint(1,9) # se escoge profesor aleatoriamente
                #cod[clase][franja] = asign
        #TODO: completar
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