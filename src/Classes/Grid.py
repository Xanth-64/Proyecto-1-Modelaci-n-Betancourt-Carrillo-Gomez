class Grid:
    '''
    Clase que construye una cuadrícula.

    Atributos:

    - coordinates (lista): Lista que contiene todos los puntos de la cuadrilla
    en coordenadas tipo (carrera, calle).
    - matrix (lista de listas): Matriz de adyacencia.
    '''
    def __init__(
        self,
        limit_n,
        limit_s,
        limit_w,
        limit_e,
        x_axis_costs,
        y_axis_costs
        ):
        '''
        Construye un objeto de la clase Grid.

        Parámetros:

        - limit_n (entero): Número de la calle que limita la cuadrilla por el norte.
        - limit_s (entero): Número de la calle que limita la cuadrilla por el sur.
        - limit_w (entero): Número de la carrera que limita la cuadrilla por el oeste.
        - limit_e (entero): Número de la carrera que limita la cuadrilla por el este.
        - x_axis_costs (lista): Lista que contiene los costos en minutos para cruzar
        horizontalmente por cada calle (los costos deben estar ordenados ascendentemente
        por número de calle).
        - y_axis_costs (lista): Lista que contiene los costos en minutos para cruzar
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
                    self.matrix[self.find_point(x, y)][self.find_point(x - 1, y)] = x_axis_costs[y - limit_s]
                    self.matrix[self.find_point(x - 1, y)][self.find_point(x, y)] = x_axis_costs[y - limit_s]
                if x + 1 <= limit_w:
                    self.matrix[self.find_point(x, y)][self.find_point(x + 1, y)] = x_axis_costs[y - limit_s]
                    self.matrix[self.find_point(x + 1, y)][self.find_point(x, y)] = x_axis_costs[y - limit_s]
                if y - 1 >= limit_s:
                    self.matrix[self.find_point(x, y)][self.find_point(x, y - 1)] = y_axis_costs[x - limit_e]
                    self.matrix[self.find_point(x, y - 1)][self.find_point(x, y)] = y_axis_costs[x - limit_e]
                if y + 1 <= limit_n:
                    self.matrix[self.find_point(x, y)][self.find_point(x, y + 1)] = y_axis_costs[x - limit_e]
                    self.matrix[self.find_point(x, y + 1)][self.find_point(x, y)] = y_axis_costs[x - limit_e]


    def find_point(self, x, y):
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
