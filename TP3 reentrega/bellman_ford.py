INFINITO = float('inf')

def string_ciclo(ciclo):
    c = ""
    for i in ciclo:
        c += i
    cadena_invertida = ""
    for letra in c:
        cadena_invertida = letra + cadena_invertida
    return cadena_invertida

def encontrar_ciclo_negativo(padre, costos, v, w):
    ciclo = [v]
    costo = 0
    while padre[v] != w:
        ciclo.append(padre[v])
        v = padre[v]
    ciclo.append(w)
    ciclo.append(ciclo[0])
    for i in range(len(ciclo)):
        if (i+1) > len(ciclo) - 1:
            ciclo.pop()
            return ciclo, costo
        tramo = ciclo[i] + ciclo[i+1]
        try: 
            costo += costos[tramo]
        except KeyError:
            tramo = ciclo[i+1] + ciclo[i]
            costo += costos[tramo]
    ciclo.pop()
    return ciclo, costo

def camino_minimo(aristas, nodos):
    dist = {}
    padre = {}
    for v in nodos:
        dist[v] = INFINITO
    origen = aristas.get('origen')
    dist[origen] = 0
    padre[origen] = None 
    for i in range(len(nodos)):
        for tramo, peso in aristas.items():
            if tramo != 'origen' and tramo != 'destino': 
                v = tramo[0]
                w = tramo[1]
                if dist[v] + peso["costo"] < dist[w]:
                    padre[w] = v
                    dist[w] = dist[v] + peso["costo"] 
    for tramo, peso in aristas.items():
        if tramo != 'origen' and tramo != 'destino': 
            v = tramo[0]
            w = tramo[1]
            if dist[v] + peso["costo"] < dist[w]:
                ciclo, costo = encontrar_ciclo_negativo(padre, aristas, v, w)
                print("Existe al menos un ciclo negativo en el grafo. {} -> costo: {} ".format(string_ciclo(ciclo), costo))
                return True, ciclo
    return False, None

def bellman_ford(grafo, nodos):
    return camino_minimo(grafo, nodos)
