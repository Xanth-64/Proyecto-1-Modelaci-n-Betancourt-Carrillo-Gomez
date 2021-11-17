import sys
import tkinter as tk
from UI.UI import UI
from Classes import Grid

def main() -> None:
    prueba = Grid(55, 50, 15, 10, [5, 10, 5, 5, 5, 5], [5, 5, 7, 7, 7, 5])
    print('Javier:', prueba.shortest_path((14,54), (14, 50)))
    print('Andreina:', prueba.shortest_path((13,52), (14, 50), 2, [((13, 52), (14, 52))]))
    root = tk.Tk()
    Window = UI(root)


if __name__ == '__main__':
    main()
    sys.exit(0)
