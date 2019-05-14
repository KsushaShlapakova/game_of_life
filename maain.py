from tkinter import *
import random


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.active = False
        self.cell = Cell(master)
        self.create_widgets()
        master.title("Game of Life")

    def create_widgets(self):
        self.width = Label(self)
        self.width['text'] = 'Введите ширину экрана:'
        self.width.grid(row=0, column=0, columnspan=2, sticky=W)

        self.ent_w = Entry(self)
        self.ent_w.grid(row=0, column=1, sticky=W)

        self.ent_h = Entry(self)
        self.ent_h.grid(row=1, column=1, sticky=W)

        self.height = Label(self)
        self.height['text'] = 'Введите высоту экрана: '
        self.height.grid(row=1, column=0, sticky=W)

        self.btn_submit = Button(self)
        self.btn_submit['text'] = 'Ввести'
        self.btn_submit['command'] = self.values
        self.btn_submit.grid(row=2, column=0, sticky=W)

        self.btn = Button(self)
        self.btn['text'] = 'Старт'
        self.btn['command'] = self.start
        self.btn.grid(row=3, column=0, sticky=W)

        self.btn1 = Button(self)
        self.btn1['text'] = 'Сгенерировать'
        self.btn1['command'] = self.generate
        self.btn1.grid(row=3, column=1, sticky=W)

    def generate(self):
        self.active = False
        self.cell.g.generate()
        self.active = True
        self.btn['text'] = 'Cтоп'
        self.refresh()

    def values(self):
        self.active = False
        a = self.ent_w.get()
        b = self.ent_h.get()

        try: a = int(a)
        except: a = 50

        try: b = int(b)
        except: b = 50

        if a <= 0: a = 50
        if b <= 0: b = 50

        self.cell.rebuild(a, b)

    def refresh(self):
        if self.active:
            self.btn['text'] = 'Cтоп'
            self.cell.g.update()
            self.cell.canvas.after(20, self.refresh)

    def start(self):
        if self.active:
            self.btn['text'] = 'Старт'
            self.active = False
        else:
            self.btn['text'] = 'Cтоп'
            self.active = True
            self.refresh()


class Cell(Frame):
    def __init__(self, master, x=10, y=10, i=10, j=10):
        super(Cell, self).__init__(master)
        self.root = master
        self.life = False
        self.pos_screen = (x, y)
        self.pos_matrix = (i, j)
        self.open()
        self.rebuild()

    def toggle_cell(self, event):
        jj = int(event.x / self.pos_matrix[0])
        ii = int(event.y / self.pos_matrix[1])
        self.g.set_value(jj, ii, True, True)

    def open(self):
        self.canvas = Canvas(self.root)
        self.g = Life(self.canvas)
        self.root.grid()
        self.canvas.grid()
        self.canvas.bind('<Button-1>', self.toggle_cell)

    def rebuild(self, a=50, b=50):
        self.a = a
        self.b = b
        self.canvas.config(width=a*10, height=b*10)
        self.g.resize(a, b)
        for i in range(b):
            for j in range(a):
                x = 10 * j
                y = 10 * i
                rect = self.canvas.create_rectangle(x, y, x+10, y+10, fill="white")
                self.g.set(j, i, [rect, False, j, i])


class Life:
    def __init__(self,canvas, a=10, b=10):
        self.canvas = canvas
        self.grid = []
        self.resize(a, b)
        self.life = 'white'
        self.death = 'black'

    def generate(self):
        for i in self.grid:
            if random.choice([True, False]):
                self.set_value(i[2], i[3], False)
            else:
                self.set_value(i[2], i[3], True)

    def set(self, x, y, cell):
        self.grid[self.a * y + x] = cell

    def set_value(self, x, y, value, toggle=False):
        c = self.cell(x, y)
        if toggle:
            c[1] = not c[1]
            if c[1]:
                self.canvas.itemconfig(c[0], fill=self.death)
            else:
                self.canvas.itemconfig(c[0], fill=self.life)
        else:
            if c[1] != value:
                c[1] = value
                if value:
                    self.canvas.itemconfig(c[0], fill=self.death)

                else:
                    self.canvas.itemconfig(c[0], fill=self.life)

    def update(self):
        for i in self.grid:
            n = self.n_cells(i[2], i[3])
            c = self.count(n, True)
            if c == 3:
                self.set_value(i[2], i[3], True)
            elif c > 3 or c < 2:
                self.set_value(i[2], i[3], False)


    def resize(self, a, b):
        for i in self.grid:
            if i:
                self.canvas.delete(i[0])
        self.a = a
        self.b = b
        self.grid = []
        self.grid = [None, ]*(a*b)

    def cell(self, x, y):
        return self.grid[self.a * y + x]

    def n_cells(self, x, y):
        n = []
        if x > 0: n.append(self.cell(x-1, y))
        if y > 0: n.append(self.cell(x, y-1))

        if x < self.a - 1:
            if y > 0:
                n.append(self.cell(x+1, y-1))
            n.append(self.cell(x+1, y))

        if y < self.b - 1:
            if x > 0:
                n.append(self.cell(x-1, y+1))
            n.append(self.cell(x, y+1))

        if x > 0 and y > 0: n.append(self.cell(x-1, y-1))
        if x < self.a - 1 and y < self.b - 1: n.append(self.cell(x + 1, y + 1))

        return n

    def count(self, n, value):
        c = 0
        for i in n:
            if i[1] == value:
                c += 1
        return c


def main():
    root = Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
