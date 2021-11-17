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
    def shortest_path(self, start, end, extra_cost = 0, blocked = []):
        '''
        Halla el camino más corto entre dos puntos de la cuadrícula.

        Parámetros:

        - start (tupla): Coordenadas del inicio.
        - end (tupla): Coordenadas del final.
        - extra_cost (real): Costo adicional al pasar por los arcos, puede transformarse
        en una ganancia si se define como un valor negativo (vale 0 por defecto).
        - blocked (lista de tuplas): Indica los trayectos entre dos puntos que deben omitirse
        a la hora de calcular la ruta más corta. Las tuplas contienen dos tuplas que representan
        el punto de inicio del trayecto y el punto final del mismo (en ese mismo orden).

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
        for point in blocked:
            fixed_matrix[self.point_index(point[0][0], point[0][1])][self.point_index(point[1][0], point[1][1])] = float('inf')
            fixed_matrix[self.point_index(point[1][0], point[1][1])][self.point_index(point[0][0], point[0][1])] = float('inf')
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
    def check_collision(self, path_j,path_a):
        '''Detecta si existe una colision entre los caminos de Javier y Andreina se reciben dos listas
        con las rutas que toman cada uno

        Parámetros:
         path_j(lista de listas): El camino de Javier, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos, se incluye el tiempo extra que le tomaria a
         uno de los dos en caso de que uno tenga que salir antes (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).

        path_a(lista de listas): El camino de Andreina, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos, se incluye el tiempo extra que le tomaria a
         uno de los dos en caso de que uno tenga que salir antes (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).
         retorna:
         (lista de tuplas) edge_list: booleano que describe si existe una colision o no.
        '''
        node_of_conflict = None
        edge_of_conflict = None
        collision_type = 'Neither'
        #Se obtienen todas las coordenadas de la matriz de adyacencia de los nodos por lo que pasa Javier
        coordinates_path_j = [self.point_index(path_j[0][i]) for i in range(len(path_j[0])-1) ]
        #Se obtienen todas las coordenadas de la matriz de adyacencia de los nodos por lo que pasa Andreina
        coordinates_path_a = [self.point_index(path_a[0][i]) for i in range(len(path_a[0])-1) ]

        #camino de javier sin el nodo destino
        route_j = [path_j[0][i] for i in range(len(path_j[0])-1)]
        #Camino de Andreina sin el nodo destino
        route_a = [path_a[0][i] for i in range(len(path_a[0])-1)]
        # Se recorren los nodos por los que pasa andreina de andreina
        for node in route_a:
        # Con cada nodo de andreina se Checkea si uno de estos existe en la ruta de Javier,en caso de ser asi se checkea si pasan por el mismo arco
            if route_j.count(node) != 0:
                if path_j[1][route_j.index(node)] == path_a[1][route_a.index(node)]:
                    if path_j[0][route_j.index(node) + 1] == path_a[0][route_a.index(node) + 1]:
                        collision_type = 'Node'
                        node_of_conflict = node
                #Se compureba si el siguiente nodo de la ruta de ambos es el mismo
                if path_j[0][route_j.index(node) + 1 ] == path_a[0][route_a.index(node) + 1]:
                    #Inserte calculo de de comprobar los tiempos
                    #minutes javier representa los minutos en los que javier esta recorriendo el arco 
                    # (Ej: javier esta en el nodo A en t=17, recorre una calle y ahora se encuentra en el nodo B en t=22, la lista minutes_javer seria [17,18,19,20,21,22] )
                    minutes_javier = [i for i in range(path_j[1][route_j.index(node)],path_j[1][route_j.index(node)]  + 1)]
                    minutes_andreina = [i for i in range(path_a[1][route_a.index(node)], path_a[1][route_a.index(node)] + 1)]
                    edge_of_conflict = (path_a[0][route_a.index(node)],path_a[0][route_a.index(node) + 1])

                #Se compurba si el nodo anterior de Javier, es igual que el nodo siguiente de Andreina (Andreina va en sentido contrario)
                if path_j[0][route_j.index(node) - 1 ] == path_a[0][route_a.index(node) + 1]:
                    #Inserte calculo de de comprobar los tiempos
                    minutes_javier = [i for i in range(path_j[1][route_j.index(node)] - 1,path_j[1][route_j.index(node)])]
                    minutes_andreina = [i for i in range(path_a[1][route_a.index(node)], path_a[1][route_a.index(node)] + 1)]
                    edge_of_conflict = (path_a[0][route_a.index(node)],path_a[0][route_a.index(node) + 1])
                    
                #Se compurba si el nodo anterior de Andreina, es igual que el nodo siguiente de Javier (Javier va en sentido contrario)
                if path_j[0][route_j.index(node) + 1 ] == path_a[0][route_a.index(node) - 1]:
                    #Inserte calculo de de comprobar los tiempos
                    minutes_javier = [i for i in range(path_j[1][route_j.index(node)],path_j[1][route_j.index(node)]  + 1)]
                    minutes_andreina = [i for i in range(path_a[1][route_a.index(node)] - 1, path_a[1][route_a.index(node)])]
                    if self.check_common_elements(minutes_andreina,minutes_javier):
                        collision_type = 'Edge'
                        edge_of_conflict = (path_a[0][route_a.index(node)],path_a[0][route_a.index(node) - 1])
                    
            
        return collision_type,edge_of_conflict,node_of_conflict
    def check_common_elements(self,array_1,array_2):
        '''
        Funcion que detecta si dos arreglos tienen elementos en comun

        parametros: 
        arra_1: primer arreglo a comparar
        array_2: segundo arreglo a comparar

        retorna:
        common_element(boolean): booleano que describe si hay elementos en comun o no
        Retorna verdadero si existe al menos 1 elemento en comun en ambos, si no retorna false
        '''
        common_element = False
        for element in array_1:
            if array_2.count(element) != 0:
                common_element = True
                break
        return  common_element

    def align_arriving_times(self,path_j,path_a):
        '''
        actualiza los tiempos de andreina y Javier
        parametros:
        path_j(lista de listas): El camino de Javier, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos(para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).

        path_a(lista de listas): El camino de Andreina, expresado como una lista que contiene dos vectores,
         el primero indica los puntos que se visitan,
         el segundo los tiempos mínimos para llegar a dichos nodos (para
         determinar el tiempo mínimo de la ruta, se revisa el último elemento del segundo vector).
         retorna:
         updated_path_j (lista de listas): camino actualizado con los pesos para que ambos lleguen al mismo tiempo
         updated_path_a (lista de listas): camino actualizado con los pesos para que ambos lleguen al mismo tiempo
         slower_person (String): Nombre de la persona que tiene que salir antes
         time_difference (number): Tiempo en minutos en el que debe salir mas temprano la persona que tarda mas tiempo
        '''
        slower_person = ''
        #Se resta el tiempo que le toma a Andreina a llegar al destino con el tiempo que le toma a Javier
        time_difference = path_a[1][-1] - path_j[1][-1]
        path_dictionary = {
            'Javier': path_j,
            'Andreina': path_a,
            'Neither': [[],[]]
        }
        if time_difference < 0:
        #Si la diferencia es negativa, entonces el tiempo de Andreina es Mayor, ella debe salir antes, o Javier debe salir despues
            slower_person = 'Javier'
            faster_person = 'Andreina'
        elif time_difference > 0:
            #Si la diferencia es positiva, entonces el tiempo de Javier es Mayor, el debe salir antes, o Andreina debe salir despues
            slower_person = 'Andreina'
            faster_person = 'Javier'
        else:
            #Si la diferencia es igual a 0 entonces no es necesario un tuempo extra
            slower_person = 'Neiher'
            return path_dictionary['Javier'],path_dictionary['Andreina'],slower_person,time_difference
        time_difference = abs(time_difference)
        for i in range(len(path_dictionary[faster_person][1])):
            #Se le agrega un tiempo extra a la persona mas rapida para denotar que saldra unos minutos despues que la persona lenta
            path_dictionary[faster_person][1][i] = path_dictionary[faster_person][1][i] + time_difference
        updated_path_j,updated_path_a = path_dictionary['Javier'],path_dictionary['Andreina']
        #Se retornan los caminos con pesos actualizados y se indica quien debe salir primero y con cuanto tiempo
        return updated_path_j,updated_path_a,slower_person,time_difference

prueba = Grid(55, 50, 15, 10, [5, 10, 5, 5, 5, 5], [5, 5, 7, 7, 7, 5])
print('Javier:', prueba.shortest_path((14,54), (14, 50)))
print('Andreina:', prueba.shortest_path((13,52), (14, 50), 2, [((13, 52), (14, 52))]))
print("Times fixed ", prueba.align_arriving_times(prueba.shortest_path((14,54), (14, 50)),
prueba.shortest_path((13,52), (14, 50), 2, [((13, 52), (14, 52))])))
#Para probar el método shortest_path
""" 
prueba = Grid(55, 50, 15, 10, [5, 10, 5, 5, 5, 5], [5, 5, 7, 7, 7, 5])
print('Javier:', prueba.shortest_path((14,54), (14, 50)))
print('Andreina:', prueba.shortest_path((13,52), (14, 50), 2, [((13, 52), (14, 52))]))
"""