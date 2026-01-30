from Read_Instance import *


def nodos_posibles(lista_centros):

    nodos={}
    nodos_usados=[]
    for i in range(len(lista_centros)):
        nodos[i]=[]

    for i in range(len(lista_centros)):
        # De acuerdo a la distancia vemos con que centro podria estar cada uno de los nodos 
        for j in V:
            if j !=i:
                if distancia[i][j]<=Lmax:
                    if j not in nodos_usados:
                        nodos[i].append(j)
        #Ordenamos la lista de nodos de acuerdo a la distancia con el nodo centro
        nodos[i].sort(key=lambda x: distancia[i][x])

    #print(nodos)
    nodos=dict(sorted(nodos.items(), key=lambda x: len(x[1])))

    for i in nodos:
        #print(i)
        # print(nodos[i],i)
        #truncamos en la cantidad de nodos que queremos
        if len(nodos[i])>s2:
            nodos[i] = nodos[i][:int(s2)]
        
        #Vamos a agregar nodos hasta un limite de poblacion
        suma = 0
        suma_obj=0
        indice = 0
        while indice < len(nodos[i]):
            if suma + poblacion[nodos[i][indice]] <= PP*(1-coef):
                if suma_obj + c[nodos[i][indice]] <= Lavg:
                    
                    suma += poblacion[nodos[i][indice]]
                    suma_obj += c[nodos[i][indice]]
                    indice += 1
                else: 
                    # Truncar la lista desde aquí hacia el final no cumple con 
                    del nodos[i][indice:]
                    break

            else:
                # Truncar la lista desde aquí hacia el final
                del nodos[i][indice:]
                break
        print(sum(poblacion[k] for k in nodos[i]),PP*(1+coef))

        for n in nodos[i]:
            nodos_usados.append(n)
    
    return nodos

                                                                                                                                                                                               
def DFS(nodos_finales,lista_centros):

    tree={}

    for q in range(len(lista_centros)):
        lista_nodos = list(nodos_finales[q])
        nodos_validos = []
        print(q, lista_nodos, 'verifiacion de que entra a la funcion')
        for j in lista_nodos:
            print(j, 'j que entra al for')
            if j != q:
                vecinos = [i for i in lista_nodos if i != j and (j, i) in E]
                print(vecinos)
                if len(vecinos) > 0:
                    nodos_validos.append(j)
               
            else:
                nodos_validos.append(j)
                    
        asign= nodos_validos
        SubMA = adyacencia.loc[asign,asign]
        adj = {u: [v for v in asign if SubMA.at[u, v] != 0] for u in asign}

        visitado = set([asign[0]]) 
        spanning_tree = []
        pendientes = sorted([n for n in asign if n != asign[0]]) 

        while pendientes:
            # Buscar el nodo de menor índice que tenga vecinos visitados
            for i, v in enumerate(pendientes):  # Recorre pendientes desde el menor índice
                vecinos_visitados = [n for n in adj[v] if n in visitado]
                print(v, vecinos_visitados,'vecinos visitados de un nodo')
                
                if vecinos_visitados:  # Si v tiene al menos un vecino ya visitado
                    padre = min(vecinos_visitados)  # Escoge el vecino de menor índice
                    spanning_tree.append((padre, v))  # Crea el arco
                    visitado.add(v)  # Marca v como visitado
                    pendientes.pop(i)  # Quita v de la lista de pendientes
                    break  # Sale del for y vuelve al while

        tree[q] = spanning_tree
        tree[q].append(('fict', q)) 

    return tree
                        
   