import pandas as pd

from inputs import codificar_inputs
from genotipo import genotipo

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def inicializar_poblacion(inputs, tam_pop):
    poblacion = [genotipo(inputs) for _ in range(tam_pop)]
    return poblacion



def ejecutar_algoritmo(n_iter, tam_pop):
    '''
    Función principal para ejecutar todos los pasos e iteraciones del algoritmo evolutivo. No devuelve ningún objeto.
    :param n_iter: número de iteraciones
    :param tam_pop: tamaño de la población
    '''
    inputs = codificar_inputs()
    poblacion = inicializar_poblacion(inputs, tam_pop)
    #for i in range(n_iter + 1):
    #    for ind in range(tam_pop + 1):
    #        calcular_fit() # Calculamos el valor de fitness para cada individuo
    #
    #    seleccionar_padres()
    #    recombinar_mutar()
    #    seleccionar_supervivientes()
    #
    #seleccionar_solución()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #ejecutar_algoritmo(100, 30)

    ejecutar_algoritmo(100, 30)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
