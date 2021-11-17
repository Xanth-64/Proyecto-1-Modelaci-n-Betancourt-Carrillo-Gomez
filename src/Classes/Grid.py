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
#Para probar el método shortest_path
""" 
prueba = Grid(55, 50, 15, 10, [5, 10, 5, 5, 5, 5], [5, 5, 7, 7, 7, 5])
print('Javier:', prueba.shortest_path((14,54), (14, 50)))
print('Andreina:', prueba.shortest_path((13,52), (14, 50), 2, [((13, 52), (14, 52))]))
"""