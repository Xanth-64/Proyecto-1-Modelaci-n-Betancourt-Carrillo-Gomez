from sys import path


class Grid:
    '''
    Clase que construye una cuadrícula.

    Atributos:

    - coordinates (lista de tuplas): Lista que contiene todos los puntos de la cuadrilla
    en coordenadas tipo (carrera, calle).
    - matrix (lista de listas): Matriz de adyacencia.
    '''
    def __init__(
        self,
        limit_n,
        limit_s,
        limit_w,
        limit_e,
        horizontal_costs,
        vertical_costs
        ):
        '''
        Construye un objeto de la clase Grid.

        Parámetros:

        - limit_n (entero): Número de la calle que limita la cuadrilla por el norte.
        - limit_s (entero): Número de la calle que limita la cuadrilla por el sur.
        - limit_w (entero): Número de la carrera que limita la cuadrilla por el oeste.
        - limit_e (entero): Número de la carrera que limita la cuadrilla por el este.
        - horizontal_costs (lista de reales): Lista que contiene los costos en minutos para cruzar
        horizontalmente por cada calle (los costos deben estar ordenados ascendentemente
        por número de calle).
        - vertical_costs (lista de reales): Lista que contiene los costos en minutos para cruzar
        verticalmente por cada carrera (los costos deben estar ordenados ascendentemente
        por número de carrera).
        '''
        self.coordinates = [
            (x, y)
            for x in range(limit_e, limit_w + 1)
            for y in range(limit_s, limit_n + 1)
        ]
        self.matrix = [
            [0 if x == y else float('inf') for x in range(len(self.coordinates))]
            for y in range(len(self.coordinates))
        ]
        for x in range(limit_e, limit_w + 1):
            for y in range(limit_s, limit_n + 1):
                if x - 1 >= limit_e:
                    self.matrix[self.point_index(x, y)][self.point_index(x - 1, y)] = horizontal_costs[y - limit_s]
                    self.matrix[self.point_index(x - 1, y)][self.point_index(x, y)] = horizontal_costs[y - limit_s]
                if x + 1 <= limit_w:
                    self.matrix[self.point_index(x, y)][self.point_index(x + 1, y)] = horizontal_costs[y - limit_s]
                    self.matrix[self.point_index(x + 1, y)][self.point_index(x, y)] = horizontal_costs[y - limit_s]
                if y - 1 >= limit_s:
                    self.matrix[self.point_index(x, y)][self.point_index(x, y - 1)] = vertical_costs[x - limit_e]
                    self.matrix[self.point_index(x, y - 1)][self.point_index(x, y)] = vertical_costs[x - limit_e]
                if y + 1 <= limit_n:
                    self.matrix[self.point_index(x, y)][self.point_index(x, y + 1)] = vertical_costs[x - limit_e]
                    self.matrix[self.point_index(x, y + 1)][self.point_index(x, y)] = vertical_costs[x - limit_e]


    def point_index(self, x, y):
        '''
        Busca el número de índice dentro de la lista \"coordinates\" de un punto en la
        cuadrícula.

        Parámetros:

        - x (entero): Número de carrera.
        - y (entero): Número de calle.

        Retorna:

        - (entero): Número de índice del punto dentro de la lista \"coordinates\".
        '''
        return self.coordinates.index((x, y))
    def shortest_path(self, start, end, extra_cost = 0):
        '''
        Halla el camino más corto entre dos puntos de la cuadrícula.

        Parámetros:

        - start (tupla): Coordenadas del inicio.
        - end (tupla): Coordenadas del final.
        - extra_cost (real): Costo adicional al pasar por los arcos, puede transformarse
        en una ganancia si se define como un valor negativo (vale 0 por defecto).

        Retorna:

        - (lista de listas): Una lista que contiene dos vectores, el primero indica los
        puntos que se visitan y el segundo los tiempos mínimos para llegar a dichos nodos (para
        determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).
        '''
        times = [0 if point == start else float('inf') for point in self.coordinates]
        checked = [False for point in self.coordinates]
        preview = [None for point in self.coordinates]
        current = self.point_index(start[0], start[1])
        fixed_matrix = self.matrix
        path = [[], []]
        while checked.count(False) > 0:
            checked[current] = True
            times_from_current = fixed_matrix[current]
            times_from_current[current] = float('inf')
            for i in range(len(times_from_current)):
                if times[current] + times_from_current[i] + extra_cost < times[i]:
                    times[i] = times[current] + times_from_current[i] + extra_cost
                    preview[i] = current
            times_from_current = [times[i] if not(checked[i]) else float('inf') for i in range(len(times))]
            current = times_from_current.index(min(times_from_current))
        current = self.point_index(end[0], end[1])
        while current:
            path[0].insert(0, self.coordinates[current])
            path[1].insert(0, times[current])
            current = preview[current]
        return path
    def check_collision(self, path_1,path_2):
        '''Detecta si existe una colision entre los caminos de Javier y Andreina se reciben dos listas
        con las rutas que toman cada uno

        Parámetros:
         path_1(lista de listas): El camino de Javier, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos, se incluye el tiempo extra que le tomaria a
         uno de los dos en caso de que uno tenga que salir antes (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).

        path_2(lista de listas): El camino de Andreina, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos, se incluye el tiempo extra que le tomaria a
         uno de los dos en caso de que uno tenga que salir antes (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).

         retorna:

         collision_type(String): te dice el tipo de colision, su valor es de Node, Edge o Neither

         edge_of_conflict(tupla de tuplas): Te describe el arco donde ocurre la colision, da dos tuplas, cada tupla es un nodo
         si no hay colision por arco entonces este campo retorna Nulo

         node_of_conflict(tupla): Te describe el nodo donde ocurre la colision, en caso de que no haya
         colision por nodo este campo retorna Nulo
        '''
        node_of_conflict = None
        edge_of_conflict = None
        collision_type = 'Neither'

        #camino de javier sin el nodo destino
        route_j = [path_1[0][i] for i in range(len(path_1[0])-1)]
        #Camino de Andreina sin el nodo destino
        route_a = [path_2[0][i] for i in range(len(path_2[0])-1)]
        # Se recorren los nodos por los que pasa andreina
        for i,node_a in enumerate(route_a):
        # Con cada nodo de andreina se Checkea si uno de estos existe en la ruta de Javier,en caso de ser asi se checkea si pasan por el mismo arco
            for j, node_j in enumerate(route_j) :
                #Se comprueba si presentan un nodo compartido en sus rutas
                if node_a == node_j:
                    # Y se verifica que dichos nodos compartidos sigan el mismo arco
                    if (path_2[0][i + 1] == path_1[0][j + 1]):
                    # En caso de que tengan un arco compartido, se verifica si lo recorrieron en tiempos que se solapan
                        if not((path_2[1][i] >= path_1[1][j + 1]) or (path_2[1][i + 1] >= path_1[1][j + 1])):
                            collision_type = 'Edge'
                            edge_of_conflict = (node_a,path_2[0][i + 1])
                    # Ahora tomamos en cuenta los casos donde se encuentren frente a frente (recorriendo en sentido contrario)
                    if i >= 1:
                        if(path_2[0][i - 1] == path_1[0][j + 1]):
                            # Vemos si lo recorrieron en tiempos que se solapan
                            if not (path_1[1][j] >= path_2[1][i] or path_2[1][i - 1] >= path_1[1][j + 1]):
                                collision_type = 'Edge'
                                edge_of_conflict = (path_1[0][j], path_1[0][j + 1])

                    if j>= 1:
                        if(path_2[0][i + 1] == path_1[0][j - 1]):
                            # Vemos si lo recorrieron en tiempos que se solapan
                            if not (path_2[1][i] >= path_1[1][j] or path_1[1][j - 1] >= path_2[1][i + 1]):
                                collision_type = 'Edge'
                                edge_of_conflict = (path_2[0][i], path_2[0][i + 1])
        # Si no existe arco en comun, se checkea que no exista nodo en comun donde ambos lleguen al mismo tiempo
        if collision_type != 'Edge':
            for node in route_a:
                if route_j.count(node) != 0 and path_1[1][route_j.index(node)] == path_2[1][route_a.index(node)]:
                    collision_type = 'Node'
                    node_of_conflict = node
                    break
        return collision_type,edge_of_conflict,node_of_conflict

    def align_arriving_times(self,path_1,path_2):
        '''
        actualiza los tiempos de andreina y Javier
        parametros:
        path_1(lista de listas): El camino 1, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos(para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).

        path_2(lista de listas): El camino 2, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).
         retorna:
         updated_path_1 (lista de listas): camino actualizado con los pesos para que ambos lleguen al mismo tiempo

         updated_path_2 (lista de listas): camino actualizado con los pesos para que ambos lleguen al mismo tiempo

         slower_person (String): Nombre de la persona que tiene que salir antes

         time_difference (number): Tiempo en minutos en el que debe salir mas temprano la persona que tarda mas tiempo

        '''
        slower_person = -1
        #Se resta el tiempo que le toma a Andreina a llegar al destino con el tiempo que le toma a Javier
        time_difference = path_2[1][-1] - path_1[1][-1]
        path_dictionary = {
            1: path_1,
            2: path_2,
            0: [[],[]]
        }
        if time_difference < 0:
        #Si la diferencia es negativa, entonces el tiempo de Andreina es Mayor, ella debe salir antes, o Javier debe salir despues
            slower_person = 1
            faster_person = 2
        elif time_difference > 0:
            #Si la diferencia es positiva, entonces el tiempo de Javier es Mayor, el debe salir antes, o Andreina debe salir despues
            slower_person = 2
            faster_person = 1
        else:
            #Si la diferencia es igual a 0 entonces no es necesario un tuempo extra
            slower_person = 0
            return path_dictionary[1],path_dictionary[2],slower_person,time_difference
        time_difference = abs(time_difference)
        for i in range(0,len(path_dictionary[faster_person][1])):
            #Se le agrega un tiempo extra a la persona mas rapida para denotar que saldra unos minutos despues que la persona lenta
            path_dictionary[faster_person][1][i] = path_dictionary[faster_person][1][i] + time_difference
        updated_path_1,updated_path_2 = path_dictionary[1],path_dictionary[2]
        #Se retornan los caminos con pesos actualizados y se indica quien debe salir primero y con cuanto tiempo
        return updated_path_1,updated_path_2,slower_person,time_difference

    def calcular_caminos(self,starting_node_1,starting_node_2,ending_node):
        diccionario_personas = {
    1: 'Javier',
    2: 'Andreina',
    0: 'Neither'
        }
        slowest_person = 3
        start_time = 0
        colision_type = 'Undefined'
        path_1 = self.shortest_path(starting_node_1,ending_node)
        path_2 = self.shortest_path(starting_node_2,ending_node,extra_cost=2)
        path_1,path_2,slowest_person,start_time = self.align_arriving_times(path_1,path_2)
        colision_type,edge_of_conflict,node_of_conflict = self.check_collision(path_1,path_2)
        while colision_type != 'Neither':
            colision_type,edge_of_conflict,node_of_conflict = self.check_collision(path_1,path_2)
            if colision_type != 'Neither':
                if colision_type == 'Node':
                    node_index = self.point_index(node_of_conflict[0],node_of_conflict[1])
                    #Eliminar todos los arcos de ese nodo 
                    #Quitar todos los arcos que conecten al nodo en la matriz del mas lento
                    for i in range(len(self.coordinates)):
                        self.matrix[i][node_index] = float('inf')
                        self.matrix[node_index][i] = float('inf')
                if colision_type == 'Edge':
                    edge_index = (self.point_index(edge_of_conflict[0][0],edge_of_conflict[0][1]),self.point_index(edge_of_conflict[1][0],edge_of_conflict[1][1]))
                    #Quitar el arco en comun que causa el conflicto, Edge of conflict tiene una tupla con el par de nodos
                    #Poner float inf al peso del arco conflictivo
                    self.matrix[edge_index[0]][edge_index[1]] = float('inf')
                    self.matrix[edge_index[1]][edge_index[0]] = float('inf')
                if diccionario_personas[slowest_person] == 'Javier':
                    #Calcular el nuevo camino y checkear si hay conflicto todavia
                    path_2 = self.shortest_path(starting_node_2,ending_node,extra_cost=2)
                    path_1,path_2,slowpoke,start_time2 = self.align_arriving_times(path_1,path_2)
                    start_time =start_time + start_time2
                    colision_type,edge_of_conflict,node_of_conflict = self.check_collision(path_1,path_2)
                elif diccionario_personas[slowest_person] == 'Andreina':
                    #calcular el nuevo camino y checkear si hay conflicto todavia
                    path_1 = self.shortest_path(starting_node_2,ending_node)
                    path_1,path_2,slowpoke,start_time2 = self.align_arriving_times(path_1,path_2)
                    start_time = start_time + start_time2
                    colision_type,edge_of_conflict,node_of_conflict = self.check_collision(path_1,path_2)

        return path_1,path_2,diccionario_personas[slowest_person],start_time
