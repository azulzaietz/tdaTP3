def obtener_aristas(fileName):
    f = open(fileName, 'r')
    tramos = f.readlines()
    f.close()
    grafo = {}
    nodos = []
    origen = True
    for t in tramos:
        data = t.split()[0].split(',')
        if data[0] not in nodos:
            nodos.append(data[0])
        if len(data) == 1 and origen:
            grafo['origen'] = data[0]
            origen = False
        elif len(data) == 1:
            grafo['destino'] = data[0]
        elif len(data) == 4:
            grafo[(data[0], data[1])] = {"costo": int(data[2]), "flujo": int(data[3])}
            if data[1] not in nodos:
                nodos.append(data[1])
    return grafo, nodos
    