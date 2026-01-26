from Read_Instance import *


def subgrafo(lista):
    nodo_idx = {nodo: idx for idx, nodo in enumerate(lista)}
    idx_nodo = {idx: nodo for nodo, idx in nodo_idx.items()}

    # construimo matriz de adyacencia
    n = len(lista)
    A = np.zeros((n, n), dtype=int)

    for (k, j) in E:
        if k<j:
            if k in nodo_idx and j in nodo_idx:
                A[nodo_idx[k], nodo_idx[j]] = 1

    # Paso 4: recuperar arcos reales desde la matriz
    arcos_filtrados = []
    for k in range(n):
        for j in range(n):
            if A[k][j] == 1:
                arcos_filtrados.append((idx_nodo[k], idx_nodo[j]))
                arcos_filtrados.append((idx_nodo[j], idx_nodo[k]))
    
    
    return arcos_filtrados 


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
        indice = 0
        while indice < len(nodos[i]):
            #print(suma)
            if suma + poblacion[nodos[i][indice]] <= PP*(1-coef):
                suma += poblacion[nodos[i][indice]]
                indice += 1
            else:
                # Truncar la lista desde aquí hacia el final
                del nodos[i][indice:]
                break
        print(sum(poblacion[k] for k in nodos[i]),PP*(1+coef))

        for n in nodos[i]:
            nodos_usados.append(n)
    
    return nodos

def kruskal(arcos):
    tupla=[]
    for (i,j) in arcos:
        if i<j:
            dist=distancia[i][j]
            tupla.append((i,j,dist))

    #print(tupla)
    G = nx.Graph()
    G.add_weighted_edges_from(tupla)
    #print(m._eta_psc.x)
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
    spanning=list(mst.edges(data=True))
    #print(spanning)

    lista_spanning=[]

    for (i,j,d) in spanning:
        lista_spanning.append((i,j))

    return lista_spanning


def dijkstra(nodo,E):

    tupla=[]
    for (i,j) in E:
        dist=distancia[i][j]
        tupla.append((i,j,dist))

    G = nx.Graph()

    #Formamos el grafo
    G.add_weighted_edges_from(tupla)
    paths = nx.single_source_dijkstra_path(G, source=nodo, weight='weight')

    arcos = set()

    for path in paths.values():
        for u, v in zip(path[:-1], path[1:]):
            arcos.add((u, v)) 
            #arcos.add((v, u)) 
    
    arcos=list(arcos)
    
    return arcos


def arcos_finales(nodos,lista_centros):

    arcos={}
    for q in range(len(lista_centros)):
        arcos[q]=[]
    
    for i in range(len(lista_centros)):
        if len(nodos[i])>1:
            arcos_finales= subgrafo(nodos[i])
            #print(arcos_finales)
            arbol= dijkstra(i,arcos_finales)
            arcos[i].extend(arbol)
    
    return arcos


def spanning_tree(raiz):
    tupla=[]
    for (i,j) in E:
        dist=distancia[i][j]
        #dist=c[i]+c[j]
        tupla.append((i,j,dist))
    
    #definimos el grafo
    G = nx.Graph()

    #Formamos el grafo
    G.add_weighted_edges_from(tupla)
    
    T = nx.minimum_spanning_tree(G, weight='weight')

    # Árbol enraizado (BFS)
    rooted_tree = nx.bfs_tree(T, source=raiz)

    arcos=set()
    for path in rooted_tree.edges():
        for u, v in zip(path[:-1], path[1:]):
            arcos.add((u, v)) 

    #FUNCION QUE ENTREGA EL NIVEL DE CADA NODO EN EL ARBOL
    U = nx.single_source_shortest_path_length(rooted_tree, source=raiz)

    return arcos,U


def sol_factible(raiz,des):
    
    arbol,grado=spanning_tree(raiz)
    print(arbol)

    grado = dict(sorted(grado.items(), key=lambda x: x[1], reverse=True))
    #print(grado)

    w={}
    for i in V:
        w[i]=poblacion[i]

    b={}
    for i in V:
        b[i]=[i]

    distritos=[]
    #lamda=PP*(1-coef)+ (PP*(1-coef)*des)
    lamda=PP*(1+coef)
    #lamda=PP*(1-coef)
    print('AQUI LAMDA',lamda)

    for i in grado:
        if w[i]+sum(w[j] for j in V if (i,j) in arbol)<lamda:
            #print('Caso_1')

            contar_distancia=0
            for j in V:
                if (i,j) in arbol:
                    for k in b[j]:
                        if distancia[i][k]>=Lmax:
                            contar_distancia+=1

            if contar_distancia>=1:
                w[i]= w[i]
            
            else:
                if contar_distancia==0:
                    w[i]=w[i]+sum(w[j] for j in V if (i,j) in arbol)

                    for j in V:
                        if (i,j) in arbol:
                            for k in b[j]:
                                b[i].append(k)

        else:
            if w[i]+sum(w[j] for j in V if (i,j) in arbol)>lamda:
                minor_weight=min(w[j] for j in V if (i,j) in arbol)
                min_j = min((j for j in V if (i, j) in arbol), key=lambda x: w[x])

                if w[i]+ minor_weight<lamda:
                    w[i]= w[i]+minor_weight

                    for k in b[min_j]:
                        b[i].append(k)

                    for j in V:
                        if (i,j) in arbol:
                            if j!= min_j:
                                distritos.append(j)
                else:
                    w[i]= w[i]
                    distritos.append(min_j)

    distritos.append(raiz)

    # print(w)
    # print(b)
    # print(distritos)

    return distritos,b


def symmetry_f(nodos,lista_centros):

    arcos = {}
    for q in range(len(lista_centros)):
        # inicialización
        arcos[q] = set()
        padre = {}
        lista_nodos = list(nodos[q])
        raiz = min(lista_nodos)
        padre[raiz] = 'fict'

        # verificamos que cada nodo cuente con al menos un vecino, esto donde estamos eliminando el ultimo vecino de la lista
        min_vecino = {}
        nodos_validos = []
        for j in lista_nodos:
            if j != raiz:
                vecinos = [i for i in lista_nodos if i != j and (j, i) in E]
                if len(vecinos) > 0:
                    nodos_validos.append(j)
                else:
                    print(j, 'se elimina por no tener vecinos')
            else:
                nodos_validos.append(j)
        
        lista_nodos = nodos_validos

        #Una vez que tenemos los nodos reales en la lista, buscamos su vecino de menor indice
        for j in lista_nodos:
            if j != raiz:
                vecinos = [i for i in lista_nodos if i != j and (j, i) in E]
                if len(vecinos) > 0:
                    min_vecino[j] = min(vecinos)
                    
        for j in lista_nodos:
            if j == raiz:
                continue
            # si su vecino mínimo es menor, es su padre 
            if min_vecino[j] < j:
                padre[j] = min_vecino[j]
            else: #esto es para evitar ciclos de 2 
                candidatos = [i for i in lista_nodos if (i, j) in E]
                padre[j] = max(candidatos)
        
        #Anadimos arco entre padre y hijo 
        for i in lista_nodos:
            arcos[q].add((padre[i],i))

    return arcos

                                                                                                                                                                                               

                        