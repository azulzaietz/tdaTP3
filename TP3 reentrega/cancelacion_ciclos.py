from bellman_ford import * 
from ford_fulkerson import *
from file_reader import *

def min_peso_arista(grafo, grafo_residual, camino):
    capacidad_residual = INFINITO
    arista = ""
    for i in range(1, len(camino)):
        if existe_arista(grafo, camino[i-1], camino[i]):
            if grafo.get((camino[i-1], camino[i]))["flujo"] < capacidad_residual:
                capacidad_residual = grafo.get((camino[i-1], camino[i]))["flujo"]
                arista = (camino[i-1], camino[i])
        else:
            if grafo.get((camino[i], camino[i-1]))["flujo"] < capacidad_residual:
                capacidad_residual = grafo.get((camino[i], camino[i-1]))["flujo"]
                arista = (camino[i-1], camino[i])
    return capacidad_residual, arista

def cancelacion_de_ciclos(fileName):
    grafo, nodos = obtener_aristas(fileName)
    f_max, flujo, grafo_residual = ford_fulkerson(grafo)
    costo = 0
    ciclos_negativos = []
    existe_ciclo_negativo, ciclo = bellman_ford(grafo_residual, nodos, ciclos_negativos)
    while existe_ciclo_negativo:
        capacidad_residual_minima, arista_a_eliminar = min_peso_arista(grafo, grafo_residual, ciclo)
        for i in range(1, len(ciclo)):
            flujo[(ciclo[i], ciclo[i-1])] += capacidad_residual_minima
            flujo[(ciclo[i-1], ciclo[i])] -= capacidad_residual_minima
        del grafo_residual[arista_a_eliminar]
        existe_ciclo_negativo, ciclo = bellman_ford(grafo_residual, nodos, ciclos_negativos)
    
    for arista, valor_flujo in flujo.items():
        if valor_flujo > 0:
            if existe_arista(grafo, arista[1], arista[0]):
                costo += valor_flujo * grafo[(arista[1], arista[0])]["costo"]

    print("Flujo", f_max)
    print("Costo", costo)
    return f_max, costo

cancelacion_de_ciclos(sys.argv[1])