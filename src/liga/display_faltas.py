import tkinter as tk
from tkinter import ttk
from getters import faltas


class TablaFaltas:
    def __init__(self, root, div) -> None:
        self.div = div
        self.limit = 10
        self.root = root
        self.label = ttk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=3)
        self.table = ttk.Treeview(
            self.root,
            columns=("c1", "c2", "c3", "c4"),
            show="headings",
            selectmode="browse",
        )
        self.table.heading("c1", text="ID Partido")
        self.table.heading("c2", text="Jugador")
        self.table.heading("c3", text="Amarillas")
        self.table.heading("c4", text="Rojas")
        self.table.grid(row=1, column=0, columnspan=3)
        self.back_button = tk.Button(self.root, text="< Prev")
        self.back_button.grid(row=2, column=0)
        self.next_button = tk.Button(self.root, text="Next >")
        self.next_button.grid(row=2, column=2)
        self.my_display(0, self.div)

    def my_display(self, n, division):
        self.label.config(text=f"Jornada {n}")
        gen = faltas().get_faltas_division(division, n, self.limit)
        next_gen = faltas().get_faltas_division(division, n + self.limit, self.limit)
        for item in self.table.get_children():
            self.table.delete(item)
        for team in gen:
            self.table.insert(parent="", index=tk.END, values=team)

        back = n - self.limit
        next = n + self.limit
        self.back_button.config(command=lambda: self.my_display(back, division))
        self.next_button.config(command=lambda: self.my_display(next, division))
        if len(next_gen) == 0:
            self.next_button["state"] = "disabled"  # disable next button
        else:
            self.next_button["state"] = "active"  # enable next button

        if n != 0:
            self.back_button["state"] = "active"  # enable Prev button
        else:
            self.back_button["state"] = "disabled"  # disable Prev button
