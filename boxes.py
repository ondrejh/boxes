from tkinter import *
import random

from play import Play


class Boxes:

    def __init__(self, frame, columns, rows, size=20):

        self.frame = frame
        self.x = columns
        self.y = rows
        self.c = []

        for y in range(self.y):
            self.c.append([])
            for x in range(self.x):
                self.c[-1].append(Frame(self.frame, height=size, width=size, relief=FLAT, bg='#fff', bd=2))
                self.c[-1][-1].grid(row=y, column=x)

        self.frame.pack()

        self.colours = [None, '#f00', '#0f0', '#00f', '#ff0', '#f0f', '#0ff', '#888']

    def set_color(self, column, row, color=None):

        self.c[row][column]['relief'] = RAISED if color else FLAT
        self.c[row][column]['bg'] = color if color else '#fff'

    def set_field(self, field):

        for y in range(self.y):
            for x in range(self.x):
                self.set_color(x, y, self.colours[field[y][x]])


if __name__ == "__main__":

    width = 8
    height = 20

    random.seed()

    root = Tk()
    main = Frame(root)
    main.pack()
    frm_boxes = Frame(main)
    boxes = Boxes(frm_boxes, width, height)
    frm_boxes.pack()

    play = Play(width, height)

    def down():
        play.piece_fall()
        boxes.set_field(play.field)
        root.after(500, down)

    def rotate():
        play.piece_rotate('L')
        boxes.set_field(play.field)

    def rotate_clock():
        play.piece_rotate('R')
        boxes.set_field(play.field)

    def left():
        play.piece_move('L')
        boxes.set_field(play.field)

    def right():
        play.piece_move('R')
        boxes.set_field(play.field)

    frm_buttons = Frame(main)
    frm_buttons.pack()

    btn_rotate = Button(frm_buttons, text='C', width=1, command=rotate_clock)
    btn_rotate.pack(side=LEFT)

    #btn_rotate_left = Button(frm_buttons, text='A', width=1, command=rotate)
    #btn_rotate_left.pack(side=LEFT)

    btn_move_left = Button(frm_buttons, text='L', width=1, command=left)
    btn_move_left.pack(side=LEFT)

    btn_move_right = Button(frm_buttons, text='R', width=1, command=right)
    btn_move_right.pack(side=LEFT)

    root.after(500, down)
    root.mainloop()
