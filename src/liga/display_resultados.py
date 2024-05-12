import tkinter as tk
from tkinter import ttk
from getters import resultados


class TablaResultados:
    def __init__(self, root, div) -> None:
        self.div = div
        self.root = root
        self.label = ttk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=3)
        self.table = ttk.Treeview(
            self.root,
            columns=("c1", "c2", "c3", "c4", "c5"),
            show="headings",
            selectmode="browse",
        )
        self.table.heading("c1", text="ID")
        self.table.heading("c2", text="Equipo1")
        self.table.heading("c3", text="Puntuación")
        self.table.heading("c4", text="Equipo2")
        self.table.heading("c5", text="Puntuación")
        self.table.grid(row=1, column=0, columnspan=3)
        self.back_button = tk.Button(self.root, text="< Prev")
        self.back_button.grid(row=2, column=0)
        self.next_button = tk.Button(self.root, text="Next >")
        self.next_button.grid(row=2, column=2)
        self.my_display(1, self.div)

    def my_display(self, n, division):
        self.n = n
        self.label.config(text=f"Jornada {self.n}")
        gen = resultados().get_resultados_jornada(division, self.n)
        next_gen = resultados().get_resultados_jornada(division, self.n + 1)
        for item in self.table.get_children():
            self.table.delete(item)
        for team in gen:
            self.table.insert(parent="", index=tk.END, values=team)

        back = self.n - 1
        next = self.n + 1
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
