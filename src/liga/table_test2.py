import tkinter as tk
from tkinter.ttk import LabelFrame
import getters

d = getters.divisiones()
g = getters.generico()

options = d.get_division()


def div():
    return d.get_division()


class MainWindow:
    def __init__(self, options) -> None:
        root = tk.Tk()

        root.title("Liga")
        root.geometry("900x900")
        root.rowconfigure(0, weight=1)

        frame1 = LabelFrame(root, text="Main")

        frame1.grid(row=0, column=0, sticky="nsew")

        suboptions = [
            "Temporada",
            "Resultados",
            "Equipos",
            "Lesiones",
            "Faltas",
        ]

        for item in options:
            button = tk.Button(
                frame1,
                text=item,
                width="10",
                command=lambda x=item: self.frame2(root, suboptions, x),
            )
            button.grid()

        root.mainloop()

    def frame2(self, root, options, name):
        frame2 = LabelFrame(root, text=name)

        frame2.grid(row=0, column=1, sticky="nsew")

        for item in options:
            button = tk.Button(
                frame2,
                text=item,
                width="10",
                command=lambda x=item: self.frame3(root, x, name[0]),
            )
            button.grid()

    def frame3(self, root, name, division):
        frame3 = LabelFrame(root, text=name)

        tabla = g.get_todo_division(name, division)

        total_rows = len(tabla)
        total_columns = len(tabla[0])

        frame3.grid(row=0, column=2)

        for i in range(total_rows):
            for j in range(total_columns):

                self.e = tk.Entry(
                    frame3, width=20, fg="blue", font=("Arial", 16, "bold")
                )

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, tabla[i][j])


t = MainWindow(options)
