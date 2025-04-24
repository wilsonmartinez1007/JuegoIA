
from collections import deque
import heapq


matrizPos = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,"P",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,"G",1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,1,1,1,0,1,1,0,0,0,0,0,1,1,1,1,1,0,1],
    [1,"Q",1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

n = len(matrizPos)
m = len(matrizPos[0])
mCostos =[[0 for _ in range(m)] for _ in range(n)]
def crearCosto():
    for filas in range(n):
        for columnas in range(m):
            if matrizPos[filas][columnas] == 1:
                mCostos[filas][columnas] = "inf"
            elif matrizPos[filas][columnas] == "G":
                mCostos[filas][columnas] = 100

            elif matrizPos[filas][columnas] == "P":
                mCostos[filas][columnas] = 1
                xA, yA = filas, columnas 
            else:
                mCostos[filas][columnas] = 1

    


def encontrar_caminoAmplitud(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    inicio = None
    objetivos = []  # ← Aquí vamos a guardar todas las "Q"

    # Buscar posición de "R" y todos los "Q"
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == "P":
                inicio = (i, j)
            elif matriz[i][j] == "Q":
                objetivos.append((i, j))

    if not inicio or not objetivos:
        return None  # No hay inicio o fin

    # BFS
    cola = deque()
    visitado = set()
    padres = {}

    cola.append(inicio)
    visitado.add(inicio)

    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    objetivo_encontrado = None

    while cola:
        actual = cola.popleft()#sacamos el primero en ingresar

        if actual in objetivos:
            objetivo_encontrado = actual
            break

        for dx, dy in direcciones:
            nx, ny = actual[0] + dx, actual[1] + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if matriz[nx][ny] not in [1] and (nx, ny) not in visitado:
                    cola.append((nx, ny))
                    visitado.add((nx, ny))
                    padres[(nx, ny)] = actual

    # Si no encontró ningún "Q"
    if not objetivo_encontrado:
        return None

    # Reconstruir camino
    camino = []
    nodo = objetivo_encontrado
    while nodo != inicio:
        camino.append(nodo)
        nodo = padres.get(nodo)
        if nodo is None:
            return None
    camino.append(inicio)
    camino.reverse()
    return camino
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_camino_astar(matriz, matriz_costos):
    filas = len(matriz)
    columnas = len(matriz[0])
    inicio = None
    fin = None

    # Buscar inicio y fin
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == "P":
                inicio = (i, j)
            elif matriz[i][j] == "Q":
                fin = (i, j)

    if not inicio or not fin:
        return None

    abiertos = []
    heapq.heappush(abiertos, (0, inicio))  # (f(n), coordenada)
    
    padres = {}
    g = {inicio: 0}  # Costo real desde el inicio
    visitados = set()

    direcciones = [(0,1), (1,0), (0,-1), (-1,0)]

    while abiertos:
        _, actual = heapq.heappop(abiertos)

        if actual == fin:
            break

        if actual in visitados:
            continue
        visitados.add(actual)

        for dx, dy in direcciones:
            nx, ny = actual[0] + dx, actual[1] + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if matriz[nx][ny] not in [1]:
                    nuevo_g = g[actual] + matriz_costos[nx][ny]
                    if (nx, ny) not in g or nuevo_g < g[(nx, ny)]:
                        g[(nx, ny)] = nuevo_g
                        f = nuevo_g + heuristica((nx, ny), fin)
                        heapq.heappush(abiertos, (f, (nx, ny)))
                        padres[(nx, ny)] = actual

    # Reconstrucción del camino
    if fin not in padres:
        return None

    camino = []
    nodo = fin
    while nodo != inicio:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.append(inicio)
    camino.reverse()
    return camino
def encontrar_camino_Profundidad(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    inicio = None
    objetivos = []

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == "P":
                inicio = (i, j)
            elif matriz[i][j] == "Q":
                objetivos.append((i, j))

    if not inicio or not objetivos:
        return None, None

    pila = [(inicio, [inicio])]
    visitado = set()

    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pila:
        actual, camino = pila.pop()
        if actual in visitado:
            continue
        visitado.add(actual)

        if actual in objetivos:
            return camino, None  # Camino completo, sin atasco

        caminos_nuevos = 0
        for dx, dy in direcciones:
            nx, ny = actual[0] + dx, actual[1] + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if matriz[nx][ny] in [0, "G", "Q"] and (nx, ny) not in visitado:
                    pila.append(((nx, ny), camino + [(nx, ny)]))
                    caminos_nuevos += 1

        # Si no hubo caminos nuevos desde aquí, es un "atasco"
        if caminos_nuevos == 0:
            return camino, actual  # Devuelve el camino hasta donde pudo y dónde se atascó

    return None, None

def continuar_con_otra_busqueda(matriz, matriz_costos):
    crearCosto()
    camino_parcial, nodo_atascado = encontrar_camino_Profundidad(matriz)

    if not camino_parcial:
        return encontrar_camino_astar(matriz, matriz_costos)

    if nodo_atascado is None:
        return camino_parcial  # DFS llegó a la meta

    # Cambiar temporalmente el punto de inicio a donde se atascó
    matriz_temp = [fila[:] for fila in matriz]
    for i in range(len(matriz_temp)):
        for j in range(len(matriz_temp[0])):
            if matriz_temp[i][j] == "P":
                matriz_temp[i][j] = 0  # quitar el inicio viejo
    matriz_temp[nodo_atascado[0]][nodo_atascado[1]] = "P"

    camino_extra = encontrar_camino_astar(matriz_temp, matriz_costos)

    if not camino_extra:
        return camino_parcial  # No pudo continuar, devuelvo lo que tengo

    # Eliminar el nodo_atascado repetido del segundo camino
    if camino_extra and camino_extra[0] == nodo_atascado:
        camino_extra = camino_extra[1:]

    camino_completo = camino_parcial + camino_extra
    return camino_completo


if __name__=="__main__":
    crearCosto()
    camino = encontrar_caminoAmplitud(matrizPos)
    print("Camino encontrado amplitud:")
    print(camino)
    camino2 = encontrar_camino_Profundidad(matrizPos)
    print("Camino encontrado profundidad:")
    print(camino2)
    camino3 = encontrar_camino_astar(matrizPos, mCostos)
    print("Camino encontrado A*:")
    print(camino3)
    print("-------------------")
    camino4 = continuar_con_otra_busqueda(matrizPos, mCostos)
    print(camino4)

