import pandas as pd
import operator
import random
import numpy as np

from inputs import codificar_inputs
from genotipo import genotipo

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def inicializar_poblacion(inputs, tam_pop):
    poblacion = [genotipo(inputs) for _ in range(tam_pop)]
    return poblacion

def seleccionar_supervivientes(poblacion, tam_pop):
    '''
    Selección de los supervivientes mediante el método de la ruleta
    '''
    poblacion_ordenada = sorted(poblacion, key=operator.attrgetter('fitness'), reverse=False)
    peor_valor_fitness = poblacion_ordenada[len(poblacion_ordenada)-1].fitness + 1
    pesos = [(peor_valor_fitness - i.fitness) for i in poblacion]
    total_valores = sum(pesos)
    pesos = np.array(pesos) / total_valores
    supervivientes = np.random.choice(poblacion, tam_pop, p=pesos, replace=False)
    supervivientes = supervivientes.tolist()
    return supervivientes


def seleccionar_padres(poblacion,tam_pop):
    '''
    Selección de los padres mediante torneo
    '''
    n_padres = int(tam_pop / 5) #Se seleccionarán una quinta parte de la población
    poblacion_desordenada = random.sample(poblacion, tam_pop)

    k = int(tam_pop/n_padres) #número de individuos en cada grupo de torneo
    padres_seleccionados = []
    for t in range(n_padres):
        torneo = poblacion_desordenada[t*k:t*k+k]
        torneo = sorted(torneo, key=operator.attrgetter('fitness'), reverse=False)
        padres_seleccionados.append(torneo[0])

    return padres_seleccionados

def seleccionar_solucion(poblacion):
    poblacion_ordenada = sorted(poblacion, key=operator.attrgetter('fitness'), reverse=False)
    return poblacion_ordenada[0]

def ejecutar_algoritmo(n_iter, tam_pop):
    '''
    Función principal para ejecutar todos los pasos e iteraciones del algoritmo evolutivo. No devuelve ningún objeto.
    :param n_iter: número de iteraciones
    :param tam_pop: tamaño de la población
    '''
    inputs = codificar_inputs()
    poblacion = inicializar_poblacion(inputs, tam_pop)
    for i in range(n_iter):
        padres = seleccionar_padres(poblacion, tam_pop)
        # recombinar_padres()
        # mutar_individuos()
        poblacion = seleccionar_supervivientes(poblacion, tam_pop)
    solucion = seleccionar_solucion(poblacion)
    solucion.plot_genotipo()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #ejecutar_algoritmo(100, 30)

    ejecutar_algoritmo(100, 10)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
