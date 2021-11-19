import sys
import tkinter as tk
from UI.UI import UI
from Classes import Grid

def main() -> None:

    root = tk.Tk()
    Window = UI(root)


if __name__ == '__main__':
    main()
    sys.exit(0)
