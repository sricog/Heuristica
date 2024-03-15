import numpy as np
import random
from openpyxl import Workbook

def leer_archivo(file_path):
    # Abre el archivo en modo lectura
    with open(file_path, 'r') as file:
        # Lee la primera línea y extrae los valores
        n = int(file.readline())
        m = int(file.readline())
        L = float(file.readline())

        # Inicializa listas para almacenar las coordenadas x, y y el peso (score)
        nodos = dict() 

        # Lee las siguientes n líneas y las mete al diccionario de los nodos
        for i in range(n):
            x, y, p = map(float, file.readline().split())
            nodos[i] = ((x, y, p))
    no_visitados = [x for x in nodos.keys() if x not in [0,n-1]]
    
    return nodos, no_visitados, n, m, L

def agregar_datos(wb,ws,resultados,z,t,metodo):
    for equipo in range(len(resultados)):
        
        ruta = resultados[equipo][0]
        num_nodos = len(ruta)
        distancia_recorrida = resultados[equipo][1]
        valor_funcion = resultados[equipo][2]
        
        # Escribimos los datos del equipo en la fila correspondiente
        fila = [num_nodos] + ruta + [round(distancia_recorrida,3), valor_funcion]
        ws.append(fila)

    # Escribimos los datos finales en la última fila
    ws.append([z,t])

    # Guardamos el libro de trabajo en un archivo
    wb.save(f"Final/TOP_SAMUELRICO_{metodo}.xlsx")


def distancia(nodo1,nodo2,nodos):
    return np.sqrt((nodos[nodo1][0]-nodos[nodo2][0])**2+(nodos[nodo1][1]-nodos[nodo2][1])**2)

def nueva_distancia(equipo, nuevo_nodo, pos, nodos):
    return equipo[1] - distancia(equipo[0][pos-1],equipo[0][pos],nodos) + distancia(equipo[0][pos-1],nuevo_nodo,nodos) + distancia(nuevo_nodo,equipo[0][pos],nodos)

def crear_ruido(nodos,r):
    ruido = nodos.copy()
    for i in range(len(ruido)):
        ruido[i] = list(ruido[i])
        ruido[i][2] += random.randint(0,r)
    return ruido