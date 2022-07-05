import sys
import queue
from copy import deepcopy
INFINITO = float('inf')

def _obtener_camino(padre, s, t):
    camino = []
    camino.insert(0, t)
    while(padre[t] != None):
        camino.insert(0, padre[t])
        t = padre[t]
    return camino


def obtener_camino(grafo_residual, s, t):
    visitados = set()
    padres = {}
    orden = {}
    padres[s] = None
    orden[s] = 0
    visitados.add(s)
    q = queue.Queue()
    q.put(s, block=False)
    while not q.empty():
        v = q.get(block=False)
        for w in encontrar_adyacentes(grafo_residual, v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                q.put(w, block=False)
    if t in visitados:
        return _obtener_camino(padres, s, t)
    return None

def min_peso(grafo, camino):
    path_flow = INFINITO
    for i in range(1, len(camino)):
        if grafo.get((camino[i-1], camino[i]))["flujo"] < path_flow:
            path_flow = grafo.get((camino[i-1], camino[i]))["flujo"]
            arista = (camino[i-1], camino[i])
    return path_flow

def encontrar_adyacentes(grafo, vertice):
    adyacentes = []
    for arista, _ in grafo.items():
        if arista[0] == vertice:
            adyacentes.append(arista[1])
    return adyacentes

def existe_arista(grafo, u, v):
    adyacentes = encontrar_adyacentes(grafo, u)
    if v in adyacentes:
        return True
    return False

def actualizar_grafo_residual(grafo_residual, u, v, valor):
    """peso_anterior = grafo_residual[(u, v)]["flujo"]
    costo_anterior = 0
    if peso_anterior == valor:
        costo_anterior = - grafo_residual[(u, v)]["costo"]
        del grafo_residual[(u, v)]
    else:
        grafo_residual[(u, v)]["flujo"] = peso_anterior - valor
    if not existe_arista(grafo_residual, v, u):
        grafo_residual[(v, u)] = {"costo": costo_anterior, "flujo": valor}
    else:
        grafo_residual[(v, u)]["flujo"] = peso_anterior + valor"""
    print((u,v))
    if valor == 0:
        print("elimino", (u,v))
        del grafo_residual[(u, v)]
    else:
        grafo_residual[(u, v)]["flujo"] = valor

def crear_grafo_residual(grafo):
    gr = deepcopy(grafo)
    for arista, valor in grafo.items():
        if arista != 'origen' and arista != 'destino':
            gr[(arista[1], arista[0])] = {"costo": -valor["costo"], "flujo": 0}
    return gr

def flujo(grafo):
    flujo_max = 0
    flujo = {}
    for arista, peso in grafo.items():
        if arista != "origen" and arista != "destino":
            flujo[arista] = peso["flujo"]
            flujo[(arista[1], arista[0])] = 0

    grafo_residual = crear_grafo_residual(grafo)
    camino = obtener_camino(grafo_residual, grafo.get('origen'), grafo.get('destino'))
    while camino is not None:
        capacidad_residual_camino = min_peso(grafo_residual, camino)
        flujo_max += capacidad_residual_camino
        print("camino", camino)
        for i in range(1, len(camino)):
            if camino[i] in encontrar_adyacentes(grafo, camino[i-1]):
                flujo[(camino[i-1], camino[i])] -= capacidad_residual_camino
                flujo[(camino[i], camino[i-1])] += capacidad_residual_camino
                actualizar_grafo_residual(grafo_residual, camino[i-1], camino[i], flujo[(camino[i-1], camino[i])])
                actualizar_grafo_residual(grafo_residual, camino[i], camino[i-1], flujo[(camino[i], camino[i-1])])
        
        camino = obtener_camino(grafo_residual, grafo.get('origen'), grafo.get('destino'))

    return flujo_max, flujo, grafo_residual

def ford_fulkerson(grafo):
    f_max, f, grafo_residual = flujo(grafo)
    return f_max, f, grafo_residual