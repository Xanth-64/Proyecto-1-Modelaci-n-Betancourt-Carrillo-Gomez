import tkinter as tk
from tkinter.font import Font

class UI(tk.Frame):
    def __init__(self,master : tk.Tk) -> None:
        super().__init__(master=master)
        self.master: tk.Tk = master
        self.inicializar_variables()
        self.configurar_ventana()
        self.crear_componentes()

    def inicializar_variables(self) -> None:
        # TODO Añadir la inicializacion de variables para la logica de la aplicación
        pass

    def configurar_ventana(self) -> None:
        # Almacenamos tanto el ancho como el alto de la pantalla del usuario
        self.altopantalla : int = self.master.winfo_screenheight()
        self.anchopantalla : int = self.master.winfo_screenwidth()
        # Creamos una ventana de 600 x 600 pixeles que esté centrada en la pantalla
        # Para lo cual es necesario hacer un sencillo cálculo de geometría
        self.master.geometry(newGeometry=f'1000x600+{int((self.anchopantalla - 1000) / 2)}+{int((self.altopantalla - 600) / 2)}')
        self.master.configure(bg='#FFFFFF')

        # Configurar la ventana principal para que tengan un marco donde poner los componentes
        self.master.rowconfigure(index=0,weight=1)
        self.master.columnconfigure(index=0,weight=1)
        self.grid(row=0,column=0,rowspan=1,columnspan=1,sticky='nsew')

        # Colocar un color grisaceo de fondo al Marco principal
        self.config(bg='#F2F2F2')

        # Colocar un texto de título a la ventana principal.
        self.master.title(string='Proyecto 1 Betancourt Carrillo Gómez')
        self.master.resizable(False,False)

    def crear_componentes(self) -> None:
        # TODO Añadir el codigo para la creacion de los Componentes visuales de la interfaz
        # Creacion de los Frames secundarios y terciarios que van a dividir las secciones de la app
        self.representation_frame = tk.LabelFrame(master=self)
        self.control_frame = tk.LabelFrame(master=self)
        self.title_frame = tk.LabelFrame(master=self)
        self.credits_frame = tk.LabelFrame(master=self)
        self.subtitle_frame = tk.LabelFrame(master=self.control_frame)
        self.button_frame = tk.LabelFrame(master=self.control_frame)
        self.javier_frame = tk.LabelFrame(master=self.control_frame,text='Ruta de Javier')
        self.andreina_frame = tk.LabelFrame(master=self.control_frame,text='Ruta de Andreina')
        self.drawing_frame = tk.Canvas(master=self.representation_frame)
        # Dimensionar el frame principal y posicionar los frames secundarios

        self.rowconfigure(tuple(range(12)),weight=1)
        self.columnconfigure(tuple(range(12)), weight=1)

        self.title_frame.grid(row=0,rowspan=1,column=0,columnspan=12,sticky='nsew')
        self.credits_frame.grid(row=11,rowspan=1,column=0,columnspan=12,sticky='nsew')
        self.control_frame.grid(row=1,rowspan=10,column=0,columnspan=6,sticky='nsew')
        self.representation_frame.grid(row=1,rowspan=10,column=6,columnspan=6,sticky='nsew')

        #Dimensionar los frames Secundarios y posicionar los frames terciarios

        self.title_frame.rowconfigure(tuple(range(12)),weight=1)
        self.title_frame.columnconfigure(tuple(range(12)),weight=1)
        self.credits_frame.rowconfigure(tuple(range(12)),weight=1)
        self.credits_frame.columnconfigure(tuple(range(12)),weight=1)
        self.control_frame.rowconfigure(tuple(range(12)),weight=1)
        self.control_frame.columnconfigure(tuple(range(12)),weight=1)
        self.representation_frame.rowconfigure(tuple(range(12)),weight=1)
        self.representation_frame.columnconfigure(tuple(range(12)),weight=1)

        self.subtitle_frame.grid(row=0,rowspan=1,column=0,columnspan=12,sticky='nsew')
        self.andreina_frame.grid(row=1,rowspan=7,column=0,columnspan=6,sticky='nsew')
        self.javier_frame.grid(row=1,rowspan=7,column=6,columnspan=6,sticky='nsew')
        self.button_frame.grid(row=8,rowspan=4,column=0,columnspan=12,sticky='nsew')
        self.drawing_frame.grid(row=4,rowspan=6,column=1,columnspan=10,sticky='nsew')
        # Dimensionar los Frames Terciarios

        self.subtitle_frame.rowconfigure(tuple(range(12)),weight=1)
        self.subtitle_frame.columnconfigure(tuple(range(12)),weight=1)
        self.andreina_frame.rowconfigure(tuple(range(12)),weight=1)
        self.andreina_frame.columnconfigure(tuple(range(12)),weight=1)
        self.javier_frame.rowconfigure(tuple(range(12)),weight=1)
        self.javier_frame.columnconfigure(tuple(range(12)),weight=1)
        self.button_frame.rowconfigure(tuple(range(12)),weight=1)
        self.button_frame.columnconfigure(tuple(range(12)),weight=1)

        # NOTE El Drawing Frame es de 6 x 6 para poder representar los nodos del grafo
        self.drawing_frame.rowconfigure(tuple(range(6)),weight=1)
        self.drawing_frame.columnconfigure(tuple(range(6)),weight=1)

        # Llenar cada uno de los campos con sus respectivos elementos

        # Primero definimos fuentes para Titulos, Subtitulos, Labels y Botones

        title_font : Font = Font(font=('Helvetica',24))
        subtitle_font : Font = Font(font=('Helvetica',18))
        label_font : Font = Font(font=('Arial',12))
        button_font : Font = Font(font=('Helvetica',14))
        credits_font : Font = Font(font=('Arial',10))
        # Procedemos a Crear el Titulo los Subtitulos y los Creditos
        self.title_label = tk.Label(master=self.title_frame,font=title_font,text='Proyecto 1: Javier y Andreina❤️')
        self.subtitle_label = tk.Label(master=self.subtitle_frame,font=subtitle_font,text='Caminos Más Cortos')
        self.credits_label = tk.Label(master=self.credits_frame,font=credits_font,text='Universidad Metropolitana, 2021. Andrés Betancourt (20191110760), Alberto Carrillo (20191110827), Manuel Gómez (20191110010)')
        # Y los posicionamos en sus espacios respectivos
        self.title_label.grid(row=0,rowspan=12,column=0,columnspan=12)
        self.subtitle_label.grid(row=0,rowspan=12,column=0,columnspan=12)
        self.credits_label.grid(row=0,rowspan=12,column=0,columnspan=12)
        # Ahora Creamos las Variables de Texto que guardaran la informacion de las rutas
        self.andreina_variable = tk.StringVar()
        self.javier_variable = tk.StringVar()

        # Y creamos las Labels para la informacion de las rutas
        self.andreina_label = tk.Label(master=self.andreina_frame,font=label_font,textvariable=self.andreina_variable)
        self.javier_label = tk.Label(master=self.javier_frame,font=label_font,textvariable=self.javier_variable)

        # Y posicionamos las Labels en sus lugares respectivos
        self.andreina_label.grid(row=1,rowspan=10,column=1,columnspan=10,sticky='nsew')
        self.javier_label.grid(row=1,rowspan=10,column=1,columnspan=10,sticky='nsew')

        # Creamos un Boton para ejecutar el codigo y botones de seleccion
        self.selection_var = tk.IntVar(value=1)

        self.execute_button = tk.Button(master=self.button_frame,text='Buscar Ruta Más Corta',command=self.buscar_ruta,font=button_font)
        self.selection_option_1 = tk.Radiobutton(master=self.button_frame,value=1,text='Discoteca The Darkness',variable=self.selection_var,font=label_font)
        self.selection_option_2 = tk.Radiobutton(master=self.button_frame,value=2,text='Bar La Pasión',variable=self.selection_var,font=label_font)
        self.selection_option_3 = tk.Radiobutton(master=self.button_frame,value=3,text='Cervecería Mi Rolita',variable=self.selection_var,font=label_font)

        # Posicionamos los Botones dentro de su padre 

        self.execute_button.grid(row=3,rowspan=6,column=8,columnspan=3,sticky='nsew')
        self.selection_option_1.grid(row=0,rowspan=4,column=1,columnspan=6,sticky='nsew')
        self.selection_option_2.grid(row=4,rowspan=4,column=1,columnspan=6,sticky='nsew')
        self.selection_option_3.grid(row=8,rowspan=4,column=1,columnspan=6,sticky='nsew')

        # Finalmente creamos los elementos de la cuadricula
        self.drawing_elements : list[list[tk.LabelFrame]] = [[tk.LabelFrame(master=self.drawing_frame,height=12,width=12) for _ in range(36) ] for _ in range(36) ]
        for i in range(6):
            for j in range(6):
                self.drawing_elements[i][j].grid(row=i,rowspan=1,column=j,columnspan=1)
                self.drawing_elements[i][j].config(bg='#000000')
        drawing_width = self.drawing_frame.winfo_width()
        drawing_height = self.drawing_frame.winfo_height()

        # TODO Hacer los calculos vectoriales de las lineas entre los recuadros del grafo
        
        #Coloración de la Interfaz
        self.configure(bg='#000000')
        self.master.configure(bg='#000000')
        self.title_frame.configure(bg='#F2F6D0')
        self.title_label.configure(bg='#F2F6D0')
        self.andreina_frame.configure(bg='#D0E1D4')
        self.javier_frame.configure(bg='#D0E1D4')
        self.andreina_label.configure(bg='#FFFFFF')
        self.javier_label.configure(bg='#FFFFFF')
        self.credits_frame.configure(bg='#D0E1D4')
        self.credits_label.configure(bg='#D0E1D4')
        self.subtitle_frame.configure(bg='#D0E1D4')
        self.subtitle_label.configure(bg='#D0E1D4')
        self.button_frame.configure(bg='#D0E1D4')
        self.selection_option_1.configure(bg='#D0E1D4')
        self.selection_option_2.configure(bg='#D0E1D4')
        self.selection_option_3.configure(bg='#D0E1D4')
        self.representation_frame.configure(bg='#D0E1D4')
        self.drawing_frame.configure(bg='#FFFFFF')
        self.execute_button.configure(bg='#E4BE9E')
        self.master.mainloop()
    def buscar_ruta(self, _=None) -> None:
        pass

    def close(self, _=None) -> None:
        self.master.destroy()

