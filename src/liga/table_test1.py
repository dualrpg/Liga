import tkinter as tk
import getters


d = getters.divisiones()
temp = getters.temporada()


def func(name, root):
    mylist = temp.get_division(name[0])
    t = Table(root, mylist)


class ButtonList:

    def __init__(self, root, mylist):
        for item in mylist:
            button = tk.Button(root, text=item, command=lambda x=item: func(x, root))
            button.grid()


class Table:

    def __init__(self, root, lst):
        total_rows = len(lst)
        total_columns = len(lst[0])

        for i in range(total_rows):
            for j in range(total_columns):

                self.e = tk.Entry(root, width=20, fg="blue", font=("Arial", 16, "bold"))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, lst[i][j])


lst = d.get_division()

root = tk.Tk()
mylist = d.get_division()
t = ButtonList(root, mylist)
root.mainloop()
