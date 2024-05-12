import tkinter as tk
from tkinter import ttk
from getters import temporada, resultados
import controller


class TablaTemporada:
    def __init__(self, root, div) -> None:
        self.acciones = controller.acciones()
        self.div = div
        self.root = root
        self.label = ttk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=3)
        self.table = ttk.Treeview(
            self.root, columns=("c1", "c2", "c3"), show="headings", selectmode="browse"
        )
        self.table.heading("c1", text="ID")
        self.table.heading("c2", text="Equipo1")
        self.table.heading("c3", text="Equipo2")
        self.table.grid(row=1, column=0, columnspan=3, sticky="we")
        self.back_button = tk.Button(self.root, text="< Prev")
        self.back_button.grid(row=2, column=0)
        self.next_button = tk.Button(self.root, text="Next >")
        self.next_button.grid(row=2, column=2)
        self.generar = tk.Button(self.root)
        self.generar.grid(row=4, column=1)
        self.my_display(1, self.div)

    def my_display(self, n, division):
        self.label.config(text=f"Jornada {n}")
        gen = temporada().get_partidos_jornada(division, n)
        next_gen = temporada().get_partidos_jornada(division, n + 1)
        temp = resultados().get_resultados_jornada(division, n)
        for item in self.table.get_children():
            self.table.delete(item)
        for team in gen:
            self.table.insert(parent="", index=tk.END, values=team)

        back = n - 1
        next = n + 1
        self.back_button.config(command=lambda: self.my_display(back, division))
        self.next_button.config(command=lambda: self.my_display(next, division))
        if len(next_gen) == 0:
            self.next_button["state"] = "disabled"  # disable next button
        else:
            self.next_button["state"] = "active"  # enable next button

        if n != 1:
            self.back_button["state"] = "active"  # enable Prev button
        else:
            self.back_button["state"] = "disabled"  # disable Prev button
        self.generar.config(
            text=f"Generar resultados jornada {n}",
            command=lambda: self.generar_resultados(n, division),
        )
        if len(temp) != 0:
            self.generar["state"] = "disabled"
        else:
            self.generar["state"] = "active"

    def generar_resultados(self, n, division):
        ids = self.acciones.teamsDay(n, division)
        for id in ids:
            self.acciones.insert_asignar_goles(id)
            self.acciones.insertAsignarFaltas(id, "normal")
            self.acciones.insert_asignar_lesiones(id, "normal")
        self.generar["state"] = "disabled"
