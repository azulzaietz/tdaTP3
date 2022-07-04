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

def min_peso_arista(grafo, camino):
    path_flow = INFINITO
    arista = ""
    for i in range(1, len(camino)):
        if grafo.get((camino[i-1], camino[i]))["flujo"] < path_flow:
            path_flow = grafo.get((camino[i-1], camino[i]))["flujo"]
            arista = (camino[i-1], camino[i])
    return path_flow, arista

def cancelacion_de_ciclos(fileName):
    grafo, nodos = obtener_aristas(fileName)
    f_max, flujo, grafo_residual = ford_fulkerson(grafo)
    costo = 0
    ciclos_negativos = []
    print(grafo_residual)
    existe_ciclo_negativo, ciclo = bellman_ford(grafo_residual, nodos, ciclos_negativos)
    while existe_ciclo_negativo:
        capacidad_residual_minima, arista_a_eliminar = min_peso_arista(grafo_residual, ciclo)
        for i in range(1, len(ciclo)):
            if arista_a_eliminar != (ciclo[i-1], ciclo[i]) and ciclo[i] in encontrar_adyacentes(grafo_residual, ciclo[i-1]):
                flujo[(ciclo[i-1], ciclo[i])] += capacidad_residual_minima
            #if arista_a_eliminar != (ciclo[0], ciclo[len(ciclo) - 1]) and ciclo[len(ciclo) - 1] in encontrar_adyacentes(grafo_residual, ciclo[0]):
                #flujo[(ciclo[0], ciclo[len(ciclo) - 1])] += capacidad_residual_minima
                #print("sumo {} a arista {}".format(capacidad_residual_minima, (ciclo[i-1], ciclo[i])))
        print("elimino arista", arista_a_eliminar)
        del grafo_residual[arista_a_eliminar]
        flujo[arista_a_eliminar] = 0
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