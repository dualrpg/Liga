import tkinter as tk
from tkinter import ttk
import getters

d = getters.divisiones()
g = getters.generico()

options = [
    "Temporada",
    "Resultados",
    "Equipos",
    "Lesiones",
    "Faltas",
]


def div():
    return d.get_division()


class MainWindow:
    def __init__(self, options) -> None:
        self.root = tk.Tk()

        self.root.title("Liga")
        self.root.geometry("900x900")
        self.root.rowconfigure(0, weight=1)
        self.style = ttk.Style(self.root)
        self.style.theme_create(
            "MyStyle",
            parent="alt",
            settings={
                "TNotebook": {
                    "configure": {
                        "tabposition": "wn",
                    }
                },
                "TNotebook.Tab": {
                    "configure": {"width": 10},
                },
            },
        )
        self.style.theme_use("MyStyle")

        self.suboptions = [
            "Temporada",
            "Resultados",
            "Equipos",
            "Lesiones",
            "Faltas",
        ]
        self.frame1 = self.tabs(self.root, self.suboptions)
        self.tabs(self.frame1, d.get_division())

        self.root.mainloop()

    def tabs(self, space, options):
        notebook = ttk.Notebook(space)
        for item in options:
            frame = tk.Frame(notebook)

            notebook.add(frame, text=item)
        notebook.grid(row=0, column=0, sticky="nsew")
        if frame:
            return frame


MainWindow(options)
