import tkinter as tk
from tkinter import ttk
from display_temporada import TablaTemporada
from display_resultados import TablaResultados
from display_equipos import TablaEquipos
from display_lesiones import TablaLesiones
from display_faltas import TablaFaltas
from display_goles import TablaGoles


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()

        self.root.title("Liga")
        self.root.geometry()
        self.root.rowconfigure(0, weight=1)
        self.style = ttk.Style(self.root)
        self.style.theme_create(
            "MyStyle",
            parent="alt",
            settings={
                "TNotebook": {
                    "configure": {
                        "self.tabposition": "wn",
                    }
                },
                "TNotebook.Tab": {
                    "configure": {"width": 10},
                },
            },
        )
        self.style.theme_use("MyStyle")
        self.main()
        self.resultados1.table.bind(
            "<Visibility>",
            lambda event: self.resultados1.my_display(self.resultados1.n, self.resultados1.div),
        )
        self.root.mainloop()

    def main(self):
        self.notebook = ttk.Notebook(self.root)
        self.tab1 = ttk.Notebook(self.notebook)
        self.tab2 = ttk.Notebook(self.notebook)
        self.tab3 = ttk.Notebook(self.notebook)
        self.tab4 = ttk.Notebook(self.notebook)
        self.tab5 = ttk.Notebook(self.notebook)
        self.tab6 = ttk.Notebook(self.notebook)
        self.temporada()
        self.resultados()
        self.equipos()
        self.lesiones()
        self.faltas()
        self.goles()
        self.notebook.add(self.tab1, text="Temporada")
        self.notebook.add(self.tab2, text="Resultados")
        self.notebook.add(self.tab3, text="Equipos")
        self.notebook.add(self.tab4, text="Lesiones")
        self.notebook.add(self.tab5, text="Faltas")
        self.notebook.add(self.tab6, text="Goles")
        self.notebook.grid(row=0, column=0, sticky="nsew")

    def temporada(self):
        self.tab1_subtab1 = ttk.Frame(self.tab1)
        self.tab1.add(self.tab1_subtab1, text="Primera")
        self.temporada1 = TablaTemporada(self.tab1_subtab1, "Primera")
        self.tab1_subtab2 = ttk.Frame(self.tab1)
        self.tab1.add(self.tab1_subtab2, text="Segunda")
        self.temporada2 = TablaTemporada(self.tab1_subtab2, "Segunda")

    def resultados(self):
        self.tab2_subtab1 = ttk.Frame(self.tab2)
        self.tab2.add(self.tab2_subtab1, text="Primera")
        self.resultados1 = TablaResultados(self.tab2_subtab1, "Primera")
        self.tab2_subtab2 = ttk.Frame(self.tab2)
        self.tab2.add(self.tab2_subtab2, text="Segunda")
        self.resultados2 = TablaResultados(self.tab2_subtab2, "Segunda")

    def equipos(self):
        self.tab3_subtab1 = ttk.Frame(self.tab3)
        self.tab3.add(self.tab3_subtab1, text="Primera")
        self.equipos1 = TablaEquipos(self.tab3_subtab1, "Primera")
        self.tab3_subtab2 = ttk.Frame(self.tab3)
        self.tab3.add(self.tab3_subtab2, text="Segunda")
        self.equipos2 = TablaEquipos(self.tab3_subtab2, "Segunda")

    def lesiones(self):
        self.tab4_subtab1 = ttk.Frame(self.tab4)
        self.tab4.add(self.tab4_subtab1, text="Primera")
        self.lesiones1 = TablaLesiones(self.tab4_subtab1, "Primera")
        self.tab4_subtab2 = ttk.Frame(self.tab4)
        self.tab4.add(self.tab4_subtab2, text="Segunda")
        self.lesiones2 = TablaLesiones(self.tab4_subtab2, "Segunda")

    def faltas(self):
        self.tab5_subtab1 = ttk.Frame(self.tab5)
        self.tab5.add(self.tab5_subtab1, text="Primera")
        self.faltas1 = TablaFaltas(self.tab5_subtab1, "Primera")
        self.tab5_subtab2 = ttk.Frame(self.tab5)
        self.tab5.add(self.tab5_subtab2, text="Segunda")
        self.faltas2 = TablaFaltas(self.tab5_subtab2, "Primera")

    def goles(self):
        self.tab6_subtab1 = ttk.Frame(self.tab6)
        self.tab6.add(self.tab6_subtab1, text="Primera")
        self.goles1 = TablaGoles(self.tab6_subtab1, "Primera")
        self.tab6_subtab2 = ttk.Frame(self.tab6)
        self.tab6.add(self.tab6_subtab2, text="Segunda")
        self.goles2 = TablaGoles(self.tab6_subtab2, "Primera")

    def reload(self, frame):
        pass


class events:
    def __init__(self) -> None:
        pass


MainWindow()
