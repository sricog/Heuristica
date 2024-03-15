import time
from auxiliares import leer_archivo, distancia, nueva_distancia,crear_ruido
import heapq
import random
import numpy as np
from openpyxl import Workbook

def constructivo(file_path):
    nodos, no_visitados, n, m, L = leer_archivo(file_path)
    inicio = time.time()
    z = 0
    equipos = {} #diccionario donde se accede a la ruta y longitud de cada equipo
    for equipo in range(m):
        equipos[equipo] = [[0,n-1],(distancia(0,n-1,nodos)),0]
    flag = True
    while flag:
        flag = 0
        ratio = 0
        mejor = (0,0,0,0,0) #nodo, pos, distancia, equipo, valor
        for equipo in range(m): #Para cada equipo
            for nodo in no_visitados: #Para cada nodo
                for pos in range(1,(len(equipos[equipo][0]))):
                    nuevo_l = nueva_distancia(equipos[equipo],nodo,pos,nodos)
                    if nuevo_l > L: continue
                    ratio_temp = nodos[nodo][2]/(nuevo_l-equipos[equipo][1])
                    if ratio_temp >= ratio:
                        ratio = ratio_temp
                        mejor = (nodo,pos,nuevo_l,equipo,nodos[nodo][2])
                        flag = 1
        if flag:
            equipos[mejor[3]][0].insert(mejor[1],mejor[0])
            equipos[mejor[3]][1] = mejor[2]
            no_visitados.remove(mejor[0])
            z += mejor[4]
            equipos[mejor[3]][2] += mejor[4]
            
    fin = time.time()
    
    return equipos,z,int(round((fin-inicio)*1000,0))

def grasp(file_path,k,nsol):
    mejor = np.zeros(3)
    inicio = time.time()
    for i in range(nsol):
        z = 0
        equipos = {} #diccionario donde se accede a la ruta y longitud de cada equipo
        nodos, no_visitados, n, m, L = leer_archivo(file_path)
        for equipo in range(m):
            equipos[equipo] = [[0,n-1],(distancia(0,n-1,nodos)),0]
        flag = True
        while flag:
            mejores = []
            for i in range(k):
                heapq.heappush(mejores, (0, ""))
            flag = 0
            ratio = 0
            t=0
            for equipo in range(m): #Para cada equipo
                for nodo in no_visitados: #Para cada nodo
                    for pos in range(1,(len(equipos[equipo][0]))):
                        nuevo_l = nueva_distancia(equipos[equipo],nodo,pos,nodos)
                        if nuevo_l > L: continue
                        ratio_temp = nodos[nodo][2]/(nuevo_l-equipos[equipo][1])
                        if ratio_temp >= mejores[0][0]:
                            t += 1
                            heapq.heappush(mejores, (ratio_temp, (nodo,pos,nuevo_l,equipo,nodos[nodo][2])))
                            heapq.heappop(mejores)
                            flag=1
            if flag:
                if t < k:
                    for i in range(k-t):
                        heapq.heappop(mejores)
                    ind_rnd = random.randint(0,t-1)
                    nodo_act, pos_act, l_act, equipo_act, val_actual = mejores[ind_rnd][1]
                    equipos[equipo_act][0].insert(pos_act,nodo_act)
                    equipos[equipo_act][1] = l_act
                    equipos[equipo_act][2] += val_actual
                    no_visitados.remove(nodo_act)
                    z += val_actual
                    continue
                ind_rnd = random.randint(0,k-1)
                nodo_act, pos_act, l_act, equipo_act, val_actual = mejores[ind_rnd][1]
                equipos[equipo_act][0].insert(pos_act,nodo_act)
                equipos[equipo_act][1] = l_act
                equipos[equipo_act][2] += val_actual
                no_visitados.remove(nodo_act)
                z += val_actual
        if z > mejor[2]:
            mejor = [equipos]+[0]+[z]
    return mejor[0],mejor[2],int(round((time.time()-inicio)*1000))

def grasp_ruido(file_path,k,r,nsol):
    mejor = np.zeros(3)
    inicio = time.time()
    for i in range(nsol):
        z = 0
        equipos = {} #diccionario donde se accede a la ruta y longitud de cada equipo
        nodos, no_visitados, n, m, L = leer_archivo(file_path)
        ruido = crear_ruido(nodos,r)
        for equipo in range(m):
            equipos[equipo] = [[0,n-1],(distancia(0,n-1,ruido)),0]
        flag = True
        while flag:
            mejores = []
            for i in range(k):
                heapq.heappush(mejores, (0, ""))
            flag = 0
            ratio = 0
            t = 0
            for equipo in range(m): #Para cada equipo
                for nodo in no_visitados: #Para cada nodo
                    for pos in range(1,(len(equipos[equipo][0]))):
                        nuevo_l = nueva_distancia(equipos[equipo],nodo,pos,ruido)
                        if nuevo_l > L: continue
                        ratio_temp = ruido[nodo][2]/(nuevo_l-equipos[equipo][1])
                        if ratio_temp >= mejores[0][0]:
                            t += 1
                            heapq.heappush(mejores, (ratio_temp, (nodo,pos,nuevo_l,equipo,ruido[nodo][2])))
                            heapq.heappop(mejores)
                            flag=1
            if flag:
                if t < k:
                    for i in range(k-t):
                        heapq.heappop(mejores)
                    ind_rnd = random.randint(0,t-1)
                    nodo_act, pos_act, l_act, equipo_act, val_actual = mejores[ind_rnd][1]
                    equipos[equipo_act][0].insert(pos_act,nodo_act)
                    equipos[equipo_act][1] = l_act
                    equipos[equipo_act][2] += nodos[nodo_act][2]
                    no_visitados.remove(nodo_act)
                    z += nodos[nodo_act][2]
                    continue
                ind_rnd = random.randint(0,k-1)
                nodo_act, pos_act, l_act, equipo_act, val_actual = mejores[ind_rnd][1]
                equipos[equipo_act][0].insert(pos_act,nodo_act)
                equipos[equipo_act][1] = l_act
                equipos[equipo_act][2] += nodos[nodo_act][2]
                no_visitados.remove(nodo_act)
                z += nodos[nodo_act][2]
        if z > mejor[2]:
            mejor = [equipos]+[0]+[z]
    return mejor[0],mejor[2],int(round((time.time()-inicio)*1000))
