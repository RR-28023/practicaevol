import operator
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from inputs import codificar_inputs
from genotipo import genotipo, mutar_genotipo, recombinar_genotipos

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
    pesos = (np.array(pesos) / total_valores)
    supervivientes = np.random.choice(poblacion, tam_pop, p=pesos, replace=False)
    supervivientes = supervivientes.tolist()
    fitness_mejor_superviviente = sorted(supervivientes, key=operator.attrgetter('fitness'), reverse=False)[0].fitness
    return supervivientes, fitness_mejor_superviviente

def seleccionar_padres(poblacion,tam_pop, num_padres):
    '''
    Selección de los padres mediante el método del torneo
    '''
    poblacion_desordenada = random.sample(poblacion, tam_pop)

    k = int(tam_pop/num_padres) #número de individuos en cada grupo de torneo
    padres_seleccionados = []
    for t in range(num_padres):
        torneo = poblacion_desordenada[t*k:t*k+k]
        torneo = sorted(torneo, key=operator.attrgetter('fitness'), reverse=False)
        padres_seleccionados.append(torneo[0])

    return padres_seleccionados

def recombinar_padres(poblacion, padres):
    nueva_poblacion = poblacion
    n_padres = len(padres)
    padres_shuffled = random.sample(padres, n_padres)
    mitad = int(n_padres/2)
    for padre1, padre2 in zip(padres_shuffled[0:mitad],padres_shuffled[mitad:n_padres]):
        nueva_poblacion.extend((recombinar_genotipos(padre1, padre2)))
    return nueva_poblacion

def mutar_individuos(poblacion, padres):
    nueva_poblacion = poblacion
    for padre in padres:
        nueva_poblacion.append(mutar_genotipo(padre))
    return nueva_poblacion

def seleccionar_solucion(poblacion):
    poblacion_ordenada = sorted(poblacion, key=operator.attrgetter('fitness'), reverse=False)
    return poblacion_ordenada[0]

def plot_fitness_iteraciones(valores_mejor_fitness):

    x = [i + 1 for i in range(len(valores_mejor_fitness))]
    ax = sns.lineplot(x=x, y=valores_mejor_fitness)
    ax.set(xlabel='Iteración', ylabel='Fitness')
    ax.text(x=x[-1] - len(x)*0.02, y= valores_mejor_fitness[-1] + 5,
            s= valores_mejor_fitness[-1], color = 'black')
    plt.show()

def ejecutar_algoritmo(n_iter, tam_pop, seed):
    '''
    Función principal para ejecutar todos los pasos e iteraciones del algoritmo evolutivo. No devuelve ningún objeto.
    :param n_iter: número de iteraciones
    :param tam_pop: tamaño de la población
    '''
    random.seed(seed)
    np.random.seed(seed)
    num_padres = int(tam_pop / 5) #Se seleccionarán una quinta parte de la población
    inputs = codificar_inputs()
    poblacion = inicializar_poblacion(inputs, tam_pop)
    mejores_fit = []
    for i in range(n_iter):
        if i == 0 and True: # Para ver visualmente como mejora (desactivado ahora)
            mejor_individuo_inicial = seleccionar_solucion(poblacion)
            mejor_individuo_inicial.plot_genotipo()
            mejor_individuo_inicial.plot_horario_profesores()

        padres = seleccionar_padres(poblacion, tam_pop, num_padres)
        poblacion =  recombinar_padres(poblacion, padres)
        poblacion = mutar_individuos(poblacion, padres)
        poblacion, fit_mejor_sup = seleccionar_supervivientes(poblacion, tam_pop)
        print("Fitness mejor superviviente en iteración {0}: {1}".format(i + 1,fit_mejor_sup))
        mejores_fit.append(fit_mejor_sup)
        if fit_mejor_sup == 0:
            display=False
            break
        display = True
    solucion = seleccionar_solucion(poblacion)
    plot_fitness_iteraciones(mejores_fit)
    solucion.plot_genotipo()
    solucion.plot_horario_profesores()
    solucion.calcular_fitness(display=display)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #ejecutar_algoritmo(100, 30)

    ejecutar_algoritmo(n_iter=400, tam_pop=100, seed=33)
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
