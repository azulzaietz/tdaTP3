from bellman_ford import * 
from ford_fulkerson import *
from file_reader import *

"""BEGIN
  (* Initialize to max flow *)
  f = CALCULATE MAX FLOW()
  (* Main Loop *)
  WHILE negative cycle might exist DO
    CONSTRUCT RESIDUAL GRAPH G'(V,E') WITH CAPACITIES u'(e) 
    EXECUTE BELLMAN-FORD ON G' FROM TARGET NODE
    IF negative cycle exists
      IDENTIFY cycle-edges 
      adjustment ← min(u'(e) | e ∈ cycle-edges )
      FOR e ∈ cycle-edges 
        f(e) += adjustment 
END"""

def min_peso_arista(grafo, grafo_residual, camino):
    capacidad_residual = INFINITO
    arista = ""
    print("---------- EN MIN PATH FLOW ---------")
    print(grafo)
    print(camino)
    for i in range(1, len(camino)):
        if existe_arista(grafo, camino[i-1], camino[i]):
            if grafo.get((camino[i-1], camino[i]))["flujo"] < capacidad_residual:
                print("min flow: ", (camino[i-1], camino[i]), grafo.get((camino[i-1], camino[i]))["flujo"])
                capacidad_residual = grafo.get((camino[i-1], camino[i]))["flujo"]
                arista = (camino[i-1], camino[i])
        else:
            if grafo.get((camino[i], camino[i-1]))["flujo"] < capacidad_residual:
                print("min flow: ", (camino[i], camino[i-1]), grafo.get((camino[i], camino[i-1]))["flujo"])
                capacidad_residual = grafo.get((camino[i], camino[i-1]))["flujo"]
                arista = (camino[i-1], camino[i])
    print("---------- EN MIN PATH FLOW ---------")
    return capacidad_residual, arista

def cancelacion_de_ciclos(fileName):
    grafo, nodos = obtener_aristas(fileName)
    f_max, flujo, grafo_residual = ford_fulkerson(grafo)
    costo = 0
    ciclos_negativos = []
    print(grafo_residual)
    print("------- FLUJO {} ---------".format(flujo))
    existe_ciclo_negativo, ciclo = bellman_ford(grafo_residual, nodos, ciclos_negativos)
    while existe_ciclo_negativo:
        print("flujo antes minpf", flujo)
        capacidad_residual_minima, arista_a_eliminar = min_peso_arista(grafo, grafo_residual, ciclo)
        for i in range(1, len(ciclo)):
            #if arista_a_eliminar != (ciclo[i-1], ciclo[i]) and ciclo[i] in encontrar_adyacentes(grafo_residual, ciclo[i-1]):
                flujo[(ciclo[i], ciclo[i-1])] += capacidad_residual_minima
                flujo[(ciclo[i-1], ciclo[i])] -= capacidad_residual_minima
            #else:
                #flujo[(ciclo[i], ciclo[i-1])] += capacidad_residual_minima
            #if arista_a_eliminar != (ciclo[0], ciclo[len(ciclo) - 1]) and ciclo[len(ciclo) - 1] in encontrar_adyacentes(grafo_residual, ciclo[0]):
                #flujo[(ciclo[0], ciclo[len(ciclo) - 1])] += capacidad_residual_minima
                #print("sumo {} a arista {}".format(capacidad_residual_minima, (ciclo[i-1], ciclo[i])))
        print("elimino arista", arista_a_eliminar)
        del grafo_residual[arista_a_eliminar]
        #flujo[arista_a_eliminar] = 0
        print("flujo desp minpf", flujo)
        existe_ciclo_negativo, ciclo = bellman_ford(grafo_residual, nodos, ciclos_negativos)
    
    print(flujo)
    print(grafo)
    for arista, valor_flujo in flujo.items():
        if valor_flujo > 0:
            if existe_arista(grafo, arista[1], arista[0]):
                costo += valor_flujo * grafo[(arista[1], arista[0])]["costo"]

    print("Flujo", f_max)
    print("Costo", costo)
    return f_max, costo

cancelacion_de_ciclos(sys.argv[1])